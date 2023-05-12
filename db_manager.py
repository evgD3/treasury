import psycopg2
import datetime


def init_db() -> tuple:
    conn = psycopg2.connect('dbname=treasurydb user=postgres')
    cur = conn.cursor()
    cur.execute(''' CREATE TABLE IF NOT EXISTS main_account
                    (id SERIAL PRIMARY KEY,
                    amount NUMERIC NOT NULL,
                    date DATE DEFAULT CURRENT_TIMESTAMP,
                    category VARCHAR (32) NOT NULL)''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS balance_table
                    (id SERIAL PRIMARY KEY,
                    balance NUMERIC NOT NULL)''')
    conn.commit()
    return conn, cur


def add_transaction(conn: psycopg2.extensions.connection,
                    cur: psycopg2.extensions.cursor,
                    amount: int, category: str) -> None:
    cur.execute(f'''INSERT INTO main_account (amount, category)
                    VALUES ({amount}, '{category}')''')
    conn.commit()


def select_by_date(cur: psycopg2.extensions.cursor,
                   from_date: datetime.date, to_date: datetime.date) -> list:
    cur.execute(f'''SELECT * FROM main_account
                    WHERE date>'{from_date}' AND date<'{to_date}'
                    ORDER BY id DESC''')
    output = cur.fetchall()
    return output


def select_groups(cur: psycopg2.extensions.cursor,
                  from_date: datetime.date, to_date: datetime.date) -> list:
    cur.execute(f'''SELECT category, SUM(amount) as grand_total
                    FROM main_account
                    WHERE date>'{from_date}' AND date<'{to_date}'
                    GROUP BY category
                    ORDER BY grand_total''')
    output = cur.fetchall()
    return output


def select_all(cur: psycopg2.extensions.cursor) -> list:
    cur.execute('''SELECT * FROM main_account
                   ORDER BY id DESC''')
    output = cur.fetchall()
    return output


def select_by_category(cur: psycopg2.extensions.cursor, category: str) -> list:
    cur.execute(f'''SELECT * FROM main_account
                    WHERE category = '{category}'
                    ORDER BY id DESC''')
    output = cur.fetchall()
    return output


def edit_transaction(conn: psycopg2.extensions.connection,
                     cur: psycopg2.extensions.cursor,
                     transaction_id: int, amount: int,
                     category: str) -> None:
    cur.execute(f'''UPDATE main_account
                    SET (amount, category) = ('{amount}', '{category}')
                    WHERE id = '{transaction_id}' ''')
    conn.commit()


def write_balance(conn: psycopg2.extensions.connection,
                  cur: psycopg2.extensions.cursor, balance: int) -> None:
    cur.execute(f'''INSERT INTO balance_table (balance)
                    VALUES ({balance})''')
    conn.commit()


def get_balance_list(cur: psycopg2.extensions.cursor) -> list:
    cur.execute('''SELECT * FROM balance_table
                   ORDER BY id DESC''')
    output = cur.fetchall()
    return output


def close_db(conn: psycopg2.extensions.connection,
             cur: psycopg2.extensions.cursor) -> None:
    conn.commit()
    cur.close()
    conn.close()
