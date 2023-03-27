import datetime

from db_manager import add_transaction
from db_manager import close_db
from db_manager import edit_transaction
from db_manager import get_balance_list
from db_manager import init_db
from db_manager import select_all
from db_manager import select_by_category
from db_manager import select_by_date
from db_manager import write_balance

from printer import print_all
from printer import print_by_date
from printer import print_category
from printer import print_resent


def command(argv: list) -> None:
    conn, cur = init_db()
    
    try:
        action = argv[1]
    except IndexError:
        action = input('action > ').strip()

    if action == '-p':
        print_resent(select_all(cur), get_balance_list(cur))

    elif action == '-a':
        try:
            amount = int(argv[2])
        except IndexError:
            amount = int(input('amount> ').strip())
        try:
            category = argv[3]
        except IndexError:
            category = input('category> ').strip()
        add_transaction(conn, cur, amount, category)
        balance = get_balance_list(cur)
        new_balance = balance[0][1] + amount
        write_balance(conn, cur, new_balance)

    elif action == '-e':
        try:
            transaction_id = argv[2]
        except IndexError:
            transaction_id = int(input('id> ').strip())
        try:
            amount = argv[3]
        except IndexError:
            amount = int(input('amount> ').strip())
        try:
            category = argv[4]
        except IndexError:
            category = input('category> ').strip()
        edit_transaction(conn, cur, transaction_id, amount, category)


    elif action == '-pc':
        try:
            category = argv[2]
        except IndexError:
            category = input('category> ').strip()
        print_category(select_by_category(cur, category))

    elif action == '-pm':
        now = datetime.date.today()
        year = now.year
        month = now.month
        from_date = (f'{year}-{month}-01')
        if month == 12:
            to_date = (f'{year+1}-01-01')

        else:
            to_date = (f'{year}-{month+1}-01')
        print_by_date(select_by_date(cur, from_date, to_date))

    elif action == '-py':
        year = datetime.date.today().year
        from_date = f'{year}-01-01'
        to_date = f'{year+1}-01-01'
        print_by_date(select_by_date(cur, from_date, to_date))

    elif action == '-pa':
        print_all(select_all(cur), get_balance_list(cur))

    elif action == '-h':
        print(f'''
        usage: treasury [-action]

        actions:
          -h                show this help message
          -p                print resent transactions
          -a                add transaction
          -pc [category]    print resent transactions for category
          -pm               print transactions for this month
          -py               print transactions for this year
              ''')

    elif action == '-pms':
        now = datetime.date.today()
        year = now.year
        month = now.month
        from_date = (f'{year}-{month}-01')
        if month == 12:
            to_date = (f'{year+1}-01-01')

        else:
            to_date = (f'{year}-{month+1}-01')
        print_stats(select_by_date(cur, from_date, to_date))

    else:
        print(f'invalid action "{action}"\ntry "-h" for help')
    
    close_db(conn, cur)
