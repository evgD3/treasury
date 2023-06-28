import sqlite3
import datetime


def init_db() -> tuple:
    conn = sqlite3.connect('treasury_data.db')
    cur = conn.cursor()
    conn.commit()
    return conn, cur


def create_account(conn: sqlite3.Connection, cur: sqlite3.Cursor,
                   account_name: str) -> None:
    cur.execute(f'''CREATE TABLE {account_name}
                   (id INTEGER PRIMARY KEY,
                    currency VARCHAR (10) NOT NULL,
                    amount REAL NOT NULL,
                    category VARCHAR (32) NOT NULL,
                    comment VARCHAR (256) NOT NULL)''')
    conn.commit()


def add_transaction(conn: sqlite3.Connection, cur: sqlite3.Cursor,
                    amount: int, category: str) -> None:
    cur.execute(f'''INSERT INTO main_account (amount, category)
                    VALUES ({amount}, '{category}')''')
    conn.commit()


def select_by_date(cur: sqlite3.Cursor,
                   from_date: datetime.date, to_date: datetime.date) -> list:
    cur.execute(f'''SELECT id, amount, date(date), category
                    FROM main_account
                    WHERE date>'{from_date}' AND date<'{to_date}'
                    ORDER BY id DESC''')
    output = cur.fetchall()
    return output


def select_groups(cur: sqlite3.Cursor, 
                 from_date: datetime.date, to_date: datetime.date) -> list:
    cur.execute(f'''SELECT category, SUM(amount) as grand_total
                    FROM main_account
                    WHERE date>'{from_date}' AND date<'{to_date}'
                    GROUP BY category
                    ORDER BY grand_total''')
    output = cur.fetchall()
    return output


def select_all(cur: sqlite3.Cursor) -> list:
    cur.execute('''SELECT id, amount, date(date), category
                   FROM main_account
                   ORDER BY id DESC''')
    output = cur.fetchall()
    return output


def select_by_category(cur: sqlite3.Cursor, category: str) -> list:
    cur.execute(f'''SELECT id, amount, date(date), category
                    FROM main_account
                    WHERE category = '{category}'
                    ORDER BY id DESC''')
    output = cur.fetchall()
    return output

def edit_transaction(conn: sqlite3.Connection,
                     cur: sqlite3.Cursor,
                     transaction_id: int, amount: int,
                     category: str) -> None:
    cur.execute(f'''UPDATE main_account
                    SET (amount, category) = ({amount}, '{category}')
                    WHERE id = {transaction_id}''')
    conn.commit()

def write_balance(conn: sqlite3.Connection,
                  cur: sqlite3.Cursor, balance: int) -> None:
    cur.execute(f'''INSERT INTO balance_table (balance)
                    VALUES ({balance})''')
    conn.commit()

def get_balance_list(cur: sqlite3.Cursor) -> list:
    cur.execute('''SELECT * FROM balance_table
                   ORDER BY id DESC''')
    output = cur.fetchall()
    return output

def close_db(conn: sqlite3.Connection,
             cur: sqlite3.Cursor) -> None:
    conn.commit()
    cur.close()
    conn.close()
