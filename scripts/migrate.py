import html
from pathlib import Path
import re
from typing import Any, Dict, List

from slugify import slugify

import yaml


ARTICLES_EXPORT_PATH = "lmdg_articles.yml"
DOCUMENT_EXPORT_PATH = "lmdg_documents.yml"
LINKS_EXPORT_PATH = "lmdg_documents_liens.yml"
OUTPUT_PATH = "content"

RUBRIQUE = {
    1: "Les planches",
    2: "L'association «Les mots du Gène»",
    4: "Eugène Vicat",
}


ARTICLE_TEMPLATE = """Title: {titre}
Date: {date}
Modified: {modified}
Slug: {slug}
Summary: {summary}
Lang: fr
Status: published
"""

# Keep the \n at the beginning of next string!! Otherwise image
# templates may me splitted on multiple lines
IMAGE_TEMPLATE = """
<figure class="image-block" style="float: {align};">
  <img alt="{title}" src="{path}">
  <figcaption style="max-width: {width}px">{title}</figcaption>
</figure>
"""


VIDEO_TEMPLATE = """
<video width="320" height="240" controls>
  <source src="{path}" type="video/mp4">
</video>
"""

PARSED_DOCUMENTS: Dict[str, Any] = {}
PARSED_LINKS: Dict[str, List[str]] = {}

def parse_documents() -> None:
    global PARSED_DOCUMENTS

    with open(DOCUMENT_EXPORT_PATH, "r") as documents_fh:
        documents = yaml.load(documents_fh, Loader=yaml.Loader)

    for doc in documents:
        if doc["statut"] not in ("publie", "prop", "prepa"):
            continue

        id = str(doc["id_document"])
        filename = doc["fichier"][4:]
        media = doc["media"]
        if media == "image":
            if filename.startswith("pl_"):
                filename = "planche_" + filename[3:]
            elif filename.startswith("panche_"):
                filename = "planche_" + filename[7:]
            elif filename.startswith("planch_"):
                filename = "planche_" + filename[7:]

            prefix = "images"
            width = doc["largeur"]
            height = doc["hauteur"]
        elif media == "video":
            prefix = "videos"
            width = 320
            height = 240
        else:
            continue

        PARSED_DOCUMENTS[id] = {
            "id": id,
            "media": media,
            "path": f"{prefix}/{filename}",
            "title": html.escape(doc["titre"]),
            "width": width,
            "height": height,
        }

def parse_liens() -> None:
    global PARSED_LINKS

    with open(LINKS_EXPORT_PATH, "r") as links_fh:
        links = yaml.load(links_fh, Loader=yaml.Loader)

    for link in links:
        id = str(link["id_objet"])
        if id not in PARSED_LINKS:
            PARSED_LINKS[id] = []

        PARSED_LINKS[id].append(str(link["id_document"]))


def cleanup_title(title: str) -> str:
    pattern = "[0-9]+\. "
    m = re.match(pattern, title)
    return title[m.end():] if m else title


def build_slug(article: Dict[str, Any]) -> str:
    if article["id_rubrique"] == 1:
        title = article["titre"]
        pattern = "([0-9]+)\. "
        m = re.match(pattern, title)
        if m:
            slug_base = f"{title[m.end():]}"
        else:
            slug_base = title
    else:
        slug_base = cleanup_title(article["titre"])

    return slugify(slug_base)


def image_ref_replace(m: re.Match) -> str:
    id = m.group(1)
    doc = PARSED_DOCUMENTS.get(id)
    if doc is None:
        print(f"WARNING: {id} not found!")
        return ""
    elif doc["media"] != "image":
        print(f"WARNING: Unexpected media type!")
        return ""

    align = m.group(2).lower()
    if align not in ("left", "center", "right"):
        align = "center"
    path = "{static}/" + doc["path"]
    title = doc["title"]
    width = doc["width"]
    return IMAGE_TEMPLATE.format(
        align=align, path=path, title=title, width=width
    )


def cleanup_text(text: str) -> str:
    text = re.sub("\\r", "\\n", text)

    pattern = "}}}( |	)*([^\\n])"
    text = re.sub(pattern, "}}}\\n\\2", text)

    pattern = "{{{(.*) :( |	)*}}}"
    text = re.sub(pattern, "## \\1", text)
    pattern = "{{{(.*)}}}"
    text = re.sub(pattern, "## \\1", text)

    text = (
        text.replace("-*", "-")
        .replace("{{", "**").replace("}}", "**")
        .replace("{", "*").replace("}", "*")
        .replace("~~~", "")
        .replace("-**", "- **")
    )

    pattern = "<emb ?([0-9]+)\|(right|center|left|[0-9]+)\n?>"
    text = re.sub(pattern, image_ref_replace, text, flags=re.IGNORECASE)

    pattern = "( |	)+$"
    text = re.sub(pattern, "\n", text, flags=re.IGNORECASE | re.MULTILINE)

    pattern = "^( |	)+(le)( |	)+(gène.*)"
    text = re.sub(pattern, "\\2 \\4", text, flags=re.IGNORECASE | re.MULTILINE)

    pattern = "^ {3,}"
    text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.MULTILINE)

    return text


if __name__ == "__main__":
    with open(ARTICLES_EXPORT_PATH, "r") as articles_fh:
        articles = yaml.load(articles_fh, Loader=yaml.Loader)

    parse_documents()
    parse_liens()

    for a in articles:
        id = str(a["id_article"])

        title = cleanup_title(a["titre"])
        slug = build_slug(a)
        category = RUBRIQUE.get(a["id_rubrique"])
        text = cleanup_text(a["texte"])

        context = {
            "titre": title,
            "date": a["date"],
            "modified": a["maj"],
            "category": category,
            "slug": slug,
            "summary": a["descriptif"],
        }

        if a["id_rubrique"] == 2:
            if slug not in ("presentation-de-l-association",):
                continue
            else:
                context["summary"] = ""

        page = ARTICLE_TEMPLATE.format(**context)

        if slug == "eugene-vicat-dit-le-gene":
            page += "save_as: index.html\n"

        if a["id_rubrique"] == 4:
            page += "Author: Brigitte Baret\n"

        page += f"\n{text}\n"

        doc_ids = PARSED_LINKS.get(id, [])
        if len(doc_ids) > 0:
            for doc_id in doc_ids:
                doc = PARSED_DOCUMENTS.get(doc_id)
                if doc is None or doc["media"] != "video":
                    continue

                source_path = Path("content/" + doc["path"])
                path = "{static}/" + doc["path"]
                page += VIDEO_TEMPLATE.format(path=path)

        if a["id_rubrique"] == 1:
            filename = Path(OUTPUT_PATH) / "les-planches" / f"{slug}.md"
        else:
            filename = Path(OUTPUT_PATH) / "pages" / f"{slug}.md"

        with open(filename, "w") as fh:
            fh.write(page)

