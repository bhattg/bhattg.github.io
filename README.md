# Gantavya Bhatt — personal academic website

Lightweight static HTML/CSS for **https://bhattg.github.io/**, migrated from the public Google Site. No package installation, Ruby, Jekyll, or JavaScript framework is required. The page content and direct navigation links work without JavaScript.

The design combines a compact academic profile, warm ivory background, espresso text, cinnamon accents, and restrained serif headings. A matching night theme uses deep espresso, warm ivory text, and amber accents. The header switch remembers the visitor’s choice; the first visit follows the system color preference. Publications appear in a minimal text-only list grouped by year, on both the homepage and the dedicated Publications page. Photography has separate collections. Photography has a distinct italic serif style and an overview of six visual themes, rather than repeating the 2023 gallery. Highlights of 2024 and 2025 add 35 curated photos from the owner’s Unsplash profile, grouped by verified upload year and shown earliest to latest in a continuous, fitted photo grid.

## Preview and edit

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:4173/.

- Edit biography, news, and archived source content in `data/content.json`.
- Edit the current publication catalog in `data/publications.json`. Each record stores the verified title, author order, venue, date precision, links, source URLs, and its mapping to Scholar records. Keep the existing IDs to preserve bookmarks. The original 17 publication records remain archived in `data/content.json`.
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

## Compact photography layout

Galleries use balanced rows that size each photograph according to its original aspect ratio, without cropping. The layout adapts to the available width, keeps left-to-right photo order, and reserves room for readable captions. JavaScript refines the row widths; CSS provides a wrapping fallback. Annual highlights have no month headings. The original 2023 essay appears before its photographs, and its photo order and thematic headings remain intact.

## Publication refresh from Google Scholar

The catalog was reviewed against all 30 public Scholar records on October 27, 2026. It contains 24 papers/technical reports and one separately labeled lecture-note contribution. Five duplicate or alternate records are consolidated; the astronomy paper was excluded at the owner’s request. Publisher metadata takes precedence over stale preprint titles and years. NVIDIA reports use the corporate author credited by arXiv, with the owner’s membership in all four full author lists verified. `migration/scholar-publication-inventory.json` records the disposition of every Scholar entry; citation details, authorship evidence, link results, and responsive layout checks are stored alongside it.

Paper thumbnails have been removed from both publication lists. The original image files are retained for provenance. The list uses compact year labels, consistent type, full author lists for ordinary papers, and plain resource links in both themes.

The owner also supplied the NVIDIA Nemotron 3.5 Super and Lightning report directly. Its October 21, 2026 cover date puts it first in the 2026 list; the owner is credited on PDF page 55. This supplementary entry has no assigned Scholar record.

The CV was updated in the owner’s Overleaf Research CV project on October 27, 2026 and the compiled four-page PDF replaced the site download. CV links now include a content hash, so future PDF replacements open the current version. See `migration/cv-update.json` for verification.
