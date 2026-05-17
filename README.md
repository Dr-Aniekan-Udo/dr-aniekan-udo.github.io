# Aniekan Udo Portfolio

A modern, automated portfolio site built with Astro and Tailwind CSS.

## Features

- **Automated Project Sync**: Projects are fetched from GitHub repos listed in `projects.yaml`
- **Dark Theme**: Premium amber-on-black design inspired by top engineering portfolios
- **Dynamic Project Pages**: Each project gets its own detail page with README rendering
- **GitHub Actions CI/CD**: Automatic build and deploy to GitHub Pages on every push

## Quick Start

```bash
# Install dependencies
npm install

# Sync content from YAML configs
npm run sync:content

# Sync projects from GitHub
npm run sync

# Sync research papers
npm run sync:research

# Start dev server
npm run dev

# Build for production
npm run build
```

## Managing Projects

Edit `projects.yaml` to add, remove, or reorder projects. Push to `main` and GitHub Actions handles the rest.

## Automated Builds

The site rebuilds automatically:
- **On every push to `main`**
- **Monthly**: 1st of every month at midnight UTC (syncs latest repo data)
- **Manual trigger**: Go to Actions tab → "Build and Deploy" → "Run workflow"

### Manual Build Trigger

You can trigger a build manually anytime:

**Via GitHub UI:**
1. Go to repository → Actions tab
2. Select "Build and Deploy" workflow
3. Click "Run workflow" → "Run workflow"

**Via GitHub CLI:**
```bash
gh workflow run build-and-deploy.yml
```

**Via API (requires token):**
```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/Dr-Aniekan-Udo/dr-aniekan-udo.github.io/actions/workflows/build-and-deploy.yml/dispatches \
  -d '{"ref":"main"}'
```

## Architecture

- **Framework**: Astro 5.x (static output)
- **Styling**: Tailwind CSS 3.x
- **Automation**: Python 3 + PyYAML sync script
- **Hosting**: GitHub Pages
- **CI/CD**: GitHub Actions

## License

MIT
