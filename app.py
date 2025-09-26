from flask import Flask, request, jsonify
import json, os, uuid, datetime
from threading import Lock

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "notes.json")
_lock = Lock()

def _now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def _read_all():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _write_all(notes):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def index():
    return {"message": "Flask Notes API", "endpoints": ["/health", "/notes"]}


@app.get("/notes")
def list_notes():
    q = (request.args.get("q") or "").strip().lower()
    notes = _read_all()
    if q:
        notes = [n for n in notes if q in n["title"].lower() or q in n["content"].lower()]
    # opcjonalne sortowanie
    sort = request.args.get("sort", "created_at")
    reverse = request.args.get("order", "desc") == "desc"
    if sort in {"created_at", "updated_at", "title"}:
        notes.sort(key=lambda n: n.get(sort, ""), reverse=reverse)
    # paginacja
    try:
        limit = int(request.args.get("limit", 0))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "limit/offset must be integers"}), 400
    if offset:
        notes = notes[offset:]
    if limit:
        notes = notes[:limit]
    return jsonify(notes)

@app.get("/notes/<note_id>")
def get_note(note_id):
    for n in _read_all():
        if n["id"] == note_id:
            return jsonify(n)
    return jsonify({"error": "note not found"}), 404

@app.post("/notes")
def create_note():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    if not title or not content:
        return jsonify({"error": "title and content are required"}), 400

    note = {
        "id": uuid.uuid4().hex[:8],
        "title": title,
        "content": content,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    with _lock:
        all_notes = _read_all()
        all_notes.append(note)
        _write_all(all_notes)
    return jsonify(note), 201

@app.put("/notes/<note_id>")
def update_note(note_id):
    data = request.get_json(silent=True) or {}
    with _lock:
        notes = _read_all()
        for n in notes:
            if n["id"] == note_id:
                if "title" in data:
                    n["title"] = (data["title"] or "").strip()
                if "content" in data:
                    n["content"] = (data["content"] or "").strip()
                n["updated_at"] = _now_iso()
                _write_all(notes)
                return jsonify(n)
    return jsonify({"error": "note not found"}), 404

@app.delete("/notes/<note_id>")
def delete_note(note_id):
    with _lock:
        notes = _read_all()
        new_notes = [n for n in notes if n["id"] != note_id]
        if len(new_notes) == len(notes):
            return jsonify({"error": "note not found"}), 404
        _write_all(new_notes)
    return "", 204


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
