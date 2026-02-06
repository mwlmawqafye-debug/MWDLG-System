
"""
================================
المخطط السيادي (The Sovereign Schema)
================================
هذا الملف هو دستور النظام وهيكله المركزي.
إنه يمثل فلسفة "النظام المُسيَّر بالبيانات الوصفية" (Metadata-Driven System).
أي تعديل هنا ينعكس تلقائيًا على كامل النظام.
"""
from collections import defaultdict

# --- 1. تعريف الكيانات ---

IDENTITY_AND_APPEARANCE = {
    'slug': 'identity-manager', # Must match the route in app.py
    'name_singular': 'الهوية والمظهر',
    'name_plural': 'إدارة الهوية والمظهر',
    'category': 'إعداد النظام',
    'group': 'المظهر العام',
    'icon': '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9.53 16.122a3 3 0 00-5.78 1.128 2.25 2.25 0 01-2.4 2.245 4.5 4.5 0 008.4-2.245c0-.399-.078-.78-.22-1.128zm0 0a15.998 15.998 0 003.388-1.62m-5.043-.025a15.998 15.998 0 011.622-3.385m5.043.025a15.998 15.998 0 001.622-3.385m-3.385 5.043a15.998 15.998 0 01-1.622 3.385m3.385-5.043a15.998 15.998 0 00-3.388 1.62m-1.62-3.385a15.998 15.998 0 013.388-1.62" /></svg>''',
    'fields': {} # This is a special page, no dynamic fields needed for forms.
}

WORK_TASK_CLASSIFICATIONS = {
    'slug': 'work-task-classifications',
    'name_singular': 'تصنيف مهمة عمل',
    'name_plural': 'تصنيفات أنواع مهام العمل',
    'add_button_label': 'إضافة تصنيف',
    'category': 'إعداد النظام',
    'group': 'المهام والمسميات الوظيفية',
    'icon': '''<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>''',
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
    'icon': '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" /></svg>''',
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
    'icon': '''<svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>''',
    'fields': {
        'subject': {'label': 'الموضوع', 'type': 'text', 'searchable': True, 'required': True},
        'document_type': {'label': 'نوع الوثيقة', 'type': 'select', 'options': ['صك وقفي', 'مراسلات', 'سجل', 'إذن شرعي']},
        'issue_date': {'label': 'تاريخ الإصدار', 'type': 'date'},
        'is_archived': {'label': 'مؤرشفة', 'type': 'boolean'},
    }
}

# --- 2. القائمة السيادية: المصدر الوحيد للحقيقة ---
SOVEREIGN_ENTITIES = {
    # إعداد النظام
    'identity-manager': IDENTITY_AND_APPEARANCE,
    'work-task-classifications': WORK_TASK_CLASSIFICATIONS,
    # البيانات الأساسية
    'manuscripts': MANUSCRIPTS,
    'documents': DOCUMENTS,
}

# --- 3. المعالجة في الخلفية: بناء هيكل القائمة الجانبية الديناميكي ---
def get_sidebar_structure():
    """
    يعالج `SOVEREIGN_ENTITIES` الخام ويحوله إلى هيكل بيانات منظم جاهز للعرض في القالب.
    يقوم بتجميع الكيانات حسب الفئة (category)، ثم حسب المجموعة (group) داخل كل فئة.
    """
    # الخطوة 1: تجميع كل الكيانات حسب 'category'
    categorized_entities = defaultdict(list)
    for slug, entity in SOVEREIGN_ENTITIES.items():
        # التأكد من أن الكيان لديه slug، وهو أمر حاسم لتوليد الروابط
        entity['slug'] = slug
        category = entity.get('category', 'عام') # فئة افتراضية
        categorized_entities[category].append(entity)

    # الخطوة 2: معالجة كل فئة لإنشاء مجموعات والعثور على الكيانات "اليتيمة"
    sidebar_data = {}
    for category, entities_in_cat in categorized_entities.items():
        groups = defaultdict(list)
        orphans = []
        for entity in entities_in_cat:
            if entity.get('group'):
                groups[entity['group']].append(entity)
            else:
                orphans.append(entity)

        # الخطوة 3: تحويل قاموس 'groups' إلى قائمة لسهولة التكرار في Jinja وفرزها أبجديًا
        grouped_list = [{'name': name, 'modules': sorted(modules, key=lambda m: m['name_singular'])}
                        for name, modules in groups.items()]
        
        sidebar_data[category] = {
            'groups': sorted(grouped_list, key=lambda g: g['name']),
            'orphans': sorted(orphans, key=lambda m: m['name_singular'])
        }
        
    # فرز الفئات النهائية لضمان ترتيب ثابت
    sorted_sidebar_data = dict(sorted(sidebar_data.items()))

    return sorted_sidebar_data
