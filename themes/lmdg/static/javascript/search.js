'use strict';

const MAX_RESULTS = 5;

document.getElementById('search-field').addEventListener('input', searchAsync);

async function searchAsync() {
    if (!this.value) {
        return;
    }
    const pagefind = await import("/pagefind/pagefind.js");
    if (this.value.length<4) {
        pagefind.preload(this.value);
        return;
    }
    const search = await pagefind.debouncedSearch(this.value);
    if (search != null) {
        const first_found = search.results.slice(0, MAX_RESULTS);
        const first_results_promises = first_found.map(item => item.data());
        const first_results = await Promise.all(first_results_promises);
        console.log(first_results);

        displayResults(first_results);
    }
}

const RESULT_WITH_IMAGE_HTML_TEMPLATE = `
<a href="{url}">
  <div style="float: left; width: 80%; box-sizing: border-box;">
    <h3>{title}</h3>
    <p>{excerpt}</p>
  </div>
  <div style="float: left; width: 20%; padding: 5px; box-sizing: border-box;">
    <img src="{image_url}" alt="{image_alt}">
  </div>
</a>
`;

const RESULT_WITHOUT_IMAGE_HTML_TEMPLATE = `
<a href="{url}">
  <div style="float: left; width: 80%; box-sizing: border-box;">
    <h3>{title}</h3>
    <p>{excerpt}</p>
  </div>
</a>
`;

const EMPTY_RESULT_HTML_TEMPLATE = `
<p>Aucun résultat de trouvé !</p>
`

function displayResults(results) {
    const results_list = document.getElementById('search-results');
    results_list.innerHTML = '';

    if (results.length > 0) {
        results_list.style.display = 'block';
        results.forEach(result => {
            const result_div = document.createElement('div');
            const has_image = result.meta.image && result.meta.image.length > 1;

            const template = has_image ? RESULT_WITH_IMAGE_HTML_TEMPLATE : RESULT_WITHOUT_IMAGE_HTML_TEMPLATE;
            let div_html = template
                .replace("{url}", result.url)
                .replace("{title}", result.meta.title)
                .replace("{excerpt}", result.excerpt);
            if (has_image) {
                div_html = div_html
                           .replace("{image_url}", result.meta.image)
                           .replace("{image_alt}", result.meta.image_alt);
            }
            result_div.innerHTML = div_html;
            results_list.appendChild(result_div);
        });
    } else {
        results_list.style.display = 'block';
        results_list.innerHTML = EMPTY_RESULT_HTML_TEMPLATE;
    }
}
