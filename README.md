# Gantavya Bhatt — personal academic website

Lightweight static HTML/CSS for **https://bhattg.github.io/**, migrated from the public Google Site. No package installation, Ruby, Jekyll, or JavaScript framework is required. The page content and direct navigation links work without JavaScript.

The design combines a compact academic profile, warm ivory background, espresso text, cinnamon accents, and restrained serif headings. A matching night theme uses deep espresso, warm ivory text, and amber accents. The header switch remembers the visitor’s choice; the first visit follows the system color preference. All publications appear in simple image-and-text rows on the homepage, with a standalone publication index and separate photography collections. Photography has a distinct italic serif style and an overview of six visual themes, rather than repeating the 2023 gallery. Highlights of 2024 and 2025 add 35 curated photos from the owner’s Unsplash profile, grouped by verified upload year and shown earliest to latest under month headings.

## Preview and edit

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:4173/.

- Edit biography, news, publication text, links, and gallery captions in `data/content.json`.
- Edit the overview’s introduction and six image selections in `data/photography-overview.json`. Each image references the verified photo inventory used by the annual galleries. The annual `photos` lists render in ascending `posted_at` order.
- Edit the 2024 and 2025 introductions, selections, source captions, locations, and image provenance in `data/unsplash-highlights.json`. The original Google Sites copy, including the replaced 2024 placeholder, remains archived in `data/content.json`.
- Edit the polished photo captions in `data/photo-captions.json`. Original captions remain archived in the source data.
- Edit typography and layout in `site/assets/style.css`. Shared `--type-*`, `--leading-*`, and font-family variables at the top define the same text styles for every page and both themes.
- Edit shared layout in `scripts/build.py`, then rebuild.
- Replace `site/assets/gantavya-bhatt-cv.pdf` to update the CV.
- `data/link-repairs.json` records verified corrections to inherited links. Original copy and URLs remain in the content data and migration inventory.
- Commit the generated `site/` along with the source changes. CI regenerates it before deployment.

## Deployment

Repository: `bhattg/bhattg.github.io`. Existing default branch: `master`.

The workflow `.github/workflows/pages.yml` validates pull requests. A push to `master` or a manual run on `master` builds, validates, uploads only `site/`, and deploys through the `github-pages` environment.

Pages is configured to use **GitHub Actions**. Only `site/` is uploaded in the public deployment artifact; source data and audit records remain repository files. The owner approved publication on October 21, 2026, after reviewing the complete local preview. The prior Jekyll template remains in Git history.

Use a normal fast-forward or pull request merge, preserving the existing repository history. Do not force-push. Check that `master` has not advanced before merging. After the successful Pages run, verify the public home page, gallery navigation, CV, and 404 page.

## Migration record

Google Search Console verification uses `site/googlef9ecd7183dcf04b0.html`. Keep this file at the site root in future deployments so Google can continue to verify ownership.

See `MIGRATION_REPORT.md` for scope, page mapping, fidelity notes, link repairs, verification, and limitations. `migration/` contains the machine-readable source inventory and audit evidence and is excluded from the deployed artifact.

The downloaded photographs, portrait, research figures, and CV retain their original ownership. No new license is applied to those assets.

## Responsive image assets

Full-size originals stay in `site/assets/images/`. Pages use local WebP previews with responsive `srcset` sizing and intrinsic dimensions, generated into `site/assets/previews/`. If adding or replacing images, run `python3 scripts/prepare_images.py` with Pillow available, then build and check as usual. Commit the generated previews and `data/image-variants.json`. Normal CI builds still use only Python’s standard library.

Images retry once against the original file after a request failure. If that also fails, the page offers a “Retry photo” button without requiring a page refresh. CSS and JavaScript URLs include content hashes, and preview filenames include a source/recipe fingerprint so updates avoid stale cached assets. Keep the full-size originals and the Search Console verification file in future deployments.
