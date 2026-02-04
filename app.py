
from flask import Flask, request, jsonify
from engine.ui_engine import DynamicUIEngine
from engine.workflow_engine import WorkflowEngine
import firebase_setup # This will initialize Firebase

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>MWDLG Core Engine is running!</h1>" 

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
    """Submits a document and moves it to the next workflow state."""
    user_role = request.headers.get('X-User-Role', 'user') # Get user role from header
    workflow_engine = WorkflowEngine(doctype_name, doc_id)
    current_state = workflow_engine.get_document_state()
    next_state = 'Submitted' # Example transition

    if workflow_engine.can_transition(user_role, current_state, next_state):
        workflow_engine.set_document_state(next_state)
        # Here you would also save the form data to Firestore
        return jsonify({"status": "success", "new_state": next_state})
    else:
        return jsonify({"status": "error", "message": "Permission denied"}), 403

if __name__ == '__main__':
    # Before running, make sure to:
    # 1. Install Flask: pip install Flask
    # 2. Provide your Firebase service account key in firebase_setup.py
    app.run(debug=True)
