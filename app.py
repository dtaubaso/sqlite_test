import streamlit as st
import sqlite3
import uuid
from datetime import datetime
import pandas as pd


def create_table():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_record(value):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO records (value, timestamp) VALUES (?, ?)", (value, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_records():
    conn = sqlite3.connect("data.db")
    df = pd.read_sql_query("SELECT * FROM records ORDER BY timestamp DESC", conn)
    conn.close()
    return df if not df.empty else pd.DataFrame(columns=["id", "value", "timestamp"])

# Crear tabla si no existe
create_table()

st.title("SQLite Streamlit App")

# Botón para agregar UUID
if st.button("Agregar registro"):
    insert_record(str(uuid.uuid4()))
    st.success("UUID agregado con éxito!")

# Mostrar registros
st.subheader("Registros en la Base de Datos")
data = get_records()
if data.empty == False:
    st.table(data)
else:
    st.write("No hay registros aún.")