# Search discovery

Submit the site's sitemap through Google Search Console and Bing Webmaster Tools, then monitor crawl and indexing results. The canonical site is **https://errorgram.rmbk.me/**.

## Published discovery files

| URL | Purpose |
| --- | --- |
| https://errorgram.rmbk.me/sitemap-index.xml | Index of the generated HTML sitemap, including `/playground/` and every condition page. |
| https://errorgram.rmbk.me/robots.txt | Allows crawling and points to the sitemap index. |
| https://errorgram.rmbk.me/llms.txt | Guide and condition index for tools that use this convention. |
| https://errorgram.rmbk.me/llms-full.txt | Complete Markdown guides and reference. |
| https://errorgram.rmbk.me/playground.md | Plain Markdown playground instructions, results, and privacy behavior. |

Starlight generates canonical URLs, titles, descriptions, and the sitemap from the Markdown routes. The playground guide and condition reference are readable without JavaScript. `llms.txt` is an additional discovery convention for tools that support it.

## Google Search Console

1. Sign in at [Google Search Console setup](https://search.google.com/search-console/welcome).
2. Add the URL-prefix property `https://errorgram.rmbk.me/`, or select a verified domain property covering it. Complete ownership verification with the exact value Google supplies. DNS records go in the domain's DNS provider; HTML verification files go in `site/public/` and must be published before verification.
3. Open **Sitemaps** and submit `https://errorgram.rmbk.me/sitemap-index.xml`. Check that the report can fetch and read it.
4. Use **URL Inspection** for the homepage, `/catalogue/`, `/playground/`, and a representative condition page. Check the canonical and crawl access, then choose **Request indexing** where available. This requires owner or full-user access.
5. Monitor the **Sitemaps** and **Page indexing** reports after crawling.

Official references: [Verify site ownership](https://support.google.com/webmasters/answer/9008080), [Submit a sitemap](https://support.google.com/webmasters/answer/183668), and [Ask Google to recrawl URLs](https://support.google.com/webmasters/answer/6065812).

## Bing Webmaster Tools

1. Sign in at [Bing Webmaster Tools](https://www.bing.com/webmasters/).
2. Add `https://errorgram.rmbk.me/`. Import a verified Google Search Console property if offered, or complete Bing's verification using the DNS, file, or meta-tag value its setup provides.
3. Open **Sitemaps** and submit `https://errorgram.rmbk.me/sitemap-index.xml`. Check its processing result.
4. Use **URL Inspection** and **URL Submission**, where available, for the homepage, catalogue, playground, and representative condition pages. Monitor results in the portal.

The [official Bing Webmaster documentation](https://learn.microsoft.com/en-us/bingwebmaster/) covers authenticated APIs for later automation.

## Record an actual submission

Record the date, property, sitemap URL, and processing status in release notes or a maintenance issue after submitting. A build or `robots.txt` alone does not establish submission; submission does not guarantee indexing.

Use the consoles or supported authenticated APIs; omit obsolete unauthenticated sitemap-ping endpoints.
