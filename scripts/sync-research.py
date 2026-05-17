#!/usr/bin/env python3
"""
Research Sync Script

Reads research entries from data/research.yaml, fetches READMEs from GitHub repos,
parses structured research content, and generates Astro content collection files.

Usage:
    python scripts/sync-research.py
"""

import os
import re
import sys
import yaml
import urllib.request
from pathlib import Path
from datetime import datetime

# Configuration
DATA_DIR = Path("data")
OUTPUT_DIR = Path("src/content/research")
PUBLIC_RESEARCH_DIR = Path("public/research")
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"


def log(msg: str):
    print(f"[research-sync] {msg}")


def load_yaml(filename: str) -> dict:
    """Load and parse a YAML file."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        log(f"WARNING: {filepath} not found")
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}
    except Exception as e:
        log(f"ERROR loading {filepath}: {e}")
        return {}


def fetch_readme(repo: str) -> str:
    """Fetch README.md from a GitHub repo."""
    # Try main branch first
    url = f"{GITHUB_RAW_BASE}/{repo}/main/README.md"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception:
        # Fallback to master branch
        url = f"{GITHUB_RAW_BASE}/{repo}/master/README.md"
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                return resp.read().decode('utf-8', errors='ignore')
        except Exception as e:
            log(f"ERROR fetching README for {repo}: {e}")
            return ""


def extract_field(readme: str, field: str) -> str:
    """Extract a field from README frontmatter (e.g., **Authors:** value)."""
    pattern = rf'\*\*{re.escape(field)}:\*\*\s*(.+?)(?:\n|$)'
    match = re.search(pattern, readme, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def extract_section(readme: str, section_name: str) -> str:
    """Extract content from a markdown section."""
    pattern = rf'##\s*{re.escape(section_name)}\s*\n(.*?)(?=\n##|\Z)'
    match = re.search(pattern, readme, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_methodology(section: str) -> list:
    """Parse numbered list from methodology section."""
    steps = []
    for line in section.split('\n'):
        line = line.strip()
        if re.match(r'^\d+\.\s+', line):
            step = re.sub(r'^\d+\.\s*', '', line)
            if step:
                steps.append(step)
    return steps


def parse_keywords(section: str) -> list:
    """Parse backtick-separated keywords."""
    keywords = re.findall(r'`([^`]+)`', section)
    return keywords


def download_thumbnail(repo: str, thumbnail_path: str) -> str:
    """Download thumbnail image from repo. Returns local path or empty string."""
    if not thumbnail_path:
        return ""
    
    url = f"{GITHUB_RAW_BASE}/{repo}/main/{thumbnail_path}"
    filename = Path(thumbnail_path).name
    local_path = PUBLIC_RESEARCH_DIR / filename
    
    try:
        urllib.request.urlretrieve(url, str(local_path))
        log(f"Downloaded thumbnail: {filename}")
        return f"/research/{filename}"
    except Exception:
        # Try master branch
        url = f"{GITHUB_RAW_BASE}/{repo}/master/{thumbnail_path}"
        try:
            urllib.request.urlretrieve(url, str(local_path))
            log(f"Downloaded thumbnail: {filename}")
            return f"/research/{filename}"
        except Exception as e:
            log(f"WARNING: Could not download thumbnail for {repo}: {e}")
            return ""


def slugify(text: str) -> str:
    """Convert title to URL-friendly slug."""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')


def generate_research_md(entry: dict, parsed_data: dict) -> str:
    """Generate a markdown file for a research paper."""
    
    # Build frontmatter
    frontmatter = {
        "title": parsed_data.get("title", entry.get("title", "Untitled Research")),
        "authors": parsed_data.get("authors", entry.get("authors", "")),
        "venue": parsed_data.get("venue", entry.get("venue", "")),
        "arxiv": parsed_data.get("arxiv", entry.get("arxiv", "")),
        "date": parsed_data.get("date", entry.get("date", "")),
        "abstract": parsed_data.get("abstract", entry.get("abstract", "")),
        "methodology": parsed_data.get("methodology", entry.get("methodology", [])),
        "conclusion": parsed_data.get("conclusion", entry.get("conclusion", "")),
        "tags": parsed_data.get("tags", entry.get("tags", [])),
        "thumbnail": parsed_data.get("thumbnail", entry.get("thumbnail", "/default-thumbnail.svg")),
        "repo": entry.get("repo", ""),
        "featured": entry.get("featured", False),
        "priority": entry.get("priority", 99),
    }
    
    # Generate markdown content
    md = "---\n"
    for key, value in frontmatter.items():
        if isinstance(value, list):
            if not value:
                md += f"{key}: []\n"
            else:
                md += f"{key}:\n"
                for item in value:
                    md += f"  - \"{item}\"\n"
        elif isinstance(value, bool):
            md += f"{key}: {str(value).lower()}\n"
        elif isinstance(value, int):
            md += f"{key}: {value}\n"
        else:
            escaped = str(value).replace('"', '\\"')
            md += f'{key}: "{escaped}"\n'
    md += "---\n\n"
    
    # Add body content
    if frontmatter["abstract"]:
        md += f"{frontmatter['abstract']}\n\n"
    
    return md


def sync_research():
    """Main sync function."""
    log("Starting research sync...")
    
    # Ensure directories exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load research config
    research_data = load_yaml("research.yaml")
    entries = research_data.get("research", [])
    
    if not entries:
        log("No research entries found in research.yaml")
        return
    
    synced = 0
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            log(f"WARNING: Research entry {i} is not a dict, skipping")
            continue
        
        log(f"Processing research entry {i+1}/{len(entries)}...")
        
        # Handle auto-sync from repo
        if entry.get("autoSync") and entry.get("repo"):
            repo = entry["repo"]
            log(f"  Auto-syncing from repo: {repo}")
            
            # Fetch and parse README
            readme = fetch_readme(repo)
            if not readme:
                log(f"  WARNING: Could not fetch README for {repo}, using manual data")
                parsed = {}
            else:
                # Parse README
                title = readme.split('\n')[0].replace('# ', '').strip()
                parsed = {
                    "title": title,
                    "authors": extract_field(readme, "Authors"),
                    "venue": extract_field(readme, "Venue"),
                    "arxiv": extract_field(readme, "arXiv"),
                    "date": extract_field(readme, "Date"),
                    "abstract": extract_section(readme, "Abstract"),
                    "methodology": parse_methodology(extract_section(readme, "Methodology")),
                    "conclusion": extract_section(readme, "Results / Conclusion"),
                    "tags": parse_keywords(extract_section(readme, "Keywords")),
                }
                
                # Download thumbnail if specified
                thumbnail_path = extract_field(readme, "Thumbnail")
                if thumbnail_path and not entry.get("thumbnail"):
                    parsed["thumbnail"] = download_thumbnail(repo, thumbnail_path)
            
            # Generate markdown file
            slug = slugify(parsed.get("title", entry.get("title", f"research-{i}")))
            md_content = generate_research_md(entry, parsed)
            
            md_path = OUTPUT_DIR / f"{slug}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            log(f"  Generated: {md_path}")
            synced += 1
            
        # Handle manual entry
        elif entry.get("title"):
            log(f"  Processing manual entry: {entry['title']}")
            slug = slugify(entry["title"])
            md_content = generate_research_md(entry, {})
            
            md_path = OUTPUT_DIR / f"{slug}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            log(f"  Generated: {md_path}")
            synced += 1
        else:
            log(f"  WARNING: Entry {i} has no repo or title, skipping")
    
    log(f"Done! Synced {synced} research papers.")


if __name__ == "__main__":
    try:
        sync_research()
        sys.exit(0)
    except Exception as e:
        log(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
