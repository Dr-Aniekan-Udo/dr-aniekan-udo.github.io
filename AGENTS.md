# AGENTS.md — Aniekan Udo Portfolio

## Project Overview

This is the automated portfolio site for **Aniekan Udo**, a software engineer specializing in Data, AI, Fullstack, MLOps, and Automation. The site is built with Astro, styled with Tailwind CSS, and deployed to GitHub Pages via GitHub Actions.

**Key feature:** Projects are automatically synced from GitHub repos listed in `projects.yaml`. The CI pipeline fetches READMEs, thumbnails, and metadata at build time.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Astro 5.x (static output) |
| Styling | Tailwind CSS 3.x |
| Fonts | Inter (body), Fira Code (mono) |
| CI/CD | GitHub Actions |
| Hosting | GitHub Pages |
| Automation | Python 3 + PyYAML (runs in isolated venv) |
| Package Manager | uv (Python), npm (Node) |

## Project Structure

```
.
├── .github/workflows/build-and-deploy.yml  # CI/CD pipeline
├── .venv/                                  # Python virtual environment (not committed)
├── scripts/
│   ├── sync-projects.py                    # Fetches repo data from GitHub
│   └── requirements.txt                    # Python dependencies (pyyaml)
├── projects.yaml                           # Single source of truth for showcased repos
├── src/
│   ├── content/config.ts                   # Astro content collections schema
│   ├── content/projects/                   # Generated at build time (*.md)
│   ├── components/                         # Astro UI components
│   ├── layouts/BaseLayout.astro            # Root HTML shell + animations
│   ├── pages/
│   │   ├── index.astro                     # Landing page
│   │   └── projects/[slug].astro           # Dynamic project detail pages
│   └── styles/global.css                   # Tailwind directives + custom utilities
├── public/
│   ├── profile.jpg                         # Author headshot
│   ├── default-thumbnail.svg               # Fallback for repos without images
│   └── projects/                           # Downloaded repo thumbnails
├── astro.config.mjs
├── tailwind.config.mjs
├── package.json
└── tsconfig.json
```

## Development Workflow

### Prerequisites

- **Node.js** 18+ and **npm**
- **Python** 3.10+ and **uv** (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Initial Setup

```bash
# 1. Install Node dependencies
npm install

# 2. Create Python virtual environment and install deps
uv venv .venv --python 3.12
uv pip install -r scripts/requirements.txt --python .venv\Scripts\python.exe

# 3. Sync projects (generates src/content/projects/*.md)
npm run sync

# 4. Start dev server (localhost:4321)
npm run dev
```

### Daily Development

```bash
# Sync projects (uses .venv python automatically)
npm run sync

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Python Environment Isolation

**Important:** The sync script always runs inside the `.venv` virtual environment to avoid polluting your system Python.

- **Windows:** `.venv\Scripts\python.exe`
- **Linux/macOS:** `.venv/bin/python`

The `npm run sync` command is pre-configured to use the correct path on Windows. On CI (GitHub Actions), it uses the Linux path automatically.

### Adding/Removing Projects

Edit `projects.yaml`:

```yaml
projects:
  - repo: Dr-Aniekan-Udo/your-new-repo
    category: "Fullstack"
    featured: true      # optional: highlights on grid
    priority: 1         # optional: sort order (lower = first)
```

Push to `main`. GitHub Actions will:
1. Create a fresh Python venv and install deps
2. Run `sync-projects.py` to fetch READMEs and thumbnails
3. Build the Astro site
4. Deploy to GitHub Pages

### Project Categories

Use one of these categories for consistency:
- `Fullstack`
- `AI & Agents`
- `MLOps & Tools`
- `Machine Learning`
- `Data Science`

## Design System

### Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `dark` | `#0a0a0a` | Page background |
| `dark-surface` | `#141414` | Cards, sections |
| `dark-elevated` | `#1a1a1a` | Hover states, badges |
| `amber` | `#f59e0b` | Primary accent, links, CTAs |
| `amber-hover` | `#d97706` | Button hover |
| `text-primary` | `#e5e5e5` | Headings |
| `text-secondary` | `#a3a3a3` | Body text |
| `text-muted` | `#737373` | Captions, labels |
| `border` | `#262626` | Dividers, card borders |

### Animation

- **Scroll reveals:** `.reveal` class + IntersectionObserver (0.6s ease-out)
- **Stagger grids:** `.stagger-children` class (100ms increments)
- **Hover effects:** Cards lift `-translate-y-1`, border shifts to `amber/50`
- **Page transitions:** Native CSS view transitions (Astro handles this)

## Automation Details

### `sync-projects.py`

1. Reads `projects.yaml`
2. For each repo:
   - Fetches GitHub API metadata (stars, language, topics, description)
   - Fetches `README.md` from `main` branch (falls back to `master`)
   - Extracts first paragraph as excerpt
   - Rewrites relative image paths to absolute GitHub raw URLs
   - Searches for thumbnail in common paths (`assets/`, `images/`, `.github/`, etc.)
   - Falls back to `public/default-thumbnail.svg`
3. Generates `src/content/projects/{slug}.md` with frontmatter + full README

### Thumbnail Discovery Priority

1. `thumbnail.{png,jpg}` (repo root)
2. `assets/thumbnail.{png,jpg}`
3. `images/thumbnail.{png,jpg}`
4. `assets/preview.{png,jpg}`
5. `docs/cover.{png,jpg}`
6. `.github/preview.{png,jpg}`
7. `screenshot.{png,jpg}`
8. `banner.{png,jpg}`

If none found → `default-thumbnail.svg`

## Troubleshooting

### Build fails locally

```bash
# Ensure venv exists and has deps
uv venv .venv --python 3.12
uv pip install -r scripts/requirements.txt --python .venv\Scripts\python.exe

# Then sync
npm run sync
```

### Build fails on GitHub Actions

- Check `projects.yaml` syntax is valid
- Ensure repos in whitelist are public
- Verify `GITHUB_TOKEN` has sufficient permissions (read repos)

### Thumbnails not appearing

- Add a `thumbnail.png` or `thumbnail.jpg` to the repo root or `assets/` folder
- Or set a custom path in `projects.yaml` (future enhancement)

### Local dev errors

- Run `npm run sync` first — Astro content collections need the `.md` files
- Ensure Node 18+ and Python 3.10+ are installed
- Ensure `.venv` exists with `pyyaml` installed

## Contact

Maintained by Aniekan Udo. For issues, open a GitHub issue or email aniekanetimudo@gmail.com.
