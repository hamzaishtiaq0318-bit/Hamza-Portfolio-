"""
Static site builder for hamzaportfolio.dev.

Edit content in _src/ and run:   python _src/build.py
It regenerates every page (index.html, works/, about/, contact/, projects/*, 404.html)
plus sitemap.xml. Pages share one header/footer, so a change in a partial updates everything.

Template syntax (deliberately tiny):
  {{key}}         -> value from the page context (HTML-escaped unless the key ends with _html)
  {{> partial}}   -> contents of _src/partials/partial.html (rendered with the same context)
  {{i:name}}      -> inline SVG icon from ICONS below
"""
import html
import json
import re
from datetime import date
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
VERSION = "7"  # bump to bust browser caches for CSS/JS after changes

SITE = {
    "domain": "https://www.hamzaportfolio.dev",
    "name": "Hamza Ishtiaq",
    "email": "hamzaishtiaq2491@gmail.com",
    "cal_url": "https://cal.com/hamza-ishtiaq-03cjw0/bookacall",
    "linkedin": "https://www.linkedin.com/in/hamza-ishtiaq-56128b434/",
    "instagram": "https://www.instagram.com/hamza.isht/",
    "threads": "https://www.threads.com/@hamza.isht",
}

# ---------------------------------------------------------------- icons
_S = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICONS = {
    "arrow": f'<svg class="i-arrow" {_S}><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "arrow-up-right": f'<svg class="i-arrow-up" {_S}><path d="M7 17 17 7M8 7h9v9"/></svg>',
    "arrow-left": f'<svg {_S}><path d="M19 12H5M11 18l-6-6 6-6"/></svg>',
    "check": f'<svg {_S}><path d="M20 6 9 17l-5-5"/></svg>',
    "check-circle": f'<svg {_S}><circle cx="12" cy="12" r="9"/><path d="m8.5 12.5 2.3 2.3 4.7-5"/></svg>',
    "mail": f'<svg {_S}><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7.5 8 5.5 8-5.5"/></svg>',
    "calendar": f'<svg {_S}><rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M16 3v4M8 3v4M3.5 10h17"/></svg>',
    "clock": f'<svg {_S}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "lock": f'<svg {_S}><rect x="5" y="11" width="14" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>',
    "copy": f'<svg {_S}><rect x="9" y="9" width="11" height="11" rx="2.5"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/></svg>',
    "layers": f'<svg {_S}><path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/></svg>',
    "message": f'<svg {_S}><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/></svg>',
    "zap": f'<svg {_S}><path d="M13 3 5 13.5h6L10.5 21 19 10.5h-6L13 3Z"/></svg>',
    "life-buoy": f'<svg {_S}><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/><path d="m5.6 5.6 3.9 3.9M14.5 14.5l3.9 3.9M18.4 5.6l-3.9 3.9M9.5 14.5l-3.9 3.9"/></svg>',
    "briefcase": f'<svg {_S}><rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7M3 12.5h18"/></svg>',
    "bag": f'<svg {_S}><path d="M5 8h14l-1.2 11.1a2 2 0 0 1-2 1.9H8.2a2 2 0 0 1-2-1.9L5 8Z"/><path d="M9 10V7a3 3 0 0 1 6 0v3"/></svg>',
    "rocket": f'<svg {_S}><path d="M5 15c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.1 2.1 0 0 0-2.9-.1Z"/><path d="M12 15 9 12a15 15 0 0 1 9-9c1.7 0 3 1.3 3 3a15 15 0 0 1-9 9Z"/><path d="M9 12H5s.5-3 2-4c1.6-1.1 5 0 5 0M12 15v4s3-.5 4-2c1.1-1.6 0-5 0-5"/></svg>',
    "dashboard": f'<svg {_S}><rect x="3" y="3" width="7.5" height="9" rx="2"/><rect x="13.5" y="3" width="7.5" height="5" rx="2"/><rect x="13.5" y="11" width="7.5" height="10" rx="2"/><rect x="3" y="15" width="7.5" height="6" rx="2"/></svg>',
    "pen": f'<svg {_S}><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>',
    "refresh": f'<svg {_S}><path d="M3 12a9 9 0 0 1 15.3-6.4L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15.3 6.4L3 16"/><path d="M8 16H3v5"/></svg>',
    "smartphone": f'<svg {_S}><rect x="6" y="2.5" width="12" height="19" rx="3"/><path d="M11 18h2"/></svg>',
    "eye": f'<svg {_S}><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>',
    "code": f'<svg {_S}><path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/></svg>',
    "heart": f'<svg {_S}><path d="M19.5 12.6 12 20l-7.5-7.4A5 5 0 1 1 12 6a5 5 0 1 1 7.5 6.6Z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>',
    "threads": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.964-.065-1.19.408-2.285 1.33-3.082.88-.76 2.119-1.207 3.583-1.291a13.853 13.853 0 0 1 3.02.142c-.126-.742-.375-1.332-.75-1.757-.513-.586-1.308-.883-2.359-.89h-.029c-.844 0-1.992.232-2.721 1.32L7.734 7.847c.98-1.454 2.568-2.256 4.478-2.256h.044c3.194.02 5.097 1.975 5.287 5.388.108.046.216.094.321.142 1.49.7 2.58 1.761 3.154 3.07.797 1.82.871 4.79-1.548 7.158-1.85 1.81-4.094 2.628-7.277 2.65Zm1.003-11.69c-.242 0-.487.007-.739.021-1.836.103-2.98.946-2.916 2.143.067 1.256 1.452 1.839 2.784 1.767 1.224-.065 2.818-.543 3.086-3.71a10.5 10.5 0 0 0-2.215-.221z"/></svg>',
}

# ---------------------------------------------------------------- tech logos
TECH = {
    "shopify": ("Shopify", "shopify.svg"),
    "wordpress": ("WordPress", "wordpress-icon.svg"),
    "wix": ("Wix", "wix.svg"),
    "react": ("React", "react.svg"),
    "nodejs": ("Node.js", "nodejs-icon.svg"),
    "javascript": ("JavaScript", "javascript.svg"),
    "html": ("HTML5", "html-5.svg"),
    "css": ("CSS3", "css3.svg"),
    "vite": ("Vite", "vite.svg"),
    "firebase": ("Firebase", "firebase-icon.svg"),
    "google": ("Google Sign-In", "google-icon.svg"),
    "graphql": ("GraphQL", "graphql.svg"),
    "git": ("Git", "git-icon.svg"),
    "vscode": ("VS Code", "visual-studio-code.svg"),
}
WIDE_LOGOS = {"wix"}


def logo_img(key, alt=True, cls=""):
    name, file = TECH[key]
    klass = " ".join(c for c in [cls, "wide" if key in WIDE_LOGOS else ""] if c)
    klass_attr = f' class="{klass}"' if klass else ""
    alt_text = f"{name} logo" if alt else ""
    return f'<img src="/assets/images/logos/{file}" alt="{alt_text}" width="32" height="32"{klass_attr} loading="lazy">'


# ---------------------------------------------------------------- content blocks
FAQS = [
    ("What kind of websites do you build?",
     "Pretty much anything on the web: business websites, landing pages, online stores, portfolios, blogs and custom web apps like dashboards, booking systems and marketplaces. If it runs in a browser, I can build it."),
    ("Can you upgrade or redesign my existing Shopify, WordPress or Wix site?",
     "Yes, it's one of the things I do most. I can refresh or upgrade your theme, redesign pages, add new sections and features, and fix speed or mobile issues, all without losing your existing content."),
    ("How long does a project take?",
     "It depends on the size and features. Most websites take between one and four weeks, and larger stores or custom web apps can take longer. After our first call I'll give you a clear timeline, so you know exactly when to expect each part."),
    ("How much does a website cost?",
     "Every project is different, so I price based on what you actually need. After a quick chat about your goals I'll send you a clear quote up front, with no hidden costs."),
    ("What do you need from me to get started?",
     "Just your idea and whatever you already have: logo, text, photos or examples of websites you like. Don't worry if you don't have everything ready. I'll help you figure out the rest."),
    ("Will my website work on mobile phones?",
     "Always. Every website I build is fully responsive and tested on phones, tablets and desktops, so it looks and works great for every visitor."),
    ("Do you offer support after the website is live?",
     "Yes. You get one month of free support after launch for questions, small tweaks and fixes. After that, I'm happy to keep helping with updates whenever you need me."),
]

STEPS = [
    ("Free intro call", "We start with a relaxed conversation. Tell me about your business, your goals and what you have in mind, and I'll suggest the best way to get there."),
    ("Plan & quote", "I send you a clear plan covering the pages, features, timeline and price. You'll know exactly what you're getting before any work begins."),
    ("Design & build", "I design and develop your website and share progress along the way, so you can give feedback before anything goes live."),
    ("Test & launch", "I test everything on phones, tablets and desktops, then launch your site and show you how to manage it yourself."),
    ("Ongoing support", "You get one month of free support after launch. If something needs a tweak, I've got you covered."),
]

PRINCIPLES = [
    ("message", "Clear communication", "Plain language, regular updates and quick replies. You'll never have to wonder what's happening with your project."),
    ("smartphone", "Mobile-first", "Most of your visitors are on their phones, so I design for small screens first and scale up from there."),
    ("zap", "Speed matters", "Optimised images, clean code and smart loading, because a slow website loses customers."),
    ("heart", "Built to last", "Tidy, well-organised code and sites you can update yourself, long after I've handed them over."),
]

BUILDS = [
    ("briefcase", "Business websites", "Professional websites that explain what you do and turn visitors into enquiries."),
    ("bag", "Online stores", "Shopify stores that look premium, load fast and make buying easy on any device."),
    ("rocket", "Landing pages", "Focused, high-converting pages for launches, campaigns and new products."),
    ("dashboard", "Web apps & dashboards", "Custom platforms with logins, real-time data and the features your business needs."),
    ("pen", "Portfolios & blogs", "Clean, personal sites that showcase your work and are easy to keep updated."),
    ("refresh", "Redesigns & upgrades", "Fresh themes, new sections and speed fixes for Shopify, WordPress and Wix sites."),
]

TOOLKIT = [
    ("shopify", "Store builds, theme customisation and custom sections", True),
    ("wordpress", "Custom themes, redesigns and plugin setup", True),
    ("wix", "Site redesigns, custom pages and landing pages", True),
    ("react", "Fast, interactive interfaces and web apps", False),
    ("nodejs", "Back-ends, APIs and server-side logic", False),
    ("javascript", "The language behind everything I build", False),
    ("html", "Clean, accessible and SEO-friendly markup", False),
    ("css", "Responsive layouts and smooth animations", False),
    ("firebase", "Logins, databases and real-time features", False),
    ("vite", "Lightning-fast builds for modern front-ends", False),
    ("graphql", "Flexible APIs for data-heavy applications", False),
    ("git", "Version control on every single project", False),
]

TOOLS = ["shopify", "wordpress", "wix", "react", "nodejs", "firebase"]


# ---------------------------------------------------------------- template engine
def load(rel):
    return (SRC / rel).read_text(encoding="utf-8")


def render(tpl, ctx, depth=0):
    if depth > 8:
        raise RecursionError("partials nested too deep")

    def partial(m):
        return render(load(f"partials/{m.group(1)}.html"), ctx, depth + 1)

    tpl = re.sub(r"\{\{>\s*([\w-]+)\s*\}\}", partial, tpl)

    def icon(m):
        name = m.group(1)
        if name not in ICONS:
            raise KeyError(f"unknown icon: {name}")
        return ICONS[name]

    tpl = re.sub(r"\{\{i:([\w-]+)\}\}", icon, tpl)

    def var(m):
        key = m.group(1)
        if key not in ctx:
            raise KeyError(f"missing template value: {key}")
        val = str(ctx[key])
        return val if key.endswith("_html") else html.escape(val, quote=True)

    return re.sub(r"\{\{\s*([\w]+)\s*\}\}", var, tpl)


def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- generated fragments
def browser(domain, src, srcset, sizes, alt, eager=False, width=1280, height=800):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (
        '<div class="browser">'
        f'<div class="browser__bar"><i></i><i></i><i></i><div class="browser__url">{ICONS["lock"]}<span>{esc(domain)}</span></div></div>'
        f'<div class="browser__screen"><img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{width}" height="{height}" alt="{esc(alt)}" {loading} decoding="async"></div>'
        "</div>"
    )


def shot(p, sizes, eager=False):
    base = f"/assets/images/projects/{p['slug']}"
    return browser(
        p["domain"], f"{base}.webp", f"{base}-640.webp 640w, {base}.webp 1280w", sizes,
        f"Screenshot of the {p['name']} website", eager,
    )


def chips(tags, extra_cls=""):
    cls = f"chip {extra_cls}".strip()
    return "".join(f'<span class="{cls}">{esc(t)}</span>' for t in tags)


def featured_cards(projects):
    """Media-first cards: the first project is shown wide, the rest in a 2-column grid."""
    out = []
    for n, p in enumerate(projects):
        wide = n == 0
        classes = "work-card" + (" work-card--wide" if wide else "") + (" work-card--dark" if p.get("card") == "dark" else "")
        new = ' <span class="badge-new">New</span>' if p["year"] >= 2026 else ""
        sizes = "(max-width: 760px) 90vw, 880px" if wide else "(max-width: 760px) 90vw, 480px"
        delay = 0 if wide else ((n - 1) % 2) * 100
        out.append(
            f'<a class="{classes}" href="/projects/{p["slug"]}/" data-reveal style="--tint:{p["tint"]};--d:{delay}ms">'
            f'<div class="work-card__media">{shot(p, sizes)}'
            f'<span class="work-card__cta">View project {ICONS["arrow-up-right"]}</span></div>'
            '<div class="work-card__info">'
            f'<div><h3 class="work-card__title">{esc(p["name"])}{new}</h3>'
            f'<p class="work-card__summary">{esc(p["summary"])}</p></div>'
            f'<div class="work-card__side"><strong>{p["year"]}</strong><span>{esc(p["type"])}</span></div>'
            "</div></a>"
        )
    return "\n".join(out)


def works_rows(projects):
    out = []
    for n, p in enumerate(projects):
        base = f"/assets/images/projects/{p['slug']}"
        out.append(
            f'<a class="index-row" href="/projects/{p["slug"]}/" data-category="{p["category"]}" '
            f'data-preview="{base}-640.webp" data-domain="{esc(p["domain"])}" data-reveal style="--d:{n * 60}ms">'
            f'<span class="index-row__num">{n + 1:02d}</span>'
            f'<span class="index-row__thumb"><img src="{base}-640.webp" width="640" height="400" alt="" loading="lazy"></span>'
            f'<span class="index-row__title"><span class="index-row__name">{esc(p["name"])}</span>'
            f'<span class="index-row__summary">{esc(p["summary"])}</span></span>'
            f'<span class="chips">{chips(p["tags"][:2], "chip--soft")}</span>'
            f'<span class="index-row__year">{p["year"]}</span>'
            f'<span class="arrow-circle">{ICONS["arrow"]}</span>'
            "</a>"
        )
    return "\n".join(out)


def faq_items(faqs):
    return "\n".join(
        f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{esc(q)}<span class="faq-item__icon" aria-hidden="true"></span></summary>'
        f'<div class="faq-item__answer"><p>{esc(a)}</p></div></details>'
        for i, (q, a) in enumerate(faqs)
    )


def steps_html(steps):
    return "\n".join(
        f'<li class="step" data-reveal><span class="step__num">{i + 1}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></li>'
        for i, (t, d) in enumerate(steps)
    )


def principles_html():
    return "\n".join(
        f'<li class="step" data-reveal style="--d:{i * 70}ms"><span class="step__num">{ICONS[ic]}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></li>'
        for i, (ic, t, d) in enumerate(PRINCIPLES)
    )


def builds_html():
    return "\n".join(
        f'<div class="info-card" data-reveal style="--d:{(i % 3) * 70}ms"><span class="tile__icon">{ICONS[ic]}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for i, (ic, t, d) in enumerate(BUILDS)
    )


def toolkit_html():
    out = []
    for i, (key, desc, featured) in enumerate(TOOLKIT):
        name = TECH[key][0]
        out.append(
            f'<div class="stack-item{" stack-item--featured" if featured else ""}" data-reveal style="--d:{(i % 3) * 60}ms">'
            f'<span class="stack-item__logo">{logo_img(key)}</span>'
            f'<div><h3>{esc(name)}</h3><p>{esc(desc)}</p></div></div>'
        )
    return "\n".join(out)


def tools_html():
    items = []
    for k in TOOLS:
        if k in WIDE_LOGOS:  # wordmark logos (Wix) already spell the name
            items.append(f'<li class="tool">{logo_img(k)}</li>')
        else:
            items.append(f'<li class="tool">{logo_img(k, alt=False)}<span>{esc(TECH[k][0])}</span></li>')
    return f'<ul class="tools__list">{"".join(items)}</ul>'


def stack_html(p):
    out = []
    for key in p["stack"]:
        name = TECH[key][0]
        out.append(f'<span class="tech"><span class="tech__logo">{logo_img(key, alt=False)}</span>{esc(name)}</span>')
    return "".join(out)


def features_html(p):
    return "\n".join(
        f'<div class="feature" data-reveal style="--d:{(i % 3) * 70}ms"><span class="feature__num">{i + 1:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for i, (t, d) in enumerate(p["features"])
    )


def more_projects_html(others):
    return "".join(
        f'<a href="/projects/{p["slug"]}/"><img src="/assets/images/projects/{p["slug"]}-640.webp" width="640" height="400" alt="" loading="lazy">'
        f'<span>{esc(p["name"])} <small>{p["year"]}</small></span></a>'
        for p in others
    )


def person_jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": SITE["name"],
        "jobTitle": "Full-Stack Web Developer",
        "url": SITE["domain"] + "/",
        "email": "mailto:" + SITE["email"],
        "image": SITE["domain"] + "/assets/images/hamza-about.webp",
        "sameAs": [SITE["linkedin"], SITE["instagram"], SITE["threads"]],
        "knowsAbout": ["Web development", "Shopify", "WordPress", "Wix", "React", "Node.js", "JavaScript"],
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS
        ],
    }
    return (
        f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>'
    )


# ---------------------------------------------------------------- page assembly
def base_ctx(path, title, description, current, og_image=None, og_alt=None, og_type="website", extra_head_html=""):
    ctx = dict(SITE)
    ctx.update(
        title=title,
        description=description,
        canonical=SITE["domain"] + path,
        version=VERSION,
        og_type=og_type,
        og_image=og_image or f"{SITE['domain']}/assets/images/og-preview.png?v={VERSION}",
        og_image_type="image/jpeg" if (og_image or "").split("?")[0].endswith(".jpg") else "image/png",
        og_alt=og_alt or "Hamza Ishtiaq, full-stack web developer",
        extra_head_html=extra_head_html,
    )
    for key in ("home", "works", "about", "contact"):
        ctx[f"cur_{key}_html"] = ' aria-current="page"' if current == key else ""
    return ctx


def write(rel, content):
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8", newline="\n")
    print("  wrote", rel)


def build_page(rel_out, page_tpl, ctx):
    ctx = dict(ctx)
    ctx["content_html"] = render(load(page_tpl), ctx)
    write(rel_out, render(load("layout.html"), ctx))


def main():
    projects = json.loads(load("projects.json"))
    print("Building site...")

    shared = dict(
        featured_cards_html=featured_cards(projects),
        works_rows_html=works_rows(projects),
        faq_items_html=faq_items(FAQS),
        steps_html=steps_html(STEPS),
        principles_html=principles_html(),
        builds_html=builds_html(),
        toolkit_html=toolkit_html(),
        tools_html=tools_html(),
        project_count=str(len(projects)),
        app_count=str(sum(p["category"] == "app" for p in projects)),
        store_count=str(sum(p["category"] == "store" for p in projects)),
        first_preview=f"/assets/images/projects/{projects[0]['slug']}-640.webp",
    )

    pages = [
        ("index.html", "pages/home.html", "/", "home",
         "Hamza Ishtiaq | Full-Stack Web Developer",
         "I'm Hamza, a full-stack web developer. I build custom websites, web apps and Shopify stores, and upgrade WordPress, Wix and Shopify themes so they look modern and load fast.",
         person_jsonld()),
        ("works/index.html", "pages/works.html", "/works/", "works",
         "Work | Hamza Ishtiaq",
         "Selected projects by Hamza Ishtiaq: a creator studio and store, SaaS and healthcare web apps, and premium Shopify stores.", ""),
        ("about/index.html", "pages/about.html", "/about/", "about",
         "About | Hamza Ishtiaq",
         "Hi, I'm Hamza, a full-stack web developer who builds websites, web apps and online stores, and upgrades Shopify, WordPress and Wix sites.", ""),
        ("contact/index.html", "pages/contact.html", "/contact/", "contact",
         "Contact | Hamza Ishtiaq",
         "Have a project in mind? Send me a message or book a free call, and let's talk about your new website, online store or redesign.", ""),
        ("404.html", "pages/404.html", "/404.html", "",
         "Page not found | Hamza Ishtiaq",
         "This page doesn't exist. Head back to the homepage or see my latest work.", '<meta name="robots" content="noindex">'),
    ]
    for rel_out, tpl, path, current, title, desc, extra in pages:
        ctx = base_ctx(path, title, desc, current, extra_head_html=extra)
        ctx.update(shared)
        build_page(rel_out, tpl, ctx)

    for i, p in enumerate(projects):
        nxt = projects[(i + 1) % len(projects)]
        others = [q for q in projects if q["slug"] not in (p["slug"], nxt["slug"])]
        ctx = base_ctx(
            f"/projects/{p['slug']}/",
            f"{p['name']} | Project by Hamza Ishtiaq",
            f"{p['summary']} A {p['type'].lower()} designed and built by Hamza Ishtiaq in {p['year']}.",
            "works",
            og_image=f"{SITE['domain']}/assets/images/og/{p['slug']}.jpg?v={VERSION}",
            og_alt=f"{p['name']} website by Hamza Ishtiaq",
            og_type="article",
        )
        ctx.update(shared)
        ctx.update(
            num=f"{i + 1:02d}",
            name=p["name"], year=str(p["year"]), url=p["url"], domain=p["domain"], type=p["type"],
            role=p["role"], platform=p["platform"], summary=p["summary"], tint=p["tint"],
            shot_html=shot(p, "(max-width: 1280px) 94vw, 1200px", eager=True),
            overview_html="".join(f"<p>{esc(t)}</p>" for t in p["overview"]),
            features_html=features_html(p),
            stack_html=stack_html(p),
            tags_html=chips(p["tags"]),
            cta_text=(
                "I build and customise Shopify stores that look premium and make buying easy. Tell me about your store and let's make it shine."
                if p["category"] == "store"
                else "I build custom web apps and platforms that are fast, secure and easy to use. Tell me about your idea and let's make it real."
            ),
            next_slug=nxt["slug"], next_name=nxt["name"], next_type=nxt["type"], next_year=str(nxt["year"]),
            next_shot_html=shot(nxt, "(max-width: 760px) 92vw, 600px"),
            more_html=more_projects_html(others),
        )
        build_page(f"projects/{p['slug']}/index.html", "templates/project.html", ctx)

    # sitemap
    today = date.today().isoformat()
    urls = [("/", "1.0", "weekly"), ("/works/", "0.9", "weekly"), ("/about/", "0.8", "monthly"), ("/contact/", "0.8", "monthly")]
    urls += [(f"/projects/{p['slug']}/", "0.7", "monthly") for p in projects]
    body = "\n".join(
        f"  <url>\n    <loc>{SITE['domain']}{u}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{f}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
        for u, pr, f in urls
    )
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n')
    print("Done.")


if __name__ == "__main__":
    main()
