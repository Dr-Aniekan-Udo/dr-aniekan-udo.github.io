#!/usr/bin/env python3
"""
Content Sync Script

Reads all YAML config files from data/ directory, validates schema,
generates placeholder images for missing photos, and outputs a typed
TypeScript data file for Astro components to consume.

Usage:
    python scripts/sync-content.py
"""

import os
import sys
import yaml
import hashlib
from pathlib import Path
from datetime import datetime

# Configuration
DATA_DIR = Path("data")
OUTPUT_FILE = Path("src/data/content.ts")
PUBLIC_DIR = Path("public")
EXPERIENCE_DIR = PUBLIC_DIR / "experience"
EDUCATION_DIR = PUBLIC_DIR / "education"
RESEARCH_DIR = PUBLIC_DIR / "research"

# Beautiful SVG placeholder template for experience photos (landscape 4:3)
# Uses unique IDs via {uid} to prevent collisions if SVGs are ever inlined
EXPERIENCE_PLACEHOLDER_SVG = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bgGrad-{uid}" x1="0" y1="0" x2="{width}" y2="{height}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1a1a1a"/>
      <stop offset="50%" stop-color="#141414"/>
      <stop offset="100%" stop-color="#0f0f0f"/>
    </linearGradient>
    <radialGradient id="glow-{uid}" cx="50%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots-{uid}" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="12" cy="12" r="1" fill="#262626" opacity="0.6"/>
    </pattern>
  </defs>

  <rect width="{width}" height="{height}" rx="16" fill="url(#bgGrad-{uid})"/>
  <rect width="{width}" height="{height}" rx="16" fill="url(#dots-{uid})"/>
  <ellipse cx="{cx}" cy="{cy_top}" rx="{glow_rx}" ry="{glow_ry}" fill="url(#glow-{uid})"/>

  <rect x="{margin}" y="20" width="{accent_width}" height="2" rx="1" fill="#f59e0b" opacity="0.6"/>
  <rect x="{margin}" y="24" width="{accent_width2}" height="1" rx="0.5" fill="#f59e0b" opacity="0.3"/>

  <path d="M {margin} 55 L {margin} 42 A 7 7 0 0 1 {margin2} 35 L {margin3} 35" fill="none" stroke="#f59e0b" stroke-width="1.5" opacity="0.35" stroke-linecap="round"/>
  <path d="M {right_x} 55 L {right_x} 42 A 7 7 0 0 0 {right_x2} 35 L {right_x3} 35" fill="none" stroke="#f59e0b" stroke-width="1.5" opacity="0.35" stroke-linecap="round"/>
  <path d="M {margin} {bottom_y} L {margin} {bottom_y2} A 7 7 0 0 0 {margin2} {bottom_y3} L {margin3} {bottom_y3}" fill="none" stroke="#f59e0b" stroke-width="1.5" opacity="0.35" stroke-linecap="round"/>
  <path d="M {right_x} {bottom_y} L {right_x} {bottom_y2} A 7 7 0 0 1 {right_x2} {bottom_y3} L {right_x3} {bottom_y3}" fill="none" stroke="#f59e0b" stroke-width="1.5" opacity="0.35" stroke-linecap="round"/>

  <g transform="translate({icon_x}, {icon_y})" opacity="0.6">
    <rect x="0" y="10" width="52" height="34" rx="7" fill="none" stroke="#a3a3a3" stroke-width="1.5"/>
    <rect x="18" y="2" width="16" height="8" rx="2" fill="none" stroke="#a3a3a3" stroke-width="1.5"/>
    <circle cx="26" cy="27" r="10" fill="none" stroke="#a3a3a3" stroke-width="1.5"/>
    <circle cx="26" cy="27" r="6" fill="none" stroke="#a3a3a3" stroke-width="1"/>
    <circle cx="42" cy="16" r="2" fill="#a3a3a3"/>
  </g>

  <text x="{cx}" y="{text_y}" text-anchor="middle" fill="#e5e5e5" font-family="Inter, system-ui, -apple-system, sans-serif" font-size="15" font-weight="600" letter-spacing="0.3">
    {label}
  </text>
  <text x="{cx}" y="{text_y2}" text-anchor="middle" fill="#737373" font-family="Inter, system-ui, -apple-system, sans-serif" font-size="11" font-weight="400" letter-spacing="0.5">
    PHOTO COMING SOON
  </text>

  <line x1="{cx2}" y1="{bottom_line_y}" x2="{cx3}" y2="{bottom_line_y}" stroke="#f59e0b" stroke-width="1.5" opacity="0.5" stroke-linecap="round"/>
  <rect x="0.5" y="0.5" width="{width_m1}" height="{height_m1}" rx="16" fill="none" stroke="#262626" stroke-width="1"/>
</svg>'''

# Square placeholder for logos (1:1)
LOGO_PLACEHOLDER_SVG = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bgGrad-{uid}" x1="0" y1="0" x2="{width}" y2="{height}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1a1a1a"/>
      <stop offset="100%" stop-color="#0f0f0f"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" rx="16" fill="url(#bgGrad-{uid})"/>
  <circle cx="{cx}" cy="{cy_top}" r="32" fill="#f59e0b" opacity="0.06"/>
  <text x="{cx}" y="{cy}" text-anchor="middle" fill="#e5e5e5" font-family="Inter, system-ui, -apple-system, sans-serif" font-size="13" font-weight="600">
    {initial}
  </text>
  <text x="{cx}" y="{cy2}" text-anchor="middle" fill="#737373" font-family="Inter, system-ui, -apple-system, sans-serif" font-size="9">
    {label}
  </text>
  <rect x="0.5" y="0.5" width="{width_m1}" height="{height_m1}" rx="16" fill="none" stroke="#262626" stroke-width="1"/>
</svg>'''


def log(msg: str):
    print(f"[content-sync] {msg}")


def escape_xml(text: str) -> str:
    """Escape XML special characters for safe use in SVG text nodes."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def sanitize_filename(name: str) -> str:
    """Sanitize a string for safe use as a filesystem filename.

    Removes/replaces characters that are invalid or problematic in filenames
    across Windows, macOS, and Linux.
    """
    import re
    # Replace spaces with hyphens
    safe = name.replace(" ", "-")
    # Remove characters invalid in filenames: < > : " / \ | ? *
    safe = re.sub(r'[<>:"/\\|?*]', "", safe)
    # Remove control characters
    safe = re.sub(r'[\x00-\x1f\x7f]', "", safe)
    # Remove leading/trailing periods (Windows restriction)
    safe = safe.strip(".")
    # Collapse multiple hyphens
    safe = re.sub(r'-+', "-", safe)
    # Strip leading/trailing hyphens
    safe = safe.strip("-")
    # Limit length
    return safe[:80] if safe else "unnamed"


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


def ensure_dir(path: Path):
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)


def generate_placeholder(path: Path, label: str, width: int = 400, height: int = 300):
    """Generate a beautiful SVG placeholder image."""
    # Always save as .svg for proper browser rendering
    svg_path = path.with_suffix(".svg")
    if svg_path.exists():
        return str(svg_path).replace("\\", "/").replace("public/", "/")

    cx = width // 2
    cy_top = height // 2 - 50
    cy = height // 2 + 25
    cy2 = height // 2 + 50
    margin = 24
    margin2 = margin + 12
    margin3 = margin + 30
    right_x = width - margin
    right_x2 = right_x - 12
    right_x3 = right_x - 30
    bottom_y = height - 30
    bottom_y2 = height - 15
    bottom_y3 = height - 5
    icon_x = cx - 26
    icon_y = cy_top - 20
    text_y = cy_top + 55
    text_y2 = text_y + 22
    cx2 = cx - 20
    cx3 = cx + 20
    bottom_line_y = height - 28
    accent_width = width - (margin * 2)
    accent_width2 = int(accent_width * 0.6)
    width_m1 = width - 1
    height_m1 = height - 1
    glow_rx = int(width * 0.45)
    glow_ry = int(height * 0.4)
    # Unique ID based on filename to prevent SVG ID collisions
    uid = hashlib.md5(str(svg_path).encode()).hexdigest()[:8]

    svg = EXPERIENCE_PLACEHOLDER_SVG.format(
        width=width, height=height, cx=cx, cy_top=cy_top, cy=cy, cy2=cy2,
        margin=margin, margin2=margin2, margin3=margin3,
        right_x=right_x, right_x2=right_x2, right_x3=right_x3,
        bottom_y=bottom_y, bottom_y2=bottom_y2, bottom_y3=bottom_y3,
        icon_x=icon_x, icon_y=icon_y,
        text_y=text_y, text_y2=text_y2,
        cx2=cx2, cx3=cx3, bottom_line_y=bottom_line_y,
        accent_width=accent_width, accent_width2=accent_width2,
        width_m1=width_m1, height_m1=height_m1,
        glow_rx=glow_rx, glow_ry=glow_ry,
        label=escape_xml(label[:35]), uid=uid
    )

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    log(f"Generated placeholder: {svg_path}")
    return str(svg_path).replace("\\", "/").replace("public/", "/")


def generate_logo_placeholder(path: Path, label: str, width: int = 200, height: int = 200):
    """Generate a square SVG placeholder for logos."""
    svg_path = path.with_suffix(".svg")
    if svg_path.exists():
        return str(svg_path).replace("\\", "/").replace("public/", "/")

    cx = width // 2
    cy_top = height // 2 - 15
    cy = height // 2 + 5
    cy2 = height // 2 + 22
    width_m1 = width - 1
    height_m1 = height - 1
    initial = label[0].upper() if label and label.strip() else "?"
    # Unique ID based on filename to prevent SVG ID collisions
    uid = hashlib.md5(str(svg_path).encode()).hexdigest()[:8]

    svg = LOGO_PLACEHOLDER_SVG.format(
        width=width, height=height, cx=cx, cy_top=cy_top, cy=cy, cy2=cy2,
        width_m1=width_m1, height_m1=height_m1,
        initial=escape_xml(initial), label=escape_xml(label[:20]), uid=uid
    )

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    log(f"Generated logo placeholder: {svg_path}")
    return str(svg_path).replace("\\", "/").replace("public/", "/")


def process_experience(data: dict) -> list:
    """Process experience entries and generate placeholders."""
    entries = data.get("experience", [])
    ensure_dir(EXPERIENCE_DIR)

    for entry in entries:
        photo = entry.get("photo", "")
        if photo:
            # Sanitize filename to prevent invalid filesystem characters
            photo_stripped = photo.lstrip("/")
            safe_name = sanitize_filename(Path(photo_stripped).name)
            photo_path = PUBLIC_DIR / Path(photo_stripped).parent / safe_name
            # If the exact file doesn't exist, check for .svg version
            if not photo_path.exists():
                svg_path = photo_path.with_suffix(".svg")
                if svg_path.exists():
                    # Update YAML reference to .svg
                    entry["photo"] = str(svg_path).replace("\\", "/").replace("public/", "/")
                else:
                    # Generate new placeholder and update reference
                    new_path = generate_placeholder(
                        photo_path,
                        entry.get("org", "Experience").split("(")[0].strip()
                    )
                    if new_path:
                        entry["photo"] = new_path

    return entries


def process_education(data: dict) -> list:
    """Process education entries and generate placeholders."""
    entries = data.get("education", [])
    ensure_dir(EDUCATION_DIR)

    for entry in entries:
        logo = entry.get("logo", "")
        if logo:
            # Sanitize filename to prevent invalid filesystem characters
            logo_stripped = logo.lstrip("/")
            safe_name = sanitize_filename(Path(logo_stripped).name)
            logo_path = PUBLIC_DIR / Path(logo_stripped).parent / safe_name
            if not logo_path.exists():
                svg_path = logo_path.with_suffix(".svg")
                if svg_path.exists():
                    entry["logo"] = str(svg_path).replace("\\", "/").replace("public/", "/")
                else:
                    new_path = generate_logo_placeholder(logo_path, entry.get("school", "School"))
                    if new_path:
                        entry["logo"] = new_path

    return entries


def process_research(data: dict) -> list:
    """Process research entries."""
    entries = data.get("research", [])
    
    valid_entries = []
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            log(f"WARNING: Research entry {i} is not a dict, skipping")
            continue
        if "repo" in entry or "title" in entry:
            valid_entries.append(entry)
        else:
            log(f"WARNING: Research entry {i} missing 'repo' or 'title', skipping")
    
    return valid_entries


def dict_to_ts(d: dict, indent: int = 0) -> str:
    """Convert a dict to TypeScript object literal."""
    if not d:
        return "{}"
    
    items = []
    for k, v in d.items():
        key = f'"{k}"' if isinstance(k, str) else str(k)
        val = value_to_ts(v, indent + 2)
        items.append(f"{key}: {val}")
    
    return "{\n" + ",\n".join("  " * (indent + 1) + item for item in items) + f"\n{'  ' * indent}}}"


def list_to_ts(lst: list, indent: int = 0) -> str:
    """Convert a list to TypeScript array literal."""
    if not lst:
        return "[]"
    
    items = [value_to_ts(v, indent + 1) for v in lst]
    return "[\n" + ",\n".join("  " * (indent + 1) + item for item in items) + f"\n{'  ' * indent}]"


def value_to_ts(v, indent: int = 0) -> str:
    """Convert any Python value to TypeScript literal."""
    if v is None:
        return "null"
    elif isinstance(v, bool):
        return "true" if v else "false"
    elif isinstance(v, (int, float)):
        return str(v)
    elif isinstance(v, str):
        escaped = v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    elif isinstance(v, list):
        return list_to_ts(v, indent)
    elif isinstance(v, dict):
        return dict_to_ts(v, indent)
    else:
        return f'"{str(v)}"'


def generate_typescript(data: dict) -> str:
    """Generate the TypeScript data file."""
    
    profile = data.get("about", {}).get("profile", {})
    social = data.get("about", {}).get("social", {})
    contact = data.get("about", {}).get("contact", {})
    experience = data.get("experience", [])
    education = data.get("education", [])
    research = data.get("research", [])
    skills = data.get("skills", {})
    
    ts = f'''// Auto-generated by sync-content.py
// Generated at: {datetime.now().isoformat()}
// DO NOT EDIT MANUALLY - Edit YAML files in data/ instead

export const profile = {value_to_ts(profile, 0)};

export const social = {value_to_ts(social, 0)};

export const contact = {value_to_ts(contact, 0)};

export const experience = {value_to_ts(experience, 0)};

export const education = {value_to_ts(education, 0)};

export const research = {value_to_ts(research, 0)};

export const skills = {value_to_ts(skills, 0)};
'''
    
    return ts


def sync_content():
    """Main sync function."""
    log("Starting content sync...")
    
    # Load all YAML files
    about_data = load_yaml("about.yaml")
    experience_data = load_yaml("experience.yaml")
    education_data = load_yaml("education.yaml")
    research_data = load_yaml("research.yaml")
    skills_data = load_yaml("skills.yaml")
    
    # Process entries and generate placeholders
    experience_entries = process_experience(experience_data)
    education_entries = process_education(education_data)
    research_entries = process_research(research_data)
    
    # Combine into single data structure
    all_data = {
        "about": about_data,
        "experience": experience_entries,
        "education": education_entries,
        "research": research_entries,
        "skills": skills_data.get("skills", {}) if isinstance(skills_data, dict) else {},
    }
    
    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate TypeScript file
    ts_content = generate_typescript(all_data)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(ts_content)
    
    log(f"Generated: {OUTPUT_FILE}")
    log(f"  - Experience entries: {len(experience_entries)}")
    log(f"  - Education entries: {len(education_entries)}")
    log(f"  - Research entries: {len(research_entries)}")
    skills_dict = all_data.get("skills", {})
    log(f"  - Skill categories: {len(skills_dict)}")
    log("Done!")


if __name__ == "__main__":
    try:
        sync_content()
        sys.exit(0)
    except Exception as e:
        log(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
