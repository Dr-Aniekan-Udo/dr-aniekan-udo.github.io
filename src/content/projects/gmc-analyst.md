---
title: "Gmc Analyst"
repo: "Dr-Aniekan-Udo/gmc-analyst"
category: "Fullstack"
description: "A fullstack web application for analyzing Global Management Challenge (GMC) competition data. Parse Excel reports, visualize financial and operational metrics, and simulate decision outcomes"
excerpt: "A fullstack web application for analyzing Global Management Challenge (GMC) competition data. Parse Excel reports, visualize financial and operational metrics, and simulate decision outcomes."
thumbnail: "/default-thumbnail.svg"
githubUrl: "https://github.com/Dr-Aniekan-Udo/gmc-analyst"
stars: 0
language: "TypeScript"
featured: true
priority: 1
tags: []
---

# Gmc Analyst

# GMC Analyst

A fullstack web application for analyzing Global Management Challenge (GMC) competition data. Parse Excel reports, visualize financial and operational metrics, and simulate decision outcomes.

## Tech Stack

- **Backend:** Go 1.22+ with Gin framework
- **Frontend:** React + TypeScript with Vite
- **Database:** PostgreSQL 16+
- **State Management:** Zustand v5.0+

## Project Structure

```
/gmc-analyst
├── /cmd/api          # Go API entry point
├── /internal         # Go internal packages (domain, adapters, config)
├── /web              # React frontend (Vite)
├── /config           # Configuration files
├── /migrations       # Database migrations
└── /docs             # Documentation
```

## Getting Started

### Prerequisites

- Go 1.22+
- Node.js 18+
- PostgreSQL 16+

### Backend Setup

```bash
# Install dependencies
go mod download

# Set environment variables (copy and edit)
cp .env.example .env

# Run the backend server (port 3030)
go run ./cmd/api
```

### Frontend Setup

```bash
cd web
npm install
npm run dev  # runs on port 5173
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `3030` | Backend API port |
| `DATABASE_URL` | - | PostgreSQL connection string |
| `LOG_LEVEL` | `debug` | Logging level |
| `CORS_ORIGIN` | `http://localhost:5173` | Allowed CORS origin |

## Development

```bash
# Run backend
go run ./cmd/api

# Run tests
go test ./...

# Run frontend
cd web && npm run dev
```

## License

MIT
