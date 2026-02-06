import sqlite3
import sovereign_schema

DATABASE_FILE = "sovereign.db"

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Dynamically creates tables based on the SOVEREIGN_SCHEMA."""
    conn = get_db_connection()
    cursor = conn.cursor()
    type_mapping = {
        "text": "TEXT",
        "textarea": "TEXT",
        "date": "TEXT",
        "number": "INTEGER",
        "relation": "INTEGER",
    }
    for entity_slug, entity_props in sovereign_schema.SOVEREIGN_ENTITIES.items():
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
        for field_name, field_props in entity_props['fields'].items():
            column_type = type_mapping.get(field_props['type'], "TEXT")
            columns.append(f"{field_name} {column_type}")
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {entity_slug} ({', '.join(columns)});"
        cursor.execute(create_table_sql)
    conn.commit()
    conn.close()

def get_all_for_entity(entity_slug):
    """Fetches all records for a given entity."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {entity_slug}")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_one_for_entity(entity_slug, record_id):
    """Fetches a single record for a given entity by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {entity_slug} WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def insert_entity(entity_slug, data):
    """Inserts a new record for a given entity."""
    conn = get_db_connection()
    cursor = conn.cursor()

    columns = data.keys()
    placeholders = ["?" for _ in columns]
    values = list(data.values())

    sql = f"INSERT INTO {entity_slug} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
    
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def update_entity(entity_slug, record_id, data):
    """Updates a record for a given entity."""
    conn = get_db_connection()
    cursor = conn.cursor()

    set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
    values = list(data.values()) + [record_id]

    sql = f"UPDATE {entity_slug} SET {set_clause} WHERE id = ?"

    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def delete_entity(entity_slug, record_id):
    """Deletes a record from a given entity table by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = f"DELETE FROM {entity_slug} WHERE id = ?"
    
    cursor.execute(sql, (record_id,))
    conn.commit()
    conn.close()
