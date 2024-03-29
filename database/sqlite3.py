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
    cur.execute(f'''
                SELECT balance
                FROM account
                WHERE id = {account_id}
                ''')
    previous_balance = cur.fetchall()
    previous_balance = previous_balance[0][0]
    new_balance = previous_balance + amount
    cur.execute(f'''
                UPDATE account
                SET balance = {new_balance}
                WHERE id = {account_id}
                ''')
    conn.commit()


def edit_deal(conn: sqlite3.Connection, cur: sqlite3.Cursor,
              account_id: str, deal_id: int, amount: float,
              category_id: int, description: str | None) -> None:
    cur.execute(f'''
                UPDATE deal
                SET (amount, category_id, description) =
                ({amount}, '{category_id}', '{description}')
                WHERE id = {deal_id}
                ''')
    cur.execute(f'''
                SELECT amount
                FROM deal
                WHERE account_id = {account_id}
                ''')
    balance = 0
    amount_list = cur.fetchall()
    for i in amount_list:
        balance += i[0]
    cur.execute(f'''
                UPDATE account
                SET balance = {balance}
                WHERE id = {account_id}
                ''')
    conn.commit()


def create_category(conn: sqlite3.Connection, cur: sqlite3.Cursor,
                    name: str, description: str) -> None:
    cur.execute(f'''
                INSERT INTO category
                (name, description)
                VALUES ('{name}', '{description}')
                ''')
    conn.commit()


def edit_category(conn: sqlite3.Connection, cur: sqlite3.Cursor,
                  name: str, description: str, category_id: int) -> None:
    cur.execute(f'''
                UPDATE category
                SET (name, description) = ('{name}', '{description}')
                WHERE id = {category_id}
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
                SELECT deal.id, deal.amount, date(date), deal.description,
                category.name
                FROM deal INNER JOIN category
                ON deal.category_id = category.id
                WHERE account_id = {account_id}
                ORDER BY deal.id DESC
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
                FROM account
                ''')
    output = cur.fetchall()
    return output


def select_category_list(cur: sqlite3.Cursor) -> list:
    cur.execute(f'''
                SELECT *
                FROM category
                ''')
    output = cur.fetchall()
    return output


def close_db(conn: sqlite3.Connection,
             cur: sqlite3.Cursor) -> None:
    conn.commit()
    cur.close()
    conn.close()
