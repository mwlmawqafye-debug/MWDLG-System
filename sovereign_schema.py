
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

# --- 1. كيان المخطوطات ---
MANUSCRIPTS = {
    'slug': 'manuscripts',
    'name_singular': 'مخطوط',
    'name_plural': 'المخطوطات',
    'icon': """
        <svg class="h-12 w-12 text-[var(--color-waqf-green)]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
        </svg>
    """,
    'fields': {
        'title': {'label': 'العنوان', 'type': 'text', 'searchable': True, 'required': True},
        'author': {'label': 'المؤلف', 'type': 'text', 'searchable': True},
        'status': {'label': 'الحالة', 'type': 'select', 'options': ['متاح', 'قيد الترميم', 'خاص', 'مفقود'], 'required': True},
        'acquisition_date': {'label': 'تاريخ الحيازة', 'type': 'date'},
        'pages': {'label': 'عدد الصفحات', 'type': 'number'},
    }
}

# --- 2. كيان الوثائق ---
DOCUMENTS = {
    'slug': 'documents',
    'name_singular': 'وثيقة',
    'name_plural': 'الوثائق',
    'icon': """
        <svg class="h-12 w-12 text-[var(--color-ornament-gold)]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
    """,
    'fields': {
        'subject': {'label': 'الموضوع', 'type': 'text', 'searchable': True, 'required': True},
        'document_type': {'label': 'نوع الوثيقة', 'type': 'select', 'options': ['صك وقفي', 'مراسلات', 'سجل', 'إذن شرعي']},
        'issue_date': {'label': 'تاريخ الإصدار', 'type': 'date'},
        'is_archived': {'label': 'مؤرشفة', 'type': 'boolean'},
    }
}

# --- 3. كيان المكتبات ---
LIBRARIES = {
    'slug': 'libraries',
    'name_singular': 'مكتبة',
    'name_plural': 'المكتبات',
    'icon': """
        <svg class="h-12 w-12 text-[var(--color-sky-blue)]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0012 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75z" />
        </svg>
    """,
    'fields': {
        'name': {'label': 'اسم المكتبة', 'type': 'text', 'searchable': True, 'required': True},
        'location': {'label': 'الموقع', 'type': 'text', 'searchable': True},
        'collection_size': {'label': 'حجم المجموعة', 'type': 'number'},
    }
}

# --- 4. كيان الأوقاف ---
ENDOWMENTS = {
    'slug': 'endowments',
    'name_singular': 'وقف',
    'name_plural': 'الأوقاف',
    'icon': """
        <svg class="w-12 h-12 text-[#8a3ffc]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 11.25v8.25a1.5 1.5 0 01-1.5 1.5H5.25a1.5 1.5 0 01-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 1012 10.125A2.625 2.625 0 0012 4.875z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 10.125v1.875m-3.75-3.75H12a3.75 3.75 0 013.75 3.75v.375m-7.5 0V15a2.25 2.25 0 002.25 2.25H15M12 10.125c-1.354 0-2.599-.432-3.642-1.158a11.962 11.962 0 01-5.69-5.69A.656.656 0 012.25 2.25h19.5c.224 0 .424.123.541.317-.003.004-.006.007-.008.01a11.962 11.962 0 01-5.69 5.69c-1.043.726-2.288 1.158-3.642 1.158z" />
        </svg>
    """,
    'fields': {
        'name': {'label': 'اسم الوقف', 'type': 'text', 'searchable': True, 'required': True},
        'founder': {'label': 'الواقف', 'type': 'text', 'searchable': True},
        'endowment_type': {'label': 'نوع الوقف', 'type': 'select', 'options': ['ذري', 'خيري', 'مشترك']},
    }
}

# --- القائمة السيادية: تجميع كل الكيانات ---
# هذا هو المصدر الوحيد للقائمة الجانبية.
SOVEREIGN_ENTITIES = {
    'manuscripts': MANUSCRIPTS,
    'documents': DOCUMENTS,
    'libraries': LIBRARIES,
    'endowments': ENDOWMENTS,
}
