import sqlite3
import datetime


def init_db() -> tuple:
    conn = sqlite3.connect('treasury_data.db')
    cur = conn.cursor()
    return conn, cur


def create_account(conn: sqlite3.Connection, cur: sqlite3.Cursor,
                   account_name: str) -> None:
    cur.execute(f'''
                CREATE TABLE {account_name}
                (id INTEGER PRIMARY KEY,
                currency VARCHAR (10) NOT NULL,
                amount REAL NOT NULL,
                date DATE DEFAULT CURRENT_TIMESTAMP,
                category VARCHAR (32) NOT NULL,
                comment VARCHAR (256) )
                ''')
    conn.commit()


def add_transaction(conn: sqlite3.Connection, cur: sqlite3.Cursor,
                    account_name: str, currency: str,
                    amount: float, category: str, comment: str|None) -> None:
    cur.execute(f'''
                INSERT INTO {account_name}
                (currency, amount, category, comment)
                VALUES ('{currency}', {amount}, '{category}', '{comment}')
                ''')
    conn.commit()


def select_by_date(cur: sqlite3.Cursor, account_name: str,
                   from_date: datetime.date, to_date: datetime.date) -> list:
    cur.execute(f'''
                SELECT id, amount, currency, date(date), category
                FROM {account_name}
                WHERE date>'{from_date}' AND date<'{to_date}'
                ORDER BY id DESC
                ''')
    output = cur.fetchall()
    return output


def select_groups(cur: sqlite3.Cursor, from_date: datetime.date,
                  to_date: datetime.date, account_name: str) -> list:
    cur.execute(f'''
                SELECT category, SUM(amount) as grand_total
                FROM {account_name}
                WHERE date>'{from_date}' AND date<'{to_date}'
                GROUP BY category
                ORDER BY grand_total
                ''')
    output = cur.fetchall()
    return output


def select_all(cur: sqlite3.Cursor, account_name: str) -> list:
    cur.execute(f'''
                SELECT id, currency, amount, date(date), category
                FROM {account_name}
                ORDER BY id DESC
                ''')
    output = cur.fetchall()
    return output


def select_by_category(cur: sqlite3.Cursor, account_name: str,
                       category: str) -> list:
    cur.execute(f'''
                SELECT id, amount, date(date), category, currency
                FROM {account_name}
                WHERE category = '{category}'
                ORDER BY id DESC
                ''')
    output = cur.fetchall()
    return output


def edit_transaction(conn: sqlite3.Connection, cur: sqlite3.Cursor,
                     account_name: str, transaction_id: int, amount: float,
                     category: str, comment: str|None) -> None:
    cur.execute(f'''
                UPDATE {account_name}
                SET (amount, category, comment) =
                ({amount}, '{category}', '{comment}')
                WHERE id = {transaction_id}''')
    conn.commit()


def close_db(conn: sqlite3.Connection,
             cur: sqlite3.Cursor) -> None:
    conn.commit()
    cur.close()
    conn.close()
