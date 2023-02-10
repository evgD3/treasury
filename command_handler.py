import datetime

from db_manager import init_db
from db_manager import add_transaction
from db_manager import select_all
from db_manager import select_by_category
from db_manager import select_by_date

from printer import print_category
from printer import print_resent
from printer import print_by_date


def command(argv: list) -> None:
    conn, cur = init_db()

    try:
        action = argv[1]
    except IndexError:
        action = input('action > ').strip()

    if action == 'p':
        print_resent(select_all(cur))

    if action == 'a':
        try:
            amount = argv[2]
        except IndexError:
            amount = int(input('amount> ').strip())
        try:
            category = argv[3]
        except IndexError:
            category = input('category> ').strip()
        add_transaction(conn, cur, amount, category)

    if action == 'pc':
        try:
            category = argv[2]
        except IndexError:
            category = input('category> ').strip()
        print_category(select_by_category(cur, category))

    if action == 'pm':
        now = datetime.date.today()
        year = now.year
        month = now.month
        #from_date = datetime.date.fromisoformat(f'{year}-{month}-01')
        from_date = (f'{year}-{month}-01')
        if month == 12:
            to_date = (f'{year+1}-01-01')
            #to_date = datetime.date.fromisoformat(f'{year+1}-01-01')
        else:
            #to_date = datetime.date.fromisoformat(f'{year}-{month+1}-01')
            to_date = (f'{year}-{month+1}-01')
        print_by_date(select_by_date(cur, from_date, to_date))
