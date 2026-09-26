# hamzaportfolio.dev

Personal portfolio of **Hamza Ishtiaq**, full-stack web developer.

A fast, hand-built static site with no framework and no dependencies. It's plain HTML, one stylesheet and one small script, and it works on any static host.

## Structure

```
index.html, works/, about/, contact/, projects/<slug>/, 404.html   ← generated pages (don't edit by hand)
assets/css/site.css     ← all styles (design tokens at the top)
assets/js/site.js       ← menu, scroll reveals, works filter/preview, Cal.com modal, contact form
assets/images/          ← photos, project screenshots, logos, link-preview images
_src/                   ← the source you edit
  projects.json         ← every project: name, year, links, description, features, tech
  pages/*.html          ← page content (home, works, about, contact, 404)
  templates/project.html← layout shared by all project pages
  partials/*.html       ← <head>, header and footer shared by every page
  build.py              ← generates the pages + sitemap.xml
  og.html               ← source for assets/images/og-preview.png (link preview)
```

## Editing

1. Change content in `_src/` (e.g. add a project to `_src/projects.json`).
2. Run `python _src/build.py`.
3. Commit the regenerated files and push.

To add a project, add an entry to `projects.json`, then add screenshots to `assets/images/projects/`: `<slug>.webp` at 1280×800 and `<slug>-640.webp` at 640×400. Add a share image at `assets/images/og/<slug>.jpg` (1200×630). It then shows up on the Home page, the Work page, the sitemap and its own case-study page.

## Services used

- **Contact form:** [FormSubmit](https://formsubmit.co) → hamzaishtiaq2491@gmail.com
- **Booking:** [Cal.com](https://cal.com/hamza-ishtiaq-03cjw0/bookacall), which opens as a pop-up

Always save files as UTF-8. Don't round-trip them through Windows PowerShell's `Get-Content`/`Set-Content`, which corrupts characters like `’` and `©`.
