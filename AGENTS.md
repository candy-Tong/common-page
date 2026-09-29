# Common Page publishing rules

This repository hosts multiple independent static websites on GitHub Pages.

## Stable URLs

- Site root: https://candy-tong.github.io/common-page/
- Put each project in `<type>/<topic>/<project>/index.html`.
- Existing project: `research/agents/jev-claude/`.
- Never overwrite the root `index.html` with an individual research page.
- Never rename or remove an existing project route unless explicitly requested.
- Keep project-specific CSS, JavaScript and assets inside its own directory.
- Use relative links, including a link back to the repository's shared homepage. Do not use `/assets/...` paths that escape `/common-page/`.

## Register a page

Append an entry to `sites.json` without removing unrelated entries. Required fields: `id`, `title`, `description`, `category`, `path`, `date`, `tags`. `path` is a lowercase, relative directory ending in `/`. The shared homepage loads this manifest and supports search.

## Checks and publication

Run `python scripts/check.py` and preview from the repository root with `python -m http.server 8000`. Check the page on desktop and mobile, all local resource links, graph interactions and calculators. Preserve source links, research dates and labels for simulated data. Never invent API test results.

GitHub Pages uses the `main` branch and repository root. Keep `.nojekyll`. After committing, inspect the Pages deployment run and verify the exact public nested URL. A successful file commit is not proof that publishing has finished.

## Safety and scope

Do not commit secrets, tokens, private account data or files from other projects. Read the current branch and existing files before replacing content; preserve concurrent changes. Make GitHub changes through the GitHub connector when that is the user's requested workflow. Do not use credential extraction or browser automation as a substitute.
