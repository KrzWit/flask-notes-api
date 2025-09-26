# Flask Notes API

A tiny REST API for managing notes, built with Flask.  
Data is stored in a local `notes.json` file (auto-created on first write).

## Features
- CRUD endpoints for notes (JSON in/out)
- Text search (`?q=...`)
- Sorting (`?sort=created_at|updated_at|title&order=asc|desc`)
- Pagination (`?limit=&offset=`)
- Health check endpoint

## Quick start

```bash
# (optional) create a virtual env
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate

# install dependency
pip install flask

# run the app
python src/app.py                   # or: python app.py  (if file is in repo root)
# server: http://127.0.0.1:5000
