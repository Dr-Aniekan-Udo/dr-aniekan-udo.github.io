# Project README Template

Use this template for all project repositories to enable enhanced parsing by the portfolio sync system.

## Required Fields

```markdown
# Project Name

**Category:** [Fullstack | AI & Agents | MLOps & Tools | Machine Learning | Data Science]
**Tech Stack:** Technology1, Technology2, Technology3
**Status:** [Active | Complete | Archived]
```

## Optional Fields

```markdown
**Thumbnail:** [assets/thumbnail.png]  ← Relative path to thumbnail image
**Live Demo:** [https://your-demo-url.com]
**License:** MIT
```

## Sections

### Overview
Write 2-3 sentences describing what the project does. This will be used as the project excerpt.

```markdown
## Overview

What this project does in 2-3 clear sentences...
```

### Features
List key features (optional).

```markdown
## Features

- Feature 1
- Feature 2
- Feature 3
```

### Screenshot
Include a screenshot for the project card thumbnail.

```markdown
## Screenshot

![Project Screenshot](assets/screenshot.png)
```

## Complete Example

```markdown
# GMC Analyst

**Category:** Fullstack
**Tech Stack:** Go, React, TypeScript, PostgreSQL
**Status:** Complete
**Thumbnail:** assets/thumbnail.png

## Overview

A fullstack web application for analyzing Global Management Challenge (GMC) competition data. Parse Excel reports, visualize financial and operational metrics, and simulate decision outcomes.

## Features

- Excel report parsing
- Financial metrics visualization
- Decision outcome simulation
- Real-time dashboard

## Screenshot

![GMC Analyst Dashboard](assets/screenshot.png)
```

## Thumbnail Guidelines

| Property | Recommendation |
|----------|---------------|
| **Size** | 1280×720px (16:9) |
| **Format** | PNG or JPG |
| **Location** | `thumbnail.png` in repo root OR `assets/thumbnail.png` |
| **Content** | Show the app interface, not just a logo |

## Category Options

Use one of these categories for consistency:
- `Fullstack`
- `AI & Agents`
- `MLOps & Tools`
- `Machine Learning`
- `Data Science`

## Notes

- The sync script searches for `thumbnail.{png,jpg}` in this priority:
  1. `thumbnail.png` (repo root)
  2. `assets/thumbnail.png`
  3. `images/thumbnail.png`
  4. `assets/preview.png`
  5. `screenshot.png`
  6. `banner.png`

- If no thumbnail is found, the project uses `default-thumbnail.svg`
- The **Overview** section (first 2-3 sentences) is used as the project description on the grid
- Keep the README concise; the full README is shown on the project detail page

## Adding Projects to Portfolio

After creating a project repo with this template:

1. Add the repo to `projects.yaml`:
```yaml
projects:
  - repo: Dr-Aniekan-Udo/your-project-repo
    category: "Fullstack"
    featured: true
    priority: 1
```

2. Run `npm run sync` to fetch the project
3. Push to GitHub — CI will auto-sync on the next build

---

**Questions?** Refer to `AGENTS.md` or open an issue.
