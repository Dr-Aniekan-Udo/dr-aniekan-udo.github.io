#!/usr/bin/env python3
"""
Portfolio Project Sync Script

Reads projects.yaml, fetches repo metadata and READMEs from GitHub,
downloads thumbnails, and generates Astro content collection files.

Run locally:
    python scripts/sync-projects.py

Or via npm:
    npm run sync
"""

import os
import re
import sys
import json
import yaml
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# Configuration
GITHUB_API_BASE = "https://api.github.com/repos"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"
CONTENT_DIR = Path("src/content/projects")
PUBLIC_PROJECTS_DIR = Path("public/projects")
PLACEHOLDER_IMAGE = "/default-thumbnail.svg"

# Common thumbnail paths to check in repos
THUMBNAIL_PATHS = [
    "thumbnail.png", "thumbnail.jpg", "thumbnail.jpeg",
    "assets/thumbnail.png", "assets/thumbnail.jpg",
    "images/thumbnail.png", "images/thumbnail.jpg",
    "assets/preview.png", "assets/preview.jpg",
    "docs/cover.png", "docs/cover.jpg",
    ".github/preview.png", ".github/preview.jpg",
    "screenshot.png", "screenshot.jpg",
    "banner.png", "banner.jpg",
]


def log(msg: str):
    print(f"[sync] {msg}")


def fetch_json(url: str, headers: dict = None) -> dict:
    """Fetch JSON from URL with optional headers."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        log(f"HTTP Error {e.code} for {url}: {e.reason}")
        return {}
    except Exception as e:
        log(f"Error fetching {url}: {e}")
        return {}


def fetch_text(url: str) -> str:
    """Fetch raw text from URL."""
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        log(f"Error fetching text {url}: {e}")
        return ""


def parse_readme_field(readme: str, field_name: str) -> str | None:
    """Extract a structured field from README using **Field:** pattern."""
    pattern = rf'\*\*{re.escape(field_name)}:\*\*\s*(.+)'
    match = re.search(pattern, readme, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def parse_tech_stack(readme: str) -> list[str]:
    """Extract tech stack as list from **Tech Stack:** field."""
    value = parse_readme_field(readme, "Tech Stack")
    if value:
        # Split by comma, and, or pipe
        techs = re.split(r'[,|]|\band\b', value)
        return [t.strip() for t in techs if t.strip()]
    return []


def parse_status(readme: str) -> str:
    """Extract status from **Status:** field."""
    value = parse_readme_field(readme, "Status")
    if value:
        valid = ["Active", "Complete", "Archived"]
        for v in valid:
            if v.lower() in value.lower():
                return v
    return "Unknown"


def parse_overview(readme: str, max_length: int = 300) -> str:
    """Extract overview from ## Overview section, fallback to first paragraph."""
    # Try ## Overview section first
    overview_match = re.search(
        r'##\s*Overview\s*\n+(.+?)(?=\n##|\Z)',
        readme, re.DOTALL | re.IGNORECASE
    )
    if overview_match:
        text = overview_match.group(1).strip()
        # Take first paragraph
        first_para = text.split('\n\n')[0] if '\n\n' in text else text.split('\n')[0]
        first_para = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', first_para)
        first_para = first_para.replace('"', "'")
        if len(first_para) > max_length:
            first_para = first_para[:max_length].rsplit(' ', 1)[0] + '...'
        return first_para
    
    # Fallback to old behavior
    return extract_excerpt(readme, max_length)


def parse_features(readme: str) -> list[str]:
    """Extract features from ## Features section."""
    features_match = re.search(
        r'##\s*Features\s*\n+(.+?)(?=\n##|\Z)',
        readme, re.DOTALL | re.IGNORECASE
    )
    if features_match:
        text = features_match.group(1)
        # Extract bullet points
        bullets = re.findall(r'^\s*[-*]\s+(.+)$', text, re.MULTILINE)
        return [b.strip() for b in bullets if b.strip()][:10]  # Max 10 features
    return []


def extract_excerpt(readme: str, max_length: int = 300) -> str:
    """Extract first meaningful paragraph from README."""
    # Remove HTML comments
    readme = re.sub(r'<!--.*?-->', '', readme, flags=re.DOTALL)
    # Remove HTML tags
    readme = re.sub(r'<[^>]+>', '', readme)
    # Remove markdown images
    readme = re.sub(r'!\[.*?\]\(.*?\)', '', readme)
    # Remove badges/shields
    readme = re.sub(r'\[?!\[.*?\]\(.*?\)\]?\(.*?\)', '', readme)
    # Find first non-empty line that's not a heading
    lines = readme.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('---') and len(line) > 20:
            # Clean markdown links
            line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', line)
            # Escape quotes for YAML
            line = line.replace('"', "'")
            if len(line) > max_length:
                line = line[:max_length].rsplit(' ', 1)[0] + '...'
            return line
    return "No description available."


def find_thumbnail(owner: str, repo: str) -> str | None:
    """Try to find a thumbnail image in the repo."""
    for path in THUMBNAIL_PATHS:
        url = f"{GITHUB_RAW_BASE}/{owner}/{repo}/main/{path}"
        try:
            req = urllib.request.Request(url, method='HEAD')
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    ext = Path(path).suffix
                    local_name = f"{owner}_{repo}{ext}"
                    local_path = PUBLIC_PROJECTS_DIR / local_name
                    # Download the image
                    urllib.request.urlretrieve(url, str(local_path))
                    log(f"Downloaded thumbnail: {local_name}")
                    return f"/projects/{local_name}"
        except Exception:
            continue
    return None


def yaml_string(value: str) -> str:
    """Format a string for safe YAML output."""
    if not value:
        return '""'
    # If contains special chars, use literal block
    if '"' in value or ':' in value or '\n' in value or value.startswith(' ') or value.endswith(' '):
        # Escape double quotes
        safe = value.replace('"', '\\"')
        return f'"{safe}"'
    return f'"{value}"'


def rewrite_image_paths(readme: str, owner: str, repo: str) -> str:
    """Rewrite relative image paths in README to absolute GitHub raw URLs."""
    base_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main"
    
    # Replace relative image paths like ./images/foo.png or images/foo.png
    def replace_path(match):
        prefix = match.group(1)  # ![alt]( or <img src="
        path = match.group(2)
        suffix = match.group(3)  # ) or "
        
        # Skip already absolute URLs
        if path.startswith('http://') or path.startswith('https://'):
            return match.group(0)
        
        # Remove leading ./
        clean_path = path.lstrip('./')
        return f'{prefix}{base_url}/{clean_path}{suffix}'
    
    # Markdown images: ![alt](./path/to/img.png)
    readme = re.sub(r'(!\[.*?\]\()(.*?)(\))', replace_path, readme)
    # HTML images: <img src="./path/to/img.png"
    readme = re.sub(r'(<img[^>]+src=")(.*?)((?:"|\'))', replace_path, readme)
    
    return readme


def slugify(text: str) -> str:
    """Convert repo name to URL slug."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def sync_projects():
    """Main sync function."""
    log("Starting project sync...")
    
    # Load config
    with open("projects.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    projects_config = config.get("projects", [])
    
    # Ensure directories exist
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    
    synced = 0
    for proj in projects_config:
        repo_full = proj["repo"]
        owner, repo = repo_full.split("/", 1)
        slug = slugify(repo)
        
        log(f"Processing {repo_full}...")
        
        # Fetch repo metadata
        meta_url = f"{GITHUB_API_BASE}/{repo_full}"
        meta = fetch_json(meta_url)
        
        # Fetch README
        readme_url = f"{GITHUB_RAW_BASE}/{repo_full}/main/README.md"
        readme = fetch_text(readme_url)
        if not readme:
            # Try master branch
            readme_url = f"{GITHUB_RAW_BASE}/{repo_full}/master/README.md"
            readme = fetch_text(readme_url)
        
        # Parse structured fields from README
        readme_category = parse_readme_field(readme, "Category") if readme else None
        tech_stack = parse_tech_stack(readme) if readme else []
        status = parse_status(readme) if readme else "Unknown"
        live_demo = parse_readme_field(readme, "Live Demo") if readme else None
        readme_thumbnail = parse_readme_field(readme, "Thumbnail") if readme else None
        
        # Extract overview/excerpt (prefers ## Overview section)
        excerpt = parse_overview(readme) if readme else "No README available."
        
        # Try to find thumbnail
        thumbnail = None
        # First check if README specifies a thumbnail path
        if readme_thumbnail:
            thumb_url = f"{GITHUB_RAW_BASE}/{owner}/{repo}/main/{readme_thumbnail.lstrip('./')}"
            try:
                req = urllib.request.Request(thumb_url, method='HEAD')
                with urllib.request.urlopen(req, timeout=5) as resp:
                    if resp.status == 200:
                        ext = Path(readme_thumbnail).suffix
                        local_name = f"{owner}_{repo}{ext}"
                        local_path = PUBLIC_PROJECTS_DIR / local_name
                        urllib.request.urlretrieve(thumb_url, str(local_path))
                        log(f"Downloaded README-specified thumbnail: {local_name}")
                        thumbnail = f"/projects/{local_name}"
            except Exception:
                pass
        
        # Fallback to path discovery
        if not thumbnail:
            thumbnail = find_thumbnail(owner, repo)
        
        if not thumbnail:
            thumbnail = PLACEHOLDER_IMAGE
            log(f"Using placeholder for {repo}")
        
        # Build frontmatter
        frontmatter = {
            "title": meta.get("name", repo).replace("-", " ").replace("_", " ").title(),
            "repo": repo_full,
            "category": readme_category or proj.get("category", "Uncategorized"),
            "description": meta.get("description", excerpt),
            "excerpt": excerpt,
            "thumbnail": thumbnail,
            "githubUrl": meta.get("html_url", f"https://github.com/{repo_full}"),
            "stars": meta.get("stargazers_count", 0),
            "language": meta.get("language", ""),
            "featured": proj.get("featured", False),
            "priority": proj.get("priority", 99),
            "tags": meta.get("topics", []),
            "techStack": tech_stack,
            "status": status,
            "liveDemo": live_demo,
            "features": parse_features(readme) if readme else [],
        }
        
        # Generate markdown file
        md_path = CONTENT_DIR / f"{slug}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            for key, value in frontmatter.items():
                if isinstance(value, list):
                    if len(value) == 0:
                        f.write(f"{key}: []\n")
                    else:
                        f.write(f"{key}:\n")
                        for item in value:
                            f.write(f"  - {yaml_string(item)}\n")
                elif isinstance(value, bool):
                    f.write(f"{key}: {str(value).lower()}\n")
                elif isinstance(value, int):
                    f.write(f"{key}: {value}\n")
                else:
                    f.write(f'{key}: {yaml_string(value)}\n')
            f.write("---\n\n")
            f.write(f"# {frontmatter['title']}\n\n")
            if readme:
                readme = rewrite_image_paths(readme, owner, repo)
                f.write(readme)
            else:
                f.write("No README content available.\n")
        
        synced += 1
        log(f"Synced: {md_path}")
    
    log(f"Done! Synced {synced} projects.")
    return synced


if __name__ == "__main__":
    try:
        count = sync_projects()
        sys.exit(0 if count > 0 else 1)
    except Exception as e:
        log(f"Fatal error: {e}")
        sys.exit(1)
