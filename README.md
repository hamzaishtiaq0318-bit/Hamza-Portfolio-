# Luzia - Portfolio Template — Extracted Site

> **Source:** https://luzia.framer.website/
> **Extracted:** September 2, 2026
> **Tool:** Framer Site Extractor Chrome Extension
> **Total files downloaded:** 244

---

## 📁 What's Inside

```
📁 your-site/
├── index.html              ← Homepage
├── styles.css              ← All CSS (keep at root level)
├── about/
│   └── index.html          ← /about page (multi-page sites)
├── work/
│   └── index.html          ← /work page (multi-page sites)
├── assets/
│   ├── js/                 ← Framer runtime + all JS chunks
│   ├── images/             ← All images (webp, jpg, png, svg…)
│   ├── fonts/              ← All fonts (woff2, woff…)
│   ├── videos/             ← All videos (mp4, webm…)
│   ├── cursors/            ← Custom cursor assets
│   └── cms/                ← CMS data (offline support)
└── README.md
```

⚡ **100% self-contained** — All assets are local files. No Framer subscription or internet needed once hosted.

---

## 🖥️ Run Locally (Preview on your computer)

> ⚠️ **Do NOT open index.html by double-clicking it.**
> Browsers block JavaScript modules on `file://` — you need a local server.

### Step 1 — Install Node.js (skip if you already have it)

Download from **https://nodejs.org** → choose the **LTS version** → install it.

To check if it's already installed, open Terminal and run:
```bash
node -v
```
If you see something like `v20.x.x` → you're good to go. ✅

### Step 2 — Open Terminal in this folder

**Mac:** Right-click the folder in Finder → **"New Terminal at Folder"**
**Windows:** Shift + Right-click the folder → **"Open PowerShell window here"**

### Step 3 — Start the local server

```bash
npx serve .
```

First time? It may ask:
> *"Need to install the following packages: serve — Ok to proceed? (y)"*

Type **y** and press **Enter**.

### Step 4 — Open your browser

Go to → **http://localhost:3000** 🎉

Your site is now running locally! All pages, animations, fonts, and videos will work exactly as expected.

---

## 🚀 Deploy to the Internet (Free Hosting)

### ⭐ Option 1 — Netlify (Easiest — No Terminal needed)

1. Go to **https://app.netlify.com/drop**
2. Drag and drop this **entire folder** onto the page
3. Wait ~10 seconds → your site is live with a public URL ✅

Want a custom domain? Go to **Site Settings → Domain Management** in Netlify.

---

### Option 2 — Vercel

**Via Terminal (fastest):**
```bash
npx vercel
```
Follow the prompts — your site is live in under a minute.

**Via Dashboard:**
1. Push this folder to a GitHub repo
2. Go to **https://vercel.com/new** → Import your repo
3. Click **Deploy** — no build settings needed ✅

---

### Option 3 — Render (Free Static Hosting)

1. Push this folder to a GitHub repo
2. Go to **https://render.com** → New → **Static Site**
3. Connect your GitHub repo
4. Set **Publish Directory** to: `.` (just a dot — the root)
5. Click **Create Static Site** ✅

---

### Option 4 — GitHub Pages (Great for portfolios)

1. Create a new repo at **https://github.com/new**
2. Upload all files from this folder to the repo root
3. Go to repo **Settings → Pages**
4. Source: **Deploy from branch** → main → / (root)
5. Save → your site is live at **https://yourusername.github.io/repo-name** ✅

---

### Option 5 — Cloudflare Pages (Fastest CDN, Free)

1. Go to **https://pages.cloudflare.com**
2. Connect GitHub → select your repo
3. Leave all build settings blank (it's a static site)
4. Click **Deploy** ✅ — auto-redeploys on every git push

---

## 🤖 Edit with AI Coding Tools (Vibe Coding)

Want to customise or modify this site using AI? It's just HTML, CSS, and JS — any AI tool can edit it.

### Claude Code

```bash
# Install Claude Code (one-time setup)
npm install -g @anthropic-ai/claude-code

# Navigate to this folder in Terminal
cd path/to/your-site

# Start Claude Code
claude
```

Then just describe what you want:
- *"Change the hero heading to say Welcome"*
- *"Make the primary colour dark blue"*
- *"Add a contact form at the bottom"*

### Cursor / Windsurf / Zed (AI Editors)

1. Open the extracted folder in the editor
2. Use the AI chat panel to describe your changes
3. Save → refresh **http://localhost:3000** to preview
4. Re-deploy when done

### VS Code + Copilot / Continue

1. **File → Open Folder** → select this folder
2. Edit `index.html`, `styles.css`, or any file directly
3. Use Copilot chat to make changes in plain English

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| **Blank page** | Use `npx serve .` — don't open index.html directly |
| **Images missing** | Re-extract on a faster connection (large sites may timeout) |
| **Sub-pages 404 locally** | Make sure you're in the right folder when running `npx serve .` |
| **Fonts look different** | Check browser settings — fonts are embedded locally and should match |
| **Netlify sub-pages 404** | Each page is a real file (e.g. `/work/index.html`) — no redirects config needed |
| **Slow to load locally** | Normal for large sites — all assets are local, just large files loading |

---

## ✅ What Was Done During Extraction

- ✅ All pages extracted — each page saved as its own HTML file
- ✅ All images, fonts, videos, and cursors downloaded locally
- ✅ All JS bundles downloaded with internal URLs rewritten
- ✅ CMS data chunks downloaded for offline support
- ✅ CSS extracted to `styles.css` at root level
- ✅ "Made with Framer" badge removed
- ✅ Analytics & tracking scripts removed
- ✅ Works on Netlify, Vercel, Render, GitHub Pages, Cloudflare Pages

---

*Generated by Framer Site Extractor Chrome Extension*
# Hamza-Portfolio-
