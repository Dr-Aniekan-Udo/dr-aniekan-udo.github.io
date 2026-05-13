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

# Sync projects (requires Python + pyyaml)
python scripts/sync-projects.py

# Start dev server
npm run dev

# Build for production
npm run build
```

## Managing Projects

Edit `projects.yaml` to add, remove, or reorder projects. Push to `main` and GitHub Actions handles the rest.

## Architecture

- **Framework**: Astro 5.x (static output)
- **Styling**: Tailwind CSS 3.x
- **Automation**: Python 3 + PyYAML sync script
- **Hosting**: GitHub Pages
- **CI/CD**: GitHub Actions

## License

MIT
