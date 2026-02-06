
"""
================================
المخطط السيادي (The Sovereign Schema)
================================
هذا الملف هو دستور النظام وهيكله المركزي.
إنه يمثل فلسفة "النظام المُسيَّر بالبيانات الوصفية" (Metadata-Driven System).

كل كائن هنا يمثل "كيانًا" سياديًا في النظام. الخصائص المعرفة هنا
تستخدمها "الوحدات الكلية" (Macros) في قوالب Jinja لبناء الواجهات ديناميكيًا،
من جداول البيانات إلى نماذج الإضافة وأشرطة التصفية.

أي تعديل هنا (مثل إضافة حقل جديد) ينعكس تلقائيًا على كامل النظام
دون الحاجة لتعديل ملفات HTML بشكل يدوي.
"""

# --- 1. كيانات إعداد النظام ---

WORK_TASK_CLASSIFICATIONS = {
    'slug': 'work-task-classifications',
    'name_singular': 'تصنيف مهمة عمل',
    'name_plural': 'تصنيفات أنواع مهام العمل',
    'add_button_label': 'إضافة تصنيف',
    'category': 'إعداد النظام',
    'group': 'المهام والمسميات الوظيفية',
    'color': 'var(--color-stone-gray)', 
    'icon_class': 'text-gray-500', # Using a neutral color for now
    'icon': '''<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>''',
    'fields': {
        'classification_name': {'label': 'اسم التصنيف', 'type': 'text', 'required': True},
        'task_definition': {'label': 'تعريف مختصر عن المهمة', 'type': 'textarea', 'required': True, 'rows': 3},
        'notes': {'label': 'ملاحظات', 'type': 'textarea'}
    }
}

# --- 2. كيانات البيانات الأساسية ---

MANUSCRIPTS = {
    'slug': 'manuscripts',
    'name_singular': 'مخطوط',
    'name_plural': 'المخطوطات',
    'add_button_label': 'إضافة مخطوط',
    'category': 'البيانات الأساسية',
    'group': 'الكيانات الرئيسية',
    'color': 'var(--color-waqf-green)',
    'icon_class': 'text-[var(--color-waqf-green)]',
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
    'color': 'var(--color-ornament-gold)',
    'icon_class': 'text-[var(--color-ornament-gold)]',
    'icon': '''<svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>''',
    'fields': {
        'subject': {'label': 'الموضوع', 'type': 'text', 'searchable': True, 'required': True},
        'document_type': {'label': 'نوع الوثيقة', 'type': 'select', 'options': ['صك وقفي', 'مراسلات', 'سجل', 'إذن شرعي']},
        'issue_date': {'label': 'تاريخ الإصدار', 'type': 'date'},
        'is_archived': {'label': 'مؤرشفة', 'type': 'boolean'},
    }
}

LIBRARIES = {
    'slug': 'libraries',
    'name_singular': 'مكتبة',
    'name_plural': 'المكتبات',
    'add_button_label': 'إضافة مكتبة',
    'category': 'البيانات الأساسية',
    'group': 'الكيانات الرئيسية',
    'color': 'var(--color-sky-blue)',
    'icon_class': 'text-[var(--color-sky-blue)]',
    'icon': '''<svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0012 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75z" /></svg>''',
    'fields': {
        'name': {'label': 'اسم المكتبة', 'type': 'text', 'searchable': True, 'required': True},
        'location': {'label': 'الموقع', 'type': 'text', 'searchable': True},
        'collection_size': {'label': 'حجم المجموعة', 'type': 'number'},
    }
}

ENDOWMENTS = {
    'slug': 'endowments',
    'name_singular': 'وقف',
    'name_plural': 'الأوقاف',
    'add_button_label': 'إضافة وقف',
    'category': 'البيانات الأساسية',
    'group': 'الكيانات الرئيسية',
    'color': '#8a3ffc',
    'icon_class': 'text-[#8a3ffc]',
    'icon': '''<svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21 11.25v8.25a1.5 1.5 0 01-1.5 1.5H5.25a1.5 1.5 0 01-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 1012 10.125A2.625 2.625 0 0012 4.875z" /><path stroke-linecap="round" stroke-linejoin="round" d="M12 10.125v1.875m-3.75-3.75H12a3.75 3.75 0 013.75 3.75v.375m-7.5 0V15a2.25 2.25 0 002.25 2.25H15M12 10.125c-1.354 0-2.599-.432-3.642-1.158a11.962 11.962 0 01-5.69-5.69A.656.656 0 012.25 2.25h19.5c.224 0 .424.123.541.317-.003.004-.006.007-.008.01a11.962 11.962 0 01-5.69 5.69c-1.043.726-2.288 1.158-3.642 1.158z" /></svg>''',
    'fields': {
        'name': {'label': 'اسم الوقف', 'type': 'text', 'searchable': True, 'required': True},
        'founder': {'label': 'الواقف', 'type': 'text', 'searchable': True},
        'endowment_type': {'label': 'نوع الوقف', 'type': 'select', 'options': ['ذري', 'خيري', 'مشترك']},
    }
}

# --- القائمة السيادية: تجميع كل الكيانات ---
# هذا هو المصدر الوحيد للقائمة الجانبية.
SOVEREIGN_ENTITIES = {
    # إعداد النظام
    'work-task-classifications': WORK_TASK_CLASSIFICATIONS,
    # البيانات الأساسية
    'manuscripts': MANUSCRIPTS,
    'documents': DOCUMENTS,
    'libraries': LIBRARIES,
    'endowments': ENDOWMENTS,
}

# --- الهيكل الهرمي للقائمة الجانبية (للتوليد الديناميكي) ---
# يتم إنشاؤه من القائمة السيادية أعلاه
def get_sidebar_structure():
    structure = {}
    for slug, entity in SOVEREIGN_ENTITIES.items():
        category = entity.get('category', 'عام')
        group = entity.get('group', 'عام')
        if category not in structure:
            structure[category] = {}
        if group not in structure[category]:
            structure[category][group] = []
        structure[category][group].append(entity)
    return structure
