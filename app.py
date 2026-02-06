
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, render_template
from engine.ui_engine import DynamicUIEngine
from engine.workflow_engine import WorkflowEngine

# --- Sovereign Schema Import ---
from sovereign_schema import SOVEREIGN_ENTITIES, get_sidebar_structure

# --- Firebase Initialization ---
# This block handles Firebase connection for both Render (using env vars)
# and local development (using a key file).
try:
    cred = None
    creds_json_str = os.environ.get('FIREBASE_CREDENTIALS')
    if creds_json_str:
        print("--- Initializing Firebase from Environment Variable ---")
        creds_dict = json.loads(creds_json_str)
        cred = credentials.Certificate(creds_dict)
    else:
        print("--- Initializing Firebase from local key file ---")
        cred = credentials.Certificate('modl-mawkuf-key.json')
    
    # Corrected: Initialize app outside the if/else block
    firebase_admin.initialize_app(cred)
    
    print("--- Firebase Connection Test SUCCEEDED ---")
    db = firestore.client()

except Exception as e:
    print("--- Firebase Connection Test FAILED ---")
    if 'modl-mawkuf-key.json' in str(e):
        print("Reason: Service key file not found. Check Render Secret File or local file.")
    elif 'FIREBASE_CREDENTIALS' in str(e):
        print("Reason: Failed to parse FIREBASE_CREDENTIALS environment variable.")
    else:
        print(f"Reason: {e}")
    db = None # Set db to None if initialization fails


app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

# --- Context Processor ---
# This makes the sidebar structure available to all templates automatically.
@app.context_processor
def inject_sidebar_structure():
    return dict(sidebar_structure=get_sidebar_structure())

# --- Middleware ---
@app.before_request
def before_request_func():
    if db is None and request.path not in ['/', '/identity_and_appearance']:
        return jsonify({"status": "error", "message": "Database connection failed. Check server logs."}), 503

# --- Core Routes ---
@app.route('/')
def index():
    # The sovereign_entities are passed for the main dashboard cards.
    return render_template('index.html', sovereign_entities=SOVEREIGN_ENTITIES)

@app.route('/identity_and_appearance')
def identity_and_appearance_manager():
    return render_template('identity_and_appearance_manager.html')

# --- Generic Manager Route (The UI Factory) ---
@app.route('/manage/<entity_slug>')
def manager_view(entity_slug):
    entity = SOVEREIGN_ENTITIES.get(entity_slug)
    if not entity:
        return "Entity not found", 404
    # The manager_template will be created in the next step.
    return render_template('manager_template.html', entity=entity)

# --- API Routes ---
@app.route('/api/identity_settings', methods=['POST'])
def save_identity_settings():
    try:
        settings_data = request.get_json()
        if not settings_data:
            return jsonify({"status": "error", "message": "Invalid data. JSON expected."}), 400
        
        settings_ref = db.collection('settings').document('identity_and_appearance')
        settings_ref.set(settings_data, merge=True)
        
        return jsonify({"status": "success", "message": "تم حفظ الإعدادات بنجاح."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"خطأ في الحفظ: {str(e)}"}), 500


# --- Deprecated Engine Routes (to be phased out) ---
@app.route('/render/<doctype_name>')
def render_doctype(doctype_name):
    try:
        ui_engine = DynamicUIEngine(doctype_name, db)
        return ui_engine.render_form()
    except Exception as e:
        return str(e), 404

@app.route('/submit/<doctype_name>/<doc_id>', methods=['POST'])
def submit_document(doctype_name, doc_id):
    user_role = request.headers.get('X-User-Role', 'user')
    
    try:
        form_data = request.get_json()
        if not form_data:
            return jsonify({"status": "error", "message": "Invalid form data. JSON expected."}), 400
            
        doc_ref = db.collection(doctype_name).document(doc_id)
        doc_ref.set(form_data, merge=True)

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error saving data to Firestore: {str(e)}"}), 500

    workflow_engine = WorkflowEngine(doctype_name, doc_id, db)
    current_state = workflow_engine.get_document_state()
    next_state = 'Submitted' # Example transition

    if workflow_engine.can_transition(user_role, current_state, next_state):
        workflow_engine.set_document_state(next_state)
        return jsonify({"status": "success", "message": "Document saved and workflow updated.", "new_state": next_state})
    else:
        return jsonify({"status": "warning", "message": "Data saved, but workflow transition denied.", "new_state": current_state}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
