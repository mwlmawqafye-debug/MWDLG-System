
"""
================================
المخطط السيادي (The Sovereign Schema)
================================
هذا الملف هو دستور النظام وهيكله المركزي.
"""
from collections import defaultdict

# --- Icon Helper Functions ---

def _get_group_icon(group_name):
    """Returns the SVG path 'd' for a given group name."""
    icons = {
        'المظهر العام': "M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01",
        'المهام والمسميات الوظيفية': "M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z",
        'الكيانات الرئيسية': "M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
    }
    return icons.get(group_name, "M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z") # Default folder icon

def _get_module_icon(module_name):
    """Returns the SVG path 'd' for a given module name."""
    icons = {
        'الهوية والمظهر': "M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z",
        'تصنيف مهمة عمل': "M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z",
        'مخطوط': "M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25",
    }
    return icons.get(module_name, "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z") # Default document icon

# --- 1. Entity Definitions ---

IDENTITY_AND_APPEARANCE = {
    'slug': 'identity-manager',
    'name_singular': 'الهوية والمظهر',
    'name_plural': 'إدارة الهوية والمظهر',
    'category': 'إعداد النظام',
    'group': 'المظهر العام',
    'fields': {}
}

WORK_TASK_CLASSIFICATIONS = {
    'slug': 'work-task-classifications',
    'name_singular': 'تصنيف مهمة عمل',
    'name_plural': 'تصنيفات أنواع مهام العمل',
    'add_button_label': 'إضافة تصنيف',
    'category': 'إعداد النظام',
    'group': 'المهام والمسميات الوظيفية',
    'fields': {
        'classification_name': {'label': 'اسم التصنيف', 'type': 'text', 'required': True},
        'task_definition': {'label': 'تعريف مختصر عن المهمة', 'type': 'textarea', 'required': True, 'rows': 3},
        'notes': {'label': 'ملاحظات', 'type': 'textarea'}
    }
}

MANUSCRIPTS = {
    'slug': 'manuscripts',
    'name_singular': 'مخطوط',
    'name_plural': 'المخطوطات',
    'add_button_label': 'إضافة مخطوط',
    'category': 'البيانات الأساسية',
    'group': 'الكيانات الرئيسية',
    'fields': {
        'title': {'label': 'العنوان', 'type': 'text', 'searchable': True, 'required': True},
        'author': {'label': 'المؤلف', 'type': 'text', 'searchable': True},
        'status': {'label': 'الحالة', 'type': 'select', 'options': ['متاح', 'قيد الترميم', 'خاص', 'مفقود'], 'required': True},
        'acquisition_date': {'label': 'تاريخ الحيازة', 'type': 'date'},
        'pages': {'label': 'عدد الصفحات', 'type': 'number'},
    }
}

DOCUMENTS = {
    'slug': 'documents',
    'name_singular': 'وثيقة',
    'name_plural': 'الوثائق',
    'add_button_label': 'إضافة وثيقة',
    'category': 'البيانات الأساسية',
    'group': 'الكيانات الرئيسية',
    'fields': {
        'subject': {'label': 'الموضوع', 'type': 'text', 'searchable': True, 'required': True},
        'document_type': {'label': 'نوع الوثيقة', 'type': 'select', 'options': ['صك وقفي', 'مراسلات', 'سجل', 'إذن شرعي']},
        'issue_date': {'label': 'تاريخ الإصدار', 'type': 'date'},
        'is_archived': {'label': 'مؤرشفة', 'type': 'boolean'},
    }
}

# --- 2. The Sovereign List ---
SOVEREIGN_ENTITIES = {
    'identity-manager': IDENTITY_AND_APPEARANCE,
    'work-task-classifications': WORK_TASK_CLASSIFICATIONS,
    'manuscripts': MANUSCRIPTS,
    'documents': DOCUMENTS,
}

# --- 3. Backend Processing ---
def get_sidebar_structure():
    """
    Processes the raw SOVEREIGN_ENTITIES and transforms it into a structured
    data format ready for the template. It groups entities by category, and then
    by group within each category, adding the necessary icon paths.
    """
    categorized_entities = defaultdict(list)
    for slug, entity in SOVEREIGN_ENTITIES.items():
        entity['slug'] = slug
        # *** NEW: Add module icon to the entity itself ***
        entity['icon'] = _get_module_icon(entity['name_singular'])
        category = entity.get('category', 'عام')
        categorized_entities[category].append(entity)

    sidebar_data = {}
    for category, entities_in_cat in categorized_entities.items():
        groups = defaultdict(list)
        orphans = []
        for entity in entities_in_cat:
            if entity.get('group'):
                groups[entity['group']].append(entity)
            else:
                orphans.append(entity)

        # *** NEW: Add group icon to the group list ***
        grouped_list = [{
                'name': name, 
                'modules': sorted(modules, key=lambda m: m['name_singular']), 
                'icon': _get_group_icon(name)
            } for name, modules in groups.items()]
        
        sidebar_data[category] = {
            'groups': sorted(grouped_list, key=lambda g: g['name']),
            'orphans': sorted(orphans, key=lambda m: m['name_singular'])
        }
        
    sorted_sidebar_data = dict(sorted(sidebar_data.items()))

    return sorted_sidebar_data
