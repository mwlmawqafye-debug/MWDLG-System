from flask import Flask, render_template, request, jsonify, redirect, url_for
import sovereign_schema
import database
import os

app = Flask(__name__)

# --- Sovereign Schema & DB Integration ---
SOVEREIGN_ENTITIES = sovereign_schema.SOVEREIGN_ENTITIES

# Create database tables unconditionally when the app starts.
# This is the most reliable way to ensure tables exist before any requests are handled,
# especially in production environments like Railway or Render.
database.create_tables()

# --- Routes ---

@app.route("/")
def index():
    sidebar_structure = sovereign_schema.get_sidebar_structure()
    # For demonstration, let's fetch some stats for the dashboard
    try:
        manuscripts_count = len(database.get_all_for_entity("manuscripts"))
        documents_count = len(database.get_all_for_entity("documents"))
    except Exception as e:
        # This might happen if tables were just created and are empty
        print(f"Could not fetch counts, probably tables are empty. Error: {e}")
        manuscripts_count = 0
        documents_count = 0
        
    stats = {
        "manuscripts": manuscripts_count,
        "documents": documents_count
    }
    return render_template("index.html", sidebar_structure=sidebar_structure, stats=stats)

@app.route("/manage/<entity_slug>")
def manage_entity(entity_slug):
    entity = SOVEREIGN_ENTITIES.get(entity_slug)
    if not entity:
        return "Entity not found", 404

    table_data = database.get_all_for_entity(entity_slug)
    sidebar_structure = sovereign_schema.get_sidebar_structure()
    return render_template(
        "manager_template.html", 
        entity=entity, 
        sidebar_structure=sidebar_structure,
        table_data=table_data
    )

@app.route("/add/<entity_slug>", methods=["GET", "POST"])
def add_entity(entity_slug):
    entity = SOVEREIGN_ENTITIES.get(entity_slug)
    if not entity:
        return "Entity not found", 404

    if request.method == "POST":
        form_data = request.form.to_dict()
        database.insert_entity(entity_slug, form_data)
        return redirect(url_for('manage_entity', entity_slug=entity_slug))

    sidebar_structure = sovereign_schema.get_sidebar_structure()
    return render_template(
        "form_template.html", 
        entity=entity, 
        sidebar_structure=sidebar_structure,
        form_data={}
    )

@app.route("/edit/<entity_slug>/<int:record_id>", methods=["GET", "POST"])
def edit_entity(entity_slug, record_id):
    entity = SOVEREIGN_ENTITIES.get(entity_slug)
    if not entity:
        return "Entity not found", 404

    if request.method == "POST":
        form_data = request.form.to_dict()
        database.update_entity(entity_slug, record_id, form_data)
        return redirect(url_for('manage_entity', entity_slug=entity_slug))

    record_data = database.get_one_for_entity(entity_slug, record_id)
    if not record_data:
        return "Record not found", 404

    sidebar_structure = sovereign_schema.get_sidebar_structure()
    return render_template(
        "form_template.html", 
        entity=entity, 
        sidebar_structure=sidebar_structure,
        form_data=record_data
    )

@app.route("/delete/<entity_slug>/<int:record_id>", methods=["POST"])
def delete_entity_route(entity_slug, record_id):
    entity = SOVEREIGN_ENTITIES.get(entity_slug)
    if not entity:
        return jsonify({"success": False, "error": "Entity not found"}), 404

    database.delete_entity(entity_slug, record_id)
    return jsonify({"success": True})


@app.route("/identity-manager")
def identity_manager():
    sidebar_structure = sovereign_schema.get_sidebar_structure()
    return render_template("identity_and_appearance_manager.html", sidebar_structure=sidebar_structure)

if __name__ == "__main__":
    # This block runs only in local development
    # Let's seed the database if it's empty
    if not database.get_all_for_entity("manuscripts"):
        print("Database is empty. Seeding initial data for local development...")
        database.insert_entity("manuscripts", {"title": "المخطوطة الأولى", "author": "المؤلف الأول", "era": "العصر العباسي"})
        database.insert_entity("manuscripts", {"title": "المخطوطة الثانية", "author": "المؤلف الثاني", "era": "العصر الأموي"})
        database.insert_entity("documents", {"title": "وثيقة الوقف", "date": "2023-12-12", "type": "صك"})
        print("Initial data seeded.")

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)
