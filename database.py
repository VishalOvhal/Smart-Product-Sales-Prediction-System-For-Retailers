import sqlite3
import pandas as pd
import streamlit as st
import os


def get_db_connection():
    return sqlite3.connect('inventory.db')



# Product Table Functions

def create_product_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            ITEM_ID TEXT PRIMARY KEY,
            ITEM_Name TEXT NOT NULL,
            ITEM_Weight REAL,
            ITEM_fat_content TEXT,
            ITEM_Type TEXT,
            ITEM_MRP REAL,
            ITEM_details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_product(item_id, name, weight, fat, type, mrp, details):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO products VALUES (?,?,?,?,?,?,?)
    ''', (item_id, name, weight, fat, type, mrp, details))
    conn.commit()
    conn.close()

def update_product(item_id, item_name, item_weight, item_fat, item_type, item_mrp, item_details):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE products SET
                          ITEM_Name = ?,
                          ITEM_Weight = ?,
                          ITEM_fat_content = ?,
                          ITEM_Type = ?,
                          ITEM_MRP = ?,
                          ITEM_details = ?
                          WHERE ITEM_ID = ?''',
                       (item_name, item_weight, item_fat, item_type, item_mrp, item_details, item_id))
    conn.commit()
    conn.close()


def get_product():
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM products', conn)
    conn.close()
    return df

def delete_product(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE ITEM_ID = ?', (item_id,))
    conn.commit()
    conn.close()

def clear_product():
    conn = get_db_connection()
    conn.execute('DELETE FROM products')
    conn.commit()
    conn.close()




# Supplier Table Functions

def create_supplier_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS supplier (
                        Supplier_ID TEXT PRIMARY KEY,
                        Supplier_Name TEXT NOT NULL,
                        Contact_Number TEXT,
                        Email TEXT,
                        Address TEXT
                      )''')
    conn.commit()
    conn.close()

def add_supplier(sup_id, name, contact, email, address):
    conn =  get_db_connection()
    conn.execute('''INSERT OR IGNORE INTO supplier
                (Supplier_ID, Supplier_Name, Contact_Number, Email, Address)
                VALUES (?, ?, ?, ?, ?)''',(sup_id, name, contact, email, address))
    conn.commit()
        

def get_supplier() -> pd.DataFrame:
    conn = get_db_connection()
    query = "SELECT * FROM supplier ORDER BY Supplier_ID"
    df = pd.read_sql_query(query, conn)
    return df

def update_supplier(sup_id, name, contact, email, address):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE supplier SET
                          Supplier_Name = ?,
                          Contact_Number = ?,
                          Email = ?,
                          Address = ?
                          WHERE Supplier_ID = ?''',
                       (name, contact, email, address, sup_id))
    conn.commit()
    conn.close()
        
def delete_supplier(sup_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM supplier WHERE Supplier_ID = ?', (sup_id,))
    conn.commit()
    conn.close()






# Item Supply Functions

def create_item_stock_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS item_supply_stock (
            ITEM_ID TEXT,
            Supplier_ID TEXT,
            ITEM_Stocks INTEGER,
            mfd DATE,
            exp DATE,
            FOREIGN KEY(ITEM_ID) REFERENCES products(ITEM_ID),
            FOREIGN KEY(Supplier_ID) REFERENCES suppliers(Supplier_ID)
        )
    ''')
    conn.commit()
    conn.close()


def add_supply_info(item_id, sup_id, stocks, mfd, exp):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO item_supply_stock VALUES (?,?,?,?,?)
    ''', (item_id, sup_id, stocks, mfd, exp))
    conn.commit()
    conn.close()


def update_supply_info(item_id, stocks, mfd, exp):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE item_supply_stock SET
                          ITEM_Stocks = ?,
                          mfd = ?,
                          exp = ?
                          WHERE ITEM_ID = ?''',
                       (stocks, mfd, exp, item_id))
    conn.commit()
    conn.close()


def delete_supply_info(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM item_supply_stock WHERE ITEM_ID = ?', (item_id,))
    conn.commit()
    conn.close()


def get_supply_info():
    conn = get_db_connection()
    df = pd.read_sql('''
        SELECT p.ITEM_ID, p.ITEM_Name, s.Supplier_ID, s.Supplier_Name, i.ITEM_Stocks, i.mfd, i.exp 
        FROM item_supply_stock i
        JOIN products p ON i.ITEM_ID = p.ITEM_ID
        JOIN supplier s ON i.Supplier_ID = s.Supplier_ID
    ''', conn)
    conn.close()
    return df





# user authentication

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    columns = [column[0] for column in cursor.description]
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return dict(zip(columns, user))
    return None

def create_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True