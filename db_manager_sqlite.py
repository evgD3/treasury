import sqlite3
import datetime


def init_db() -> tuple:
    conn = sqlite3.connect('treasury_data.db')
    cur = conn.cursor()
    cur.execute(''' CREATE TABLE IF NOT EXISTS main_account
                    (id INTEGER PRIMARY KEY,
                    amount NUMERIC NOT NULL,
                    date DATE DEFAULT CURRENT_TIMESTAMP,
                    category VARCHAR (32) NOT NULL)''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS balance_table
                    (id INTEGER PRIMARY KEY,
                    balance NUMERIC NOT NULL)''')
    conn.commit()
    return conn, cur


def add_transaction(conn: sqlite3.Connection, cur: sqlite3.Cursor,
                    amount: int, category: str) -> None:
    cur.execute(f'''INSERT INTO main_account (amount, category)
                    VALUES ({amount}, '{category}')''')
    conn.commit()


def select_by_date(cur: sqlite3.Cursor,
                   from_date: datetime.date, to_date: datetime.date) -> list:
    cur.execute(f'''SELECT * FROM main_account
                    WHERE date>'{from_date}' AND date<'{to_date}'
                    ORDER BY id DESC''')
    output = cur.fetchall()
    return output


def select_all(cur: sqlite3.Cursor) -> list:
    cur.execute('''SELECT * FROM main_account
                   ORDER BY id DESC''')
    output = cur.fetchall()
    return output


def select_by_category(cur: sqlite3.Cursor, category: str) -> list:
    cur.execute(f'''SELECT * FROM main_account
                    WHERE category = '{category}'
                    ORDER BY id DESC''')
    output = cur.fetchall()
    return output

def edit_transaction(conn: sqlite3.Connection,
                     cur: sqlite3.Cursor,
                     transaction_id: int, amount: int,
                     category: str) -> None:
    cur.execute(f'''UPDATE main_account
                    WHERE id = '{transaction_id}'
                    SET (amount, category) = ({amount}, '{category}' ''')
    conn.commit()

def write_balance(conn,
                  cur, balance: int) -> None:
    cur.execute(f'''INSERT INTO balance_table (balance)
                    VALUES ({balance})''')
    conn.commit()

def get_balance_list(cur) -> list:
    cur.execute('''SELECT * FROM balance_table
                   ORDER BY id DESC''')
    output = cur.fetchall()
    return output

def close_db(conn,
             cur) -> None:
    conn.commit()
    cur.close()
    conn.close()
