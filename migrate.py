import html
from pathlib import Path
import re
from typing import Dict, Any

from slugify import slugify

import yaml


ARTICLES_EXPORT_PATH = "lmdg_articles.yml"
DOCUMENT_EXPORT_PATH = "lmdg_documents.yml"
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
Author: {author}
Lang: fr
Status: published

{text}
"""

PARSED_DOCUMENTS: Dict[str, Any] = {}

def parse_documents(documents: Dict[str, Any]) -> None:
    global PARSED_DOCUMENTS

    for doc in documents:
        if doc["media"] != "image" or doc["statut"] != "publie":
            continue

        id = str(doc["id_document"])
        filename = doc["fichier"][4:]
        if filename.startswith("pl_"):
            filename = "planche_" + filename[3:]

        PARSED_DOCUMENTS[id] = {
            "id": id,
            "path": f"images/{filename}",
            "title": html.escape(doc["titre"]),
        }


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

    align = m.group(2)
    path = "{static}/" + doc["path"]
    title = doc["title"]
    return f"""<img style="float: {align};" alt="{title}" src="{path}">"""


def cleanup_text(text: str) -> str:
    text = re.sub("\\r", "\\n", text)

    pattern = "{{{(.*) :}}}"
    text = re.sub(pattern, "## \\1", text)
    pattern = "{{{(.*)}}}"
    text = re.sub(pattern, "## \\1", text)

    text = (
        text.replace("-*", "-")
        .replace("{{", "**").replace("}}", "**")
        .replace("{", "*").replace("}", "*")
    )

    pattern = "<emb([0-9]+)\|(right|center|left)>"

    text = re.sub(pattern, image_ref_replace, text)
    return text


if __name__ == "__main__":
    with open(ARTICLES_EXPORT_PATH, "r") as articles_fh:
        articles = yaml.load(articles_fh, Loader=yaml.Loader)

    with open(DOCUMENT_EXPORT_PATH, "r") as documents_fh:
        documents = yaml.load(documents_fh, Loader=yaml.Loader)

    parse_documents(documents)

    for a in articles:
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
            "text": text,
        }
        if a["id_rubrique"] == 4:
            context["author"] = "Brigitte Baret"
        else:
            context["author"] = None

        if a["id_rubrique"] == 2:
            if slug not in ("presentation-de-l-association",):
                continue
            else:
                context["summary"] = ""

        page = ARTICLE_TEMPLATE.format(**context)

        if a["id_rubrique"] == 1:
            filename = Path(OUTPUT_PATH) / "les-planches" / f"{slug}.md"
        else:
            filename = Path(OUTPUT_PATH) / "pages" / f"{slug}.md"
        with open(filename, "w") as fh:
            fh.write(page)

