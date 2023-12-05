import sqlite3
import datetime


def init_connection() -> tuple:
    conn = sqlite3.connect('tt.db')
    cur = conn.cursor()
    return conn, cur


def init_db(conn: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    cur.execute('''CREATE TABLE account
                (id INTEGER PRIMARY KEY,
                name VARCHAR(128) NOT NULL,
                currency VARCHAR(10) NOT NULL,
                balance REAL NOT NULL,
                description VARCHAR(255) )
                ''')
    cur.execute('''CREATE TABLE category
                (id INTEGER PRIMARY KEY,
                name VARCHAR(64) NOT NULL,
                description VARCHAR(512) )
                ''')
    cur.execute('''CREATE TABLE deal
                (id INTEGER PRIMARY KEY,
                amount REAL NOT NULL,
                date DATE DEFAULT CURRENT_TIMESTAMP,
                description VARCHAR(256),
                account_id INTEGER,
                category_id INTEGER,
                FOREIGN KEY(account_id) REFERENCES account(id),
                FOREIGN KEY(category_id) REFERENCES category(id) )
                ''')
    conn.commit()


def create_account(conn: sqlite3.Connection, cur: sqlite3.Cursor,
                   account_name: str, currency: str,
                   description: str | None) -> None:
    cur.execute(f'''
                INSERT INTO account
                (name, currency, balance, description)
                VALUES ('{account_name}', '{currency}', '0.0', 
                '{description}')
                ''')
    conn.commit()


def create_deal(conn: sqlite3.Connection, cur: sqlite3.Cursor,
                account_id: int, amount: float, category_id: int,
                description: str | None) -> None:
    cur.execute(f'''
                INSERT INTO deal
                (account_id, amount, category_id, description)
                VALUES ('{account_id}', {amount}, '{category_id}', 
                '{description}')
                ''')
    conn.commit()


def edit_deal(conn: sqlite3.Connection, cur: sqlite3.Cursor,
              account_name: str, deal_id: int, amount: float,
              category: str, comment: str | None) -> None:
    cur.execute(f'''
                UPDATE {account_name}
                SET (amount, category, comment) =
                ({amount}, '{category}', '{comment}')
                WHERE id = {deal_id}''')
    conn.commit()


def create_category(conn: sqlite3.Connection, cur: sqlite3.Cursor,
                    name: str, description: str) -> None:
    cur.execute(f'''
                INSERT INTO category
                (name, description)
                VALUES ('{name}', '{description}')
                ''')
    conn.commit()


def select_by_date(cur: sqlite3.Cursor, account_id: int,
                   from_date: datetime.date, to_date: datetime.date) -> list:
    cur.execute(f'''
                SELECT deal.id, deal.amount, date(date), category.name
                FROM deal INNER JOIN category
                ON deal.category_id = category.id
                WHERE account_id = '{account_id}' AND
                date>'{from_date}' AND date<'{to_date}'
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


def select_all(cur: sqlite3.Cursor, account_id: int) -> list:
    cur.execute(f'''
                SELECT id, amount, date(date), description, category_id
                FROM deal
                WHERE account_id = {account_id}
                ORDER BY id DESC
                ''')
    output = cur.fetchall()
    return output


def select_by_category(cur: sqlite3.Cursor, account_id: int,
                       category_id: int) -> list:
    cur.execute(f'''
                SELECT id, amount, date(date), description
                FROM deal
                WHERE account_id = {account_id}
                AND category_id = {category_id}
                ORDER BY id DESC
                ''')
    output = cur.fetchall()
    return output


def select_account_list(cur: sqlite3.Cursor) -> list:
    cur.execute(f'''
                SELECT *
                from account
                ''')
    output = cur.fetchall()
    return output

def select_category_list(cur: sqlite3.Cursor) -> list:
    cur.execute(f'''
                SELECT *
                from category
                ''')
    output = cur.fetchall()
    return output


def close_db(conn: sqlite3.Connection,
             cur: sqlite3.Cursor) -> None:
    conn.commit()
    cur.close()
    conn.close()
