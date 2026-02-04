
from firebase_setup import db

class WorkflowEngine:
    def __init__(self, doctype_name, doc_id):
        self.doctype_name = doctype_name
        self.doc_id = doc_id
        self.doc_ref = db.collection(self.doctype_name).document(self.doc_id)

    def get_document_state(self):
        """Gets the current state of the document."""
        doc = self.doc_ref.get()
        if doc.exists:
            return doc.to_dict().get('workflow_state', 'Draft')
        return 'Draft'

    def set_document_state(self, new_state):
        """Sets the new state of the document."""
        self.doc_ref.update({'workflow_state': new_state})

    def can_transition(self, user_role, current_state, next_state):
        """Checks if a user with a given role can transition the document state."""
        # This is a simplified role-based access matrix. 
        # You can expand this with more complex logic.
        rules = {
            'Draft': {
                'submit': ['user', 'admin'],
            },
            'Submitted': {
                'review': ['reviewer', 'admin'],
                'reject': ['reviewer', 'admin'],
            },
            'Reviewed': {
                'approve': ['approver', 'admin'],
                'reject': ['approver', 'admin'],
            },
            'Approved': {},
            'Rejected': {
                're-submit': ['user', 'admin']
            }
        }

        if current_state in rules and next_state in rules[current_state]:
            return user_role in rules[current_state][next_state]
        return False
