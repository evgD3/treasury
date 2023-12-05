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
from database.sqlite3 import select_category_list
from database.sqlite3 import select_groups

from printer import print_all
from printer import print_by_date
from printer import print_category
from printer import print_resent
from printer import print_stats


def cli_parce(argv: list) -> None:
    conn, cur = init_connection()
    accounts = select_account_list(cur)
    categories = select_category_list(cur)

    try:
        account_name = argv[1]
        action = argv[2]
    except IndexError:
        account_name = input('account > ').strip()
        action = input('action > ').strip()
    for i in accounts:
        if i[1] == account_name:
            account_id = i[0]
            account_cur = i[2]
            account_balance = i[3]
            account_description = i[4]
            break
        else:
            print(f'account "{account_name}" not exist')
            raise SystemExit

    if action in ('-p', '--print'):
        deals = select_all(cur, account_id)
        print_resent(account_name, account_cur, account_balance, deals)

    elif action in ('-a', '--add_deal'):
        try:
            amount = int(argv[3])
            category = argv[4]
            try:
                description = argv[5]
            except IndexError:
                description = None
        except IndexError:
            amount = int(input('amount > ').strip())
            category = input('category > ').strip()
            description = input('comment > ').strip()
        for i in categories:
            if category == i[1]:
                category_id = i[0]
                break
            else:
                print(f'category "{category}" not exist')
                raise SystemExit
        create_deal(conn, cur, account_id, amount, category_id, description)

    elif action in ('-e', '--edit_deal'):
        try:
            deal_id = argv[3]
            amount = argv[4]
            category = argv[5]
            try:
                description = argv[5]
            except IndexError:
                description = None
        except IndexError:
            deal_id = int(input('id > ').strip())
            amount = int(input('amount > ').strip())
            category = input('category > ').strip()
            description = input('comment > ').strip()
        for i in categories:
            if category == i[1]:
                category_id = i[0]
                break
            else:
                print(f'category "{category}" not exist')
                raise SystemExit
        edit_deal(conn, cur, account_id, deal_id, amount, category_id,
                  description)

    elif action in ('-pc', '--print_category'):
        try:
            category = argv[3]
        except IndexError:
            category = input('category > ').strip()
        for i in categories:
                if category == i[1]:
                    category_id = i[0]
                    break
                else:
                    print(f'category "{category}" not exist')
                    raise SystemExit
        deals = select_by_category(cur, account_id, category_id)
        print_category(account_name, category, account_cur, deals)

    elif action in ('-pm', '--print_month'):
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
        deals = select_by_date(cur, account_id, from_date, to_date)
        print_by_date(account_name, account_cur, from_date, to_date, deals)
                      
    elif action in ('-py', '--print_year'):
        year = datetime.date.today().year
        from_date = datetime.date.fromisoformat(f'{year}-01-01')
        to_date = datetime.date.fromisoformat(f'{year+1}-01-01')
        deals = select_by_date(cur, account_id, from_date, to_date)
        print_by_date(account_name, account_cur, from_date, to_date, deals)


    elif action in ('-pa', '--print_all'):
        deals = select_all(cur, account_id)
        print_all(account_name, account_cur, account_balance, deals)

    elif action in ('-ps', 'print_stats'):
        from_date = input('from (yyyy-mm-dd) > ').strip()
        from_date = datetime.date.fromisoformat(from_date)
        to_date = input('to (yyyy-mm-dd) > ').strip()
        to_date = datetime.date.fromisoformat(to_date)
        deals = select_by_date(cur, account_id, from_date, to_date)
        print_stats(account_name, account_cur, deals, from_date, to_date)

    elif action in ('-pms', '--print_month_stats'):
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
        deals = select_by_date(cur, account_id, from_date, to_date)
        print_stats(account_name, account_cur, deals, from_date, to_date)

    elif action in ('-pys', '--print_year_stats'):
        year = datetime.date.today().year
        from_date = datetime.date.fromisoformat(f'{year}-01-01')
        to_date = datetime.date.fromisoformat(f'{year+1}-01-01')
        deals = select_by_date(cur, account_id, from_date, to_date)
        print_stats(account_name, account_cur, deals, from_date, to_date)

    elif action in ('-pas', '--print_all_stats'):
        from_date = datetime.date.fromisoformat('1970-01-01')
        to_date = datetime.date.today()
        deals = select_by_date(cur, account_id, from_date, to_date)
        print_stats(account_name, account_cur, deals, from_date, to_date)


    elif action in ('-h', '--help'):
        print('''
        usage: treasury [account_name] [-action]

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
