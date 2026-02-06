from flask import Flask, render_template, request, jsonify, redirect, url_for
import sovereign_schema
import database # Import the new database module
import os

app = Flask(__name__)

# --- Sovereign Schema & DB Integration ---
SOVEREIGN_ENTITIES = sovereign_schema.SOVEREIGN_ENTITIES
DATABASE_INITIALIZED = False

def initialize_database():
    """Initializes the database, creates tables, and seeds it with initial data if needed."""
    global DATABASE_INITIALIZED
    if not DATABASE_INITIALIZED:
        # Create tables based on the schema
        database.create_tables()
        
        # --- One-time data seeding ---
        # Check if the database is empty before seeding
        if not database.get_all_for_entity("manuscripts"):
            print("Database is empty. Seeding initial data...")
            conn = database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO manuscripts (title, author, era) VALUES (?, ?, ?)", 
                           ("المخطوطة الأولى", "المؤلف الأول", "العصر العباسي"))
            cursor.execute("INSERT INTO manuscripts (title, author, era) VALUES (?, ?, ?)", 
                           ("المخطوطة الثانية", "المؤلف الثاني", "العصر الأموي"))
            cursor.execute("INSERT INTO documents (title, date, type) VALUES (?, ?, ?)", 
                           ("وثيقة الوقف", "2023-12-12", "صك"))
            conn.commit()
            conn.close()
            print("Initial data seeded.")

        DATABASE_INITIALIZED = True

# --- Routes ---
@app.before_request
def before_first_request_func():
    initialize_database()

@app.route("/")
def index():
    sidebar_structure = sovereign_schema.get_sidebar_structure()
    return render_template("index.html", sidebar_structure=sidebar_structure)

@app.route("/manage/<entity_slug>")
def manage_entity(entity_slug):
    entity = SOVEREIGN_ENTITIES.get(entity_slug)
    if not entity:
        return "Entity not found", 404

    # Fetch data from the real database
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

    # For a GET request, fetch existing data and show the form
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
    app.run(debug=True)
