# Google Sites → GitHub Pages migration

**Source:** https://sites.google.com/view/gbhatt/

**Destination:** https://bhattg.github.io/

**Status:** Migration approved by the owner on October 21, 2026; GitHub Pages configured for Actions deployment.

## Content and navigation inventory

Crawled every same-site link exposed by the published navigation and page content, recursively within `/view/gbhatt`. All discovered pages returned HTTP 200. The root and `/home` serve the same academic page. The source photography overview repeated the 2023 gallery. At the owner’s request, the overview is now a distinct portfolio introduction; the full original 2023 narrative and gallery remain at `/photography/highlights-of-2023/`, and the original duplicate overview remains archived in `data/content.json`.

| Original page | New location | Recovered content |
| --- | --- | --- |
| `/view/gbhatt/`, `/view/gbhatt/home` | `/`, `/home/` redirects to `/`, `/publications/` | Biography; research interests; internship and undergraduate details; job-market statement; 5 news updates; 17 publication entries; profile links; CV; portrait; mountain header |
| `/view/gbhatt/photography` | `/photography/` | Owner-requested portfolio summary and six thematic image selections, replacing the duplicate 2023 gallery. Original copy remains in the 2023 page and archive. |
| `/view/gbhatt/photography/highlights-of-2023` | `/photography/highlights-of-2023/` | Full original 2023 gallery and narrative, including the repeated overview content |
| `/view/gbhatt/photography/mountains-by-the-day` | `/photography/mountains-by-the-day/` | 13 photographs and their original captions and locations |
| `/view/gbhatt/photography/mountains-by-the-night` | `/photography/mountains-by-the-night/` | 5 photographs and their original captions and locations |
| `/view/gbhatt/photography/highlights-of-2024` | `/photography/highlights-of-2024/` | Original header and “Stay tuned!” archived; replaced by 19 verified 2024 Unsplash uploads at the owner’s request |
| New collection from `https://unsplash.com/@gbhatt_2` | `/photography/highlights-of-2025/` | 16 verified 2025 Unsplash uploads |

The site has six distinct content pages plus the home alias. The migrated site now has eight content pages: the six source pages plus a dedicated `/publications/` page and new 2025 highlights. At the owner’s request, the 2024 placeholder is replaced by a curated Unsplash collection; its original content remains archived unchanged in `data/content.json`. Navigation links directly to About, Publications, Photography, and CV. All 17 publication entries appear on the homepage and on the standalone publication index. Photography has collection navigation. Existing Google Sites heading fragments for biography, news, and publications are mapped to their new anchors on the new domain.

There was no separate projects page, research page, blog, or downloadable project archive linked on the Google Site. Research information remains in the biography, publication entries, code/project links, and unchanged CV. No project descriptions or achievements were invented.

## Asset recovery

All **55 distinct source image URLs** were recovered, stored locally, and recorded with original URL, local path, byte size, and SHA-256 checksum in `migration/source-assets.json`. This includes publication figures, the portrait, gallery photographs, and header images. Initial direct-download failures were resolved through a browser export for the academic images and refreshed public source pages for gallery images. A recorded original HTTP 403 is an initial attempt; a `local_path` and `recovery` field show successful recovery.

The original linked CV downloaded as a valid **4-page PDF** and is served at `/assets/gantavya-bhatt-cv.pdf`. Its text identifies Gantavya Bhatt and the UW affiliation; the first page was rendered and visually inspected. The PDF bytes were preserved without edits. The original Drive URL remains in the source inventory.

No source photograph or research figure is hotlinked from Google Sites. The website uses local CSS, a small local JavaScript theme and bookmark helper, and system fonts. Gallery images link to their full recovered local files. Publication figures are displayed with `object-fit: contain`.

## Content fidelity and source issues

Biographical statements, authors and author order, equal-contribution symbols, publication titles and venue/status statements, gallery captions, locations, and the photography narrative were retained. Google Sites span formatting, excessive whitespace, menus, search UI, and report-abuse controls were replaced with semantic site markup. Cosmetic headings and social-label capitalization were modernized.

The source footer says **“Last Updated at January 28nd, 2026”**, despite containing May 2026 updates. That exact source string is archived in `data/content.json` and `migration/source-inventory.json`; it is not presented as the new website's update date.

The following source inconsistencies were preserved for owner review rather than silently changing publication facts:

- “Effective Backdoor Mitigation Depends on the Pre-training Objective” has both a TMLR acceptance line and “Under review.”
- The Decay RNN entry uses the same SCIL venue string as the preceding RNN paper, while its paper URL leads to the ACL student research workshop. The original title, authors, and venue wording remain unchanged.
- RadarHD's link labeled “arxiv” points to the same ACM DOI page as its “pdf” link. The original label and valid destination remain preserved.
- The physical video-to-audio publication has no paper/code URL in the source. No guessed link was added.
- The CV contains additional and updated material relative to the webpage. The full original CV is preserved, without merging its differences into the webpage's publication list.

## Verified link repairs

Original URLs are preserved in the source inventory and content data. Repairs are applied by the builder and recorded in `data/link-repairs.json`.

| Issue | Replacement and verification |
| --- | --- |
| Aniket Rege's `/about/` page returned 404 | https://aniketrege.github.io/ — verified current author homepage |
| Aditya Kusupati's UW homepage returned 404 | https://adityakusupati.com/ — verified current author homepage |
| The old Matryoshka title PDF returned 404 | https://arxiv.org/abs/2205.13147 — verified title and authors; this paper was also linked in the original entry |
| LabelBench's “pdf” linked to the backdoor paper | https://data.mlr.press/assets/pdf/v01-7.pdf — verified journal PDF of LabelBench |
| LabelBench's “arxiv” linked to the backdoor paper | https://arxiv.org/abs/2306.09910 — verified record linked by https://github.com/EfficientTraining/LabelBench |

Other working external links remain unchanged. The first pass checked **67 distinct external URLs**. The three confirmed dead destinations above were replaced. ACM and one OpenReview PDF returned 403, Unsplash returned 401, and the two LinkedIn profile URLs returned 405 to automated HEAD requests. These are documented as restricted automated checks, not confirmed dead links; their original links remain available. See `migration/external-links.json` for each response and final redirect URL.

## Verification

- Built successfully with Python's standard library; no external build dependencies.
- Checked 11 HTML files, including the Google verification file; validated generated pages, including the home redirect and 404 page.
- Checked 751 local links, anchors, script/CSS references, and image references: no missing targets.
- Passed 259 text checks across biography, news, publication entries, original galleries, and new highlights. The superseded 2024 placeholder is archived rather than rendered.
- Verified local files and SHA-256 checksums for all 55 source images and validated the CV PDF signature.
- Inspected home, publications, and photography visually in the browser.
- Current light and night layouts passed 48 browser layout checks across all eight content routes at requested viewport widths of 320, 768, and 1280 pixels (actual CSS widths 291, 698, and 1163 due to browser zoom). No horizontal overflow or broken loaded images were found. Deferred images use lazy loading; all image files were independently checked over HTTP. Desktop profile, publication rows, mobile profile, and a photography collection were visually inspected; the browser reported no console errors. The theme switch works with keyboard input, persists across reload and navigation, and updates the browser theme color. Both palettes meet 4.5:1 contrast for all text tokens; see `migration/theme-contrast-checks.json`. See `migration/browser-layout-checks.json`.
- All 446 served files returned HTTP 200 when checked against the running local server.
- Prepared GitHub Actions build, validation, artifact upload, and deployment jobs. Pull requests only build/check; deployment targets `master`.
- The owner approved publication after reviewing the completed site. Hosted deployment and live checks are verified separately from local validation through GitHub Actions run history and the public site.

## Missing content and access limits

**No missing body content, linked source images, or CV among the discovered public pages.** The original 2024 gallery was a “Stay tuned!” placeholder. Its replacement with 19 Unsplash highlights and the new 2025 page were explicitly requested by the owner; the original text and header image remain archived.

Google Sites did not expose a usable sitemap at `/view/gbhatt/sitemap.xml` (HTTP 404). A supplementary public search did not identify additional in-scope pages. The inventory therefore covers all publicly linked pages discoverable from the published site; unpublished drafts, private pages, and unlinked pages absent from public discovery cannot be enumerated. No sign-in-only content was accessed.

The source Google Site URL cannot receive an HTTP redirect controlled by this GitHub repository. After the new site is approved, published, and verified, the owner can add a migration notice/link on the Google Site. No changes have been made to the Google Site.

## Publishing plan and rollback

The existing public repository is `bhattg/bhattg.github.io`, with `master` as its default branch. Before migration, it used legacy Pages deployment from `/` on `master`; it is now configured to use GitHub Actions.

The owner approved publication, and the Pages publishing source has been switched to GitHub Actions. Publish with normal history-preserving Git operations, wait for the workflow, and verify https://bhattg.github.io/. Only `site/` is included in the Pages artifact; audit reports and source data remain repository files.

The old site is retained in existing Git history and the local `work/existing-repository` clone. Record the prior `master` commit before publication. To roll back, revert the migration commit and restore Pages publishing from the original `master` root. No remote files, branches, or settings were changed during preview preparation; the Pages source was changed only after the owner approved publication.

## Design and presentation

The owner requested a blend of Shuran Song’s research-focused structure (https://shurans.github.io/) and the first pre-Galen local preview. The latest refinement uses a portrait beside the biography, warm ivory background, espresso headings and text, cinnamon links, a small caramel accent, restrained serif headings, compact news, and image-and-text publication rows. Profile links align with the portrait, and more generous spacing keeps the academic layout uncluttered. The palette follows the owner’s requested fall/coffee direction. A matching night variant uses deep espresso surfaces, warm ivory text, and amber links. A small sun/moon control changes themes and remembers the selection locally; before an explicit selection, it follows the system color preference. The theme is applied before the stylesheet paints. Research figures and photographs retain their original colors. All 17 original publications appear on the homepage as well as the standalone index. Photography has a small homepage introduction and full collection pages. No reference-site content or images were copied.

All original source text checks, image checksums, PDF validation, local references, and current browser layout checks pass. The local preview is available at http://127.0.0.1:4173/. The owner has approved publication; the live destination is https://bhattg.github.io/.

## Unsplash highlights extension

The owner requested populating 2024 and 2025 highlights from https://unsplash.com/@gbhatt_2. The public profile displayed 210 photos; all 210 photo cards were enumerated through normal public pagination. Pinned photographs do not appear in chronological order, so profile order was not treated as year evidence. Public photo-page metadata was verified for 102 candidates: 78 with `created_at` in 2024 and 24 in 2025. All 102 pages identified `gbhatt_2` as the author; none of those detail requests remained missing. The site's public feed endpoint returned HTTP 401, so public profile and photo pages supplied the data.

The final selection contains **19 photographs for 2024** and **16 for 2025**. This is a curated highlights selection; other verified candidates are recorded as unselected in `migration/unsplash-inventory.json`. Themes include night skies, mountains, forests, desert landscapes, wildlife, and city scenes. The overview’s thematic labels are editorial organization; the annual galleries now use a continuous sequence ordered by verified upload dates. Author descriptions are used verbatim when available; otherwise, the source's descriptive alt text supplies the caption. Source location names are preserved. At the owner’s request, visible Unsplash links were removed from the galleries; the individual source URLs remain in the data and audit inventory.

**Year assignment uses the public Unsplash upload timestamp (`created_at`), not the capture date.** Capture dates were not supplied by the public metadata. The gallery notes refer to photographs “shared” in each year; the exact upload-date basis remains documented here and in the source data. Photographs uploaded in later years were not reassigned to 2024 or 2025 based on visual guesses.

All 35 selected photographs are non-premium, non-Plus public photos by the owner and were downloaded as uncropped JPEGs at up to 1800px width, with SHA-256 checksums and source/download URLs in `data/unsplash-highlights.json`. Their colors and compositions were retained. The original 55 Google Sites images remain intact, including the archived 2024 header. The website now serves 90 local source photographs/figures in total. Both new collections are included in collection navigation and the sitemap, with shared light/night styling and responsive layouts. No Unsplash account content was modified.

## Yearly introductions

At the owner’s request, 2024 and 2025 now open with two-paragraph personal notes in the reflective style of the original 2023 introduction. These are newly drafted editorial copy based on the selected photographs’ documented subjects and locations, without invented trip dates, travel itineraries, career milestones, or other life events. The notes are editable in each gallery’s `introduction` field in `data/unsplash-highlights.json`. The original 2023 note is unchanged.

Repeated image-source links and the source-profile introduction were removed from the two new galleries. Captions and available locations remain; all image links still open local full-size photographs. Source links, authorship, upload timestamps, and checksums remain archived. Both updated introductions were inspected on desktop and checked at three viewport sizes in light and night themes, with no overflow or browser errors.

## Typography consistency

Typography uses a single shared scale across academic pages and every photography collection, including the original 2023 note. Georgia supplies page titles and section headings; the same system sans-serif stack supplies narrative copy, publication titles, navigation, captions, and supporting information. Page titles use 42px on larger screens and 34px on mobile; section headings use 28px and 26px respectively. Academic narrative copy uses 14px with 1.9 line spacing. Following the owner’s later request, photography narrative uses 16px italic Georgia, with 13px italic captions and 12px locations. Shared navigation stays upright at 12px, and footer details use 11px. Semibold text uses one shared weight. The `gb.` monogram remains the intentional italic brand treatment.

Shared variables in `site/assets/style.css` control these roles. Theme switching changes colors, without changing typefaces, font sizes, weights, or spacing. Browser checks across all eight content routes, three sizes, and both themes confirmed matching title and narrative text styles, consistent section headings, no horizontal overflow, and no console errors. No external fonts or build dependencies were introduced.

## Distinct photography overview and italic style

The owner requested replacing the duplicate 2023 Overview with a summary based on the Unsplash portfolio, and using italics throughout the photography section. The new overview has an original two-paragraph introduction grounded in the documented photo subjects and locations, followed by six visual themes: Mountain light, After dark, City skylines, Still water, Forest roads, and Desert landscapes. The six photographs reuse verified local images, and each links directly to its corresponding full annual gallery entry. The small overview thumbnails use a consistent crop; the full local photographs and annual galleries retain their original compositions. No new assets or external links were added.

The overview is editable in `data/photography-overview.json`. The full 2023 essay and images remain on their dedicated page. Original duplicated content remains archived in `data/content.json`; its repeated text is no longer required on the redesigned overview. All original 55 image checksums and 35 Unsplash image checksums remain verified.

A scoped `photography-page` style applies italic Georgia to photography headings, narrative text, and captions consistently across the overview, yearly highlights, and mountain collections. Navigation and site controls remain upright sans-serif; academic typography is unchanged. The same photography typography applies in both color themes. All eight content routes passed 48 browser checks across three requested viewport widths and two themes, with no overflow, missing loaded images, or console errors.

## Chronological yearly galleries

At the owner’s request, the 2024 and 2025 galleries now display every selected photograph from earliest to latest. Month headings were subsequently removed at the owner’s request. The builder sorts by the original verified UTC `posted_at` timestamp; identical timestamps use a stable photo-ID tie-breaker, without claiming a finer sequence within a batch. The opening photograph is the earliest entry, replacing the previous out-of-order featured cover. All 19 photographs from 2024 and 16 from 2025, their captions, locations, source links in the data, and checksums remain intact.

The original 2023 images contain no capture-date metadata. After being asked about their order, the owner explicitly requested ignoring that part; the original 2023 order remains unchanged. No missing dates were guessed. See `migration/gallery-chronology.json` for the exact ordered IDs and timestamps. The static checker now verifies the rendered dates are sorted and complete; twelve browser checks across both updated galleries, three screen sizes, and two themes also confirmed ascending dates, correct photo counts, and no overflow or browser errors.

## Image-loading reliability and revised captions

The owner reported intermittent photos requiring a forced refresh. A live mobile inspection found a concrete contributing issue: older gallery images had no intrinsic dimensions, and 15 of the 18 original 2023 images collapsed to zero-height boxes while waiting for lazy loading. All gallery photos also used their original files regardless of screen width. No permanently missing source file or browser console error was found during that inspection, so the original report is not attributed solely to a network failure.

All 89 unique local image files now have responsive, locally generated WebP previews: 339 files across widths up to 320, 640, 960, and 1600 pixels, without upscaling. Publication figures use lossless WebP. The approximately 640px preview set totals 5,030,674 bytes versus 31,358,170 bytes for the originals, an 84.0% reduction. Every rendered image has intrinsic dimensions, responsive sizes, and an original-file fallback. The original files remain unchanged and accessible from gallery image links. Every preview was decoded successfully and its checksum recorded in `data/image-variants.json`.

A failed preview gets one automatic retry against the original image using a fresh request URL. If that also fails, a “Retry photo” button lets the visitor retry without reloading the page. Actual local HTTP failures were simulated: automatic recovery succeeded, and manual recovery succeeded after the missing test file was restored. Test fixtures were removed before packaging. CSS and JavaScript URLs are content-versioned; responsive image filenames include a source/recipe fingerprint. These measures address the observed layout problem and reduce transfer size while providing recovery for transient failures; they do not claim that an unavailable connection can be made reliable by code.

The owner also requested improved captions. Sixty-nine photo captions were rewritten as concise descriptions grounded in the images, existing captions, and recorded locations. They are stored as editorial overrides in `data/photo-captions.json`; the original Google Sites and Unsplash caption records are unchanged. Biography, research information, publication facts, yearly upload chronology, and the 2023 essay/order remain unchanged.

All eight content routes passed 48 browser layout checks across three screen widths and both color themes, with no collapsed image boxes, missing responsive source attributes, horizontal overflow, or gallery error notices. Mobile scrolling loaded newly visible images normally. All 446 local files returned HTTP 200. See `migration/image-loading-checks.json` for the recovery tests and byte comparison.

## Compact gallery refinement

The owner requested less whitespace, no month separations, and a grid that fits mixed image orientations. All five full galleries now use balanced rows based on intrinsic image aspect ratios. Portrait and landscape photographs share an image height within each row, keep their original compositions, and remain in left-to-right reading order. Row widths recalculate when the container resizes; narrow screens prioritize readable image and caption widths. A CSS wrapping layout keeps the gallery usable without JavaScript. Full-size image links, responsive previews, image recovery, captions, and both themes are retained.

Month headings are removed from 2024 and 2025 while their verified timestamp ordering stays intact. The complete original 2023 essay now precedes the photos, with its opening night-sky photograph incorporated into the stargazing group. Its 18-image order and three original thematic headings remain intact. Header, narrative, image, and caption spacing have been reduced in photography pages; academic content and styling are unchanged.

All five galleries passed 30 browser layout checks across three widths and both themes, with no horizontal overflow, collapsed images, or visual-order reversals. Two initial observations caught in-flight lazy loads; settled rechecks found no pending visible photos or image-error notices. Browser warning/error logs were empty. The static checker validates the original galleries’ photo order as well as the 2024/2025 chronology and absence of month sections. See `migration/compact-gallery-checks.json`.
