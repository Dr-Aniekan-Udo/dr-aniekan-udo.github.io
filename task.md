# Portfolio v3.0 — Config-Driven Implementation Tasks

## Phase 1: YAML Infrastructure
- [x] Create `data/` directory
- [x] Create `data/experience.yaml`
- [x] Create `data/education.yaml`
- [x] Create `data/research.yaml`
- [x] Create `data/skills.yaml`
- [x] Create `data/about.yaml`
- [ ] Create `scripts/sync-content.py` (YAML validator & loader)
- [ ] Create `scripts/sync-research.py` (README parser)
- [ ] Update `scripts/sync-projects.py` (enhanced README parsing)

## Phase 2: Experience Redesign
- [ ] Redesign `Experience.astro` (YAML-driven + photos)
- [ ] Add photo support (opposite timeline side)
- [ ] Auto-generate placeholder for missing photos

## Phase 3: Education & Skills Components
- [ ] Create `Education.astro` component
- [ ] Update `Skills.astro` to read from YAML

## Phase 4: Research Auto-Sync
- [ ] Implement `sync-research.py`
- [ ] Update glioma repo README to match template
- [ ] Create `ResearchCard.astro`
- [ ] Update `Research.astro`

## Phase 5: About & Navigation Updates
- [ ] Update `About.astro` to read from YAML
- [ ] Update `Hero.astro` to read from YAML
- [ ] Update `Navigation.astro`
- [ ] Update `Footer.astro`

## Phase 6: Enhanced Project Sync
- [ ] Update project README parsing
- [ ] Extract structured sections (Category, Tech Stack, Overview)

## Phase 7: Documentation
- [ ] Update `AGENTS.md`
- [ ] Create `RESEARCH_TEMPLATE.md`
- [ ] Create `PROJECT_README_TEMPLATE.md`
- [ ] Create `CONTENT_GUIDE.md`

## Phase 8: Populate & Deploy
- [ ] Migrate all existing content to YAML
- [ ] Build and test locally
- [ ] Commit and push
