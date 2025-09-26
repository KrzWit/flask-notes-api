# Flask Notes API

A tiny REST API for managing notes, built with Flask.  
Data is stored in a local `notes.json` file (auto-created on first write).

## Features
- CRUD endpoints for notes (JSON in/out)
- Text search: `?q=...`
- Sorting: `?sort=created_at|updated_at|title&order=asc|desc`
- Pagination: `?limit=&offset=`
- Health check endpoint `/health`

---

## Quick Start (local)

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # or: pip install flask
python app.py
# App runs on http://127.0.0.1:5000
```


## cURl examples

```bash
# health
curl http://127.0.0.1:5000/health

# create
curl -X POST http://127.0.0.1:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"First","content":"Hello Motorola!"}'

# list
curl http://127.0.0.1:5000/notes

# get by id
curl http://127.0.0.1:5000/notes/<ID>

# update
curl -X PUT http://127.0.0.1:5000/notes/<ID> \
  -H "Content-Type: application/json" \
  -d '{"content":"Updated"}'

# delete
curl -X DELETE http://127.0.0.1:5000/notes/<ID>
```
##Run in GitHub Codespaces

```bash
# inside Codespaces terminal
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```





