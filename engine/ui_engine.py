
import json

class DynamicUIEngine:
    def __init__(self, doctype_name, db):
        self.doctype_name = doctype_name
        self.db = db  # Receive the db connection
        self.doctype_def = self.load_doctype_definition()

    def load_doctype_definition(self):
        """Loads the DocType definition (JSON) from the 'doctype' folder."""
        try:
            with open(f"doctype/{self.doctype_name}/{self.doctype_name}.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"DocType definition not found for: {self.doctype_name}")

    def render_form(self):
        """Renders the form based on the DocType definition."""
        if not self.doctype_def:
            return "<p>Error: DocType definition not loaded.</p>"

        html = f"<h1>{self.doctype_def.get('name', 'Form')}</h1>"
        html += "<form>"

        for field in self.doctype_def.get('fields', []):
            field_type = field.get('fieldtype', 'Data')
            label = field.get('label', '')
            fieldname = field.get('fieldname', '')

            if field_type == 'Data':
                html += f'<div><label for="{fieldname}">{label}</label><input type="text" id="{fieldname}" name="{fieldname}"></div>'
            elif field_type == 'Text':
                html += f'<div><label for="{fieldname}">{label}</label><textarea id="{fieldname}" name="{fieldname}"></textarea></div>'
            # Add more field types as needed

        html += "<button type=\"submit\">Submit</button>"
        html += "</form>"
        return html
