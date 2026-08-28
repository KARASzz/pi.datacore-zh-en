# pi.dev local knowledge base

This directory is a reproducible, local archive of the publicly reachable
content on <https://pi.dev/>. It is deliberately scoped to the canonical
\`https://pi.dev\` origin: external links are recorded in the link graph but
are not fetched.

## What the archive contains

- \`raw/html/\`: response bodies for public HTML pages
- \`raw/assets/\`: same-origin assets referenced by archived content
- \`markdown/\`: Markdown extractions of HTML pages, with source metadata
- \`crawl/\`: the captured robots.txt, run metadata, manifest, failures, and
  skip decisions
- \`metadata/\`: page inventory, asset inventory, URL map, and link graph
- \`reports/coverage.md\`: capture totals, scope, and known limitations
- \`checksums/SHA256SUMS\`: integrity hashes for generated archive files

## Re-running the capture

Run the crawler from this directory:

    node crawl-pi-dev.mjs

The crawler first downloads and applies robots.txt, uses one request at a time
with a configurable delay, avoids external and side-effecting endpoints, and
uses a bounded URL budget to protect against accidental infinite query spaces.
Its defaults can be adjusted only when a broader recrawl is intentionally
needed:

    PI_DEV_CRAWL_DELAY_MS=500 PI_DEV_CRAWL_MAX_URLS=5000 node crawl-pi-dev.mjs

The run report states whether the budget was reached; do not treat a
budget-limited run as a complete snapshot.

## Provenance and use

Every Markdown record identifies its source URL, retrieval time, raw archived
file, and SHA-256 checksum. The site footer displayed at capture time refers
to an MIT License, but this archive makes no independent licence assertion for
all site material. Retain provenance and verify rights before redistribution.
