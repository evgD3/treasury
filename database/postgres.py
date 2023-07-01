import psycopg2
import datetime


import psycopg2.extensions


def init_db() -> tuple:
    conn = psycopg2.connect('dbname=test_treasurydb user=postgres')
    cur = conn.cursor()
    return conn, cur


def create_account(conn: psycopg2.extensions.connection,
                   cur: psycopg2.extensions.cursor,
                   account_name: str) -> None:
    cur.execute(f'''
                CREATE TABLE {account_name}
                (id SERIAL PRIMARY KEY,
                currency VARCHAR (10) NOT NULL,
                amount REAL NOT NULL,
                date DATE DEFAULT CURRENT_TIMESTAMP,
                category VARCHAR (32) NOT NULL,
                comment VARCHAR (256) )
                ''')
    conn.commit()


def add_transaction(conn: psycopg2.extensions.connection,
                    cur: psycopg2.extensions.cursor,
                    account_name: str, currency: str,
                    amount: float, category: str, comment: str) -> None:
    cur.execute(f'''
                INSERT INTO {account_name}
                (currency, amount, category, comment)
                VALUES
                ('{currency}', {amount}, '{category}', '{comment}')
                ''')
    conn.commit()


def select_by_date(cur: psycopg2.extensions.cursor,
                   from_date: datetime.date, to_date: datetime.date,
                   account_name: str) -> list:
    cur.execute(f'''
                SELECT id, amount, date, category
                FROM {account_name}
                WHERE date>'{from_date}' AND date<'{to_date}'
                ORDER BY id DESC
                ''')
    output = cur.fetchall()
    return output


def select_groups(cur: psycopg2.extensions.cursor,
                  from_date: datetime.date, to_date: datetime.date,
                  account_name: str) -> list:
    cur.execute(f'''
                SELECT category, SUM(amount) as grand_total
                FROM {account_name}
                WHERE date>'{from_date}' AND date<'{to_date}'
                GROUP BY category
                ORDER BY grand_total
                ''')
    output = cur.fetchall()
    return output


def select_all(cur: psycopg2.extensions.cursor, account_name: str) -> list:
    cur.execute(f'''
                SELECT id, currency, amount, date, category
                FROM {account_name}
                ORDER BY id DESC
                ''')
    output = cur.fetchall()
    return output


def select_by_category(cur: psycopg2.extensions.cursor,
                       account_name: str, category: str) -> list:
    cur.execute(f'''
                SELECT id, amount, date, category
                FROM {account_name}
                WHERE category = '{category}'
                ORDER BY id DESC
                ''')
    output = cur.fetchall()
    return output


def edit_transaction(conn: psycopg2.extensions.connection,
                     cur: psycopg2.extensions.cursor,
                     account_name: str, transaction_id: int, amount: float,
                     category: str, comment: str) -> None:
    cur.execute(f'''
                UPDATE {account_name}
                SET (amount, category, comment) =
                ('{amount}', '{category}', '{comment}')
                WHERE id = '{transaction_id}'
                ''')
    conn.commit()


def close_db(conn: psycopg2.extensions.connection,
             cur: psycopg2.extensions.cursor) -> None:
    conn.commit()
    cur.close()
    conn.close()
