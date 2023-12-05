import datetime

from database.sqlite3 import create_account
from database.sqlite3 import create_category
from database.sqlite3 import create_deal
from database.sqlite3 import close_db
from database.sqlite3 import edit_deal
from database.sqlite3 import init_connection
from database.sqlite3 import init_db
from database.sqlite3 import select_account_list
from database.sqlite3 import select_all
from database.sqlite3 import select_by_category
from database.sqlite3 import select_by_date
from database.sqlite3 import select_groups

from printer import print_all
from printer import print_by_date
from printer import print_category
from printer import print_resent
from printer import print_stats


def cli_parce(argv: list) -> None:
    conn, cur = init_connection()
    accounts = select_account_list(cur)

    try:
        account_name = argv[1]
        action = argv[2]
    except IndexError:
        account_name = input('account > ').strip()
        action = input('action > ').strip()
    for i in accounts:
        if i[1] == account_name:
            account_id = i[0]
            break
        else:
            print(f'account {account_name} not exist')
            raise SystemExit

    if action in ('-p', '--print'):
        print_resent(account, select_all(cur, account))

    elif action in ('-a', '--add_deal'):
        try:
            account_id = int(arg
            amount = int(argv[3])
            category = argv[4]
            try:
                comment = argv[5]
            except IndexError:
                comment = None
        except IndexError:
            amount = int(input('amount > ').strip())
            category = input('category > ').strip()
            comment = input('comment > ').strip()
        create_deal(conn, cur, account_id, amount, category_id, description)

    elif action == '-e':
        try:
            transaction_id = argv[3]
            amount = argv[4]
            category = argv[5]
            try:
                comment = argv[5]
            except IndexError:
                comment = None
        except IndexError:
            transaction_id = int(input('id> ').strip())
            amount = int(input('amount > ').strip())
            category = input('category > ').strip()
            comment = input('comment > ').strip()
        edit_transaction(conn, cur, account, transaction_id, amount,
                         category, comment)

    elif action == '-pc':
        try:
            category = argv[3]
        except IndexError:
            category = input('category > ').strip()
        print_category(account, select_by_category(cur, account, category))

    elif action == '-pm':
        now = datetime.date.today()
        year = now.year
        month = now.month
        if month < 10:
            from_date = datetime.date.fromisoformat(f'{year}-0{month}-01')
        else:
            from_date = datetime.date.fromisoformat(f'{year}-{month}-01')
        if month == 12:
            to_date = datetime.date.fromisoformat(f'{year+1}-01-01')
        else:
            if month < 9:
                to_date = datetime.date.fromisoformat(f'{year}-0{month+1}-01')
            else:
                to_date = datetime.date.fromisoformat(f'{year}-{month+1}-01')
        print_by_date(account, 
                      select_by_date(cur, account, from_date, to_date))

    elif action == '-py':
        year = datetime.date.today().year
        from_date = datetime.date.fromisoformat(f'{year}-01-01')
        to_date = datetime.date.fromisoformat(f'{year+1}-01-01')
        print_by_date(account,
                      select_by_date(cur, account, from_date, to_date))

    elif action == '-pa':
        print_all(account, select_all(cur, account))

    elif action == '-ps':
        from_date = input('from (yyyy-mm-dd) > ').strip()
        from_date = datetime.date.fromisoformat(from_date)
        to_date = input('to (yyyy-mm-dd) > ').strip()
        to_date = datetime.date.fromisoformat(to_date)
        print_stats(account, select_by_date(cur, account, from_date, to_date),
                    from_date, to_date)

    elif action == '-pms':
        now = datetime.date.today()
        year = now.year
        month = now.month
        if month < 10:
            from_date = datetime.date.fromisoformat(f'{year}-0{month}-01')
        else:
            from_date = datetime.date.fromisoformat(f'{year}-{month}-01')
        if month == 12:
            to_date = datetime.date.fromisoformat(f'{year+1}-01-01')
        else:
            if month < 9:
                to_date = datetime.date.fromisoformat(f'{year}-0{month+1}-01')
            else:
                to_date = datetime.date.fromisoformat(f'{year}-{month+1}-01')
        print_stats(account, select_by_date(cur, account, from_date, to_date),
                    from_date, to_date)

    elif action == '-pys':
        year = datetime.date.today().year
        from_date = datetime.date.fromisoformat(f'{year}-01-01')
        to_date = datetime.date.fromisoformat(f'{year+1}-01-01')
        print_stats(account, select_by_date(cur, account, from_date, to_date),
                    from_date, to_date)

    elif action == '-pas':
        from_date = datetime.date.fromisoformat('1970-01-01')
        to_date = datetime.date.today()
        print_stats(account, select_all(cur, account), from_date, to_date)

    elif action == '-h':
        print('''
        usage: treasury [-action]

        actions:
          -h                show this help message
          -p                print resent transactions
          -a                add transaction
          -pc [category]    print resent transactions for category
          -pm               print transactions for this month
          -py               print transactions for this year
          -pa               print all exist transactions
          -pms              print monthly statistic
          -pys              print yearly statistic
          -pas              print statistic by all time
              ''')

    else:
        print(f'invalid action "{action}"\ntry "-h" for help')

    close_db(conn, cur)
