# Research README Template

Use this template for all research repositories to enable automatic parsing by the portfolio sync system.

## Required Fields

The following fields **must** be present for the sync script to work properly:

```markdown
# [Paper Title]

**Authors:** [Full author list separated by commas]  
**Venue:** [Conference or Workshop Name, Year]  
**arXiv:** [xxxx.xxxxx]  
**Date:** [Month Year]
```

## Optional Fields

```markdown
**Thumbnail:** [assets/thumbnail.jpg]  ← Relative path to thumbnail image
**DOI:** [10.xxxx/xxxxx]  ← Digital Object Identifier
**Code:** [github.com/username/repo]  ← Link to code repository
```

## Sections

### Abstract
Write a clear, concise abstract (2-4 paragraphs) describing the problem, approach, and key contributions.

```markdown
## Abstract

Your abstract text here...
```

### Methodology
Use a numbered list for methodology steps. These will be displayed as numbered cards on the site.

```markdown
## Methodology

1. First step description
2. Second step description
3. Third step description
```

### Results / Conclusion
Summarize your findings and conclusions.

```markdown
## Results / Conclusion

Your results text here...
```

### Keywords
Use backtick-separated keywords for automatic tag generation.

```markdown
## Keywords

`Keyword1` · `Keyword2` · `Keyword3`
```

## Complete Example

See the `glioma-segmentation-paper-README.md` file for a complete working example.

## Flexible Parsing Rules

The sync script handles missing fields gracefully:

| Missing Field | Behavior |
|--------------|----------|
| **Venue** | Shows "Preprint" or hides venue badge |
| **arXiv** | Hides arXiv button |
| **Date** | Hides date display |
| **Thumbnail** | Uses default research placeholder |
| **Methodology** | Hides methodology section |
| **Keywords** | Hides tags section |

## Notes

- Keep the `## Abstract`, `## Methodology`, `## Results / Conclusion`, and `## Keywords` section headers exactly as shown (case-insensitive)
- The script uses regex to extract information, so maintain the `**Field:** value` format
- Thumbnails should be 1200×630px (1.91:1 ratio) for best display
- Place thumbnail in `assets/` directory or specify custom path

## Adding Research to Portfolio

After creating a research repo with this template:

1. Add the repo to `data/research.yaml`:
```yaml
research:
  - repo: "Dr-Aniekan-Udo/your-research-repo"
    autoSync: true
    featured: true
    priority: 1
```

2. Run `npm run sync:content` to validate
3. Push to GitHub — CI will auto-sync the research paper

---

**Questions?** Refer to `AGENTS.md` or open an issue.
