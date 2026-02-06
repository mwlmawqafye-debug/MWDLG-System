from flask import Flask, render_template, request, jsonify, redirect, url_for
from whitenoise import WhiteNoise
import sovereign_schema
import database
import os

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")

# --- Database & Schema Initialization ---
database.create_tables()
SOVEREIGN_ENTITIES = sovereign_schema.SOVEREIGN_ENTITIES

# --- Context Processor ---
@app.context_processor
def inject_sidebar_structure():
    """Injects sidebar_structure into all templates automatically."""
    return dict(sidebar_structure=sovereign_schema.get_sidebar_structure())

# --- Main Routes ---

@app.route("/")
def index():
    try:
        manuscripts_count = len(database.get_all_for_entity("manuscripts"))
        documents_count = len(database.get_all_for_entity("documents"))
    except Exception:
        manuscripts_count = 0
        documents_count = 0
    stats = {"manuscripts": manuscripts_count, "documents": documents_count}
    return render_template("index.html", stats=stats)

@app.route("/manage/<entity_slug>")
def manage_entity(entity_slug):
    entity = SOVEREIGN_ENTITIES.get(entity_slug)
    if not entity:
        return "Entity not found", 404
    table_data = database.get_all_for_entity(entity_slug)
    return render_template("manager_template.html", entity=entity, table_data=table_data)

@app.route("/add/<entity_slug>", methods=["GET", "POST"])
def add_entity(entity_slug):
    entity = SOVEREIGN_ENTITIES.get(entity_slug)
    if not entity:
        return "Entity not found", 404
    if request.method == "POST":
        database.insert_entity(entity_slug, request.form.to_dict())
        return redirect(url_for('manage_entity', entity_slug=entity_slug))
    return render_template("form_template.html", entity=entity, form_data={})

@app.route("/edit/<entity_slug>/<int:record_id>", methods=["GET", "POST"])
def edit_entity(entity_slug, record_id):
    entity = SOVEREIGN_ENTITIES.get(entity_slug)
    if not entity:
        return "Entity not found", 404
    if request.method == "POST":
        database.update_entity(entity_slug, record_id, request.form.to_dict())
        return redirect(url_for('manage_entity', entity_slug=entity_slug))
    record_data = database.get_one_for_entity(entity_slug, record_id)
    if not record_data:
        return "Record not found", 404
    return render_template("form_template.html", entity=entity, form_data=record_data)

@app.route("/delete/<entity_slug>/<int:record_id>", methods=["POST"])
def delete_entity_route(entity_slug, record_id):
    database.delete_entity(entity_slug, record_id)
    return jsonify({"success": True})

@app.route("/identity-manager")
def identity_manager():
    return render_template("identity_and_appearance_manager.html")

# --- Main Execution ---
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)
