
from flask import Flask, request, jsonify, render_template
from engine.ui_engine import DynamicUIEngine
from engine.workflow_engine import WorkflowEngine
import firebase_setup # This will initialize Firebase
from firebase_admin import firestore

# Get a reference to the Firestore database
db = firestore.client()

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return "<h1>MWDLG Core Engine is running!</h1>" 

@app.route('/identity_and_appearance')
def identity_and_appearance_manager():
    """Renders the Identity and Appearance Manager admin interface."""
    return render_template('identity_and_appearance_manager.html')

@app.route('/api/identity_settings', methods=['POST'])
def save_identity_settings():
    """Saves the identity and appearance settings to Firestore."""
    try:
        settings_data = request.get_json()
        if not settings_data:
            return jsonify({"status": "error", "message": "Invalid data. JSON expected."}), 400
        
        # Use a specific document for these settings (Singleton pattern)
        settings_ref = db.collection('settings').document('identity_and_appearance')
        settings_ref.set(settings_data, merge=True) # merge=True updates fields without overwriting the whole doc
        
        return jsonify({"status": "success", "message": "Settings saved successfully."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error saving settings to Firestore: {str(e)}"}), 500

@app.route('/render/<doctype_name>')
def render_doctype(doctype_name):
    """Renders the form for a given DocType."""
    try:
        ui_engine = DynamicUIEngine(doctype_name)
        return ui_engine.render_form()
    except Exception as e:
        return str(e), 404

@app.route('/submit/<doctype_name>/<doc_id>', methods=['POST'])
def submit_document(doctype_name, doc_id):
    """Submits a document, saves its data, and moves it to the next workflow state."""
    user_role = request.headers.get('X-User-Role', 'user') # Get user role from header
    
    # --- Firestore Data Saving ---
    try:
        form_data = request.get_json()
        if not form_data:
            return jsonify({"status": "error", "message": "Invalid form data. JSON expected."}), 400
            
        doc_ref = db.collection(doctype_name).document(doc_id)
        doc_ref.set(form_data, merge=True)

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error saving data to Firestore: {str(e)}"}), 500

    # --- Workflow Engine Logic ---
    workflow_engine = WorkflowEngine(doctype_name, doc_id)
    current_state = workflow_engine.get_document_state()
    next_state = 'Submitted' # Example transition

    if workflow_engine.can_transition(user_role, current_state, next_state):
        workflow_engine.set_document_state(next_state)
        return jsonify({"status": "success", "message": "Document saved and workflow updated.", "new_state": next_state})
    else:
        return jsonify({"status": "warning", "message": "Data saved, but workflow transition denied.", "new_state": current_state}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
