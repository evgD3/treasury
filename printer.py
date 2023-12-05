import datetime


def print_resent(account_name: str, account_cur: str,
                 account_balance, deals: list) -> None:
    deals = deals[:10]
    print(f'ACCOUNT  {account_name}  {account_balance}')
    print(f'\033[34m[{"id":<5}][{"CUR":<4}][{"amount":<9}]'
          f'[{"date":<11}][{"type":<15}]')
    for i in deals:
        if i[2] > 0:
            print(f'\033[92m[{i[0]:<5}][{account_cur:<4}]'
                  f'[{i[1]:<9}][{i[2]} ][{i[3]:<15}]')
        else:
            print(f'\033[31m[{i[0]:<5}][{account_cur:<4}]'
                  f'[{i[1]:<9}][{i[2]} ][{i[3]:<15}]')



def print_all(account_name: str, account_cur,
              account_balance: str, deals: list) -> None:
    income = 0
    costs = 0
    for i in deals:
        if i[2] > 0:
            income += i[2]
        else:
            costs += i[2]
    print(f'ACCOUNT  {account_name}  {account_balance}')
    print(f'\033[92mINCOME: {income} '
          f'\033[91mCOSTS: {costs}')
    print(f'\033[34m[{"id":<5}][{"CUR":<4}][{"amount":<9}]'
          f'[{"date":<11}][{"type":<15}]')
    for i in deals:
        if i[2] > 0:
            print(f'\033[92m[{i[0]:<5}][{account_cur:<4}]'
                  f'[{i[1]:<9}][{i[2]} ][{i[3]:<15}]')
        else:
            print(f'\033[31m[{i[0]:<5}][{account_cur:<4}]'
                  f'[{i[1]:<9}][{i[2]} ][{i[3]:<15}]')


def print_category(account_name: str, category_name: str,
                   account_cur: str, deals: list) -> None:
    ALL = 0
    print(f'ACCOUNT  {account_name}  {category_name}')
    for i in deals:
        ALL += i[1]
    if ALL > 0:
        print(f'\033[92mALL {ALL}')
    else:
        print(f'\033[91mALL {ALL}')
    print(f'\033[95m[{"type":<15}][{"date":<11}]'
          f'[{"amount":<9}][{"CUR":<4}][{"id":<5}]')
    for i in deals:
        if i[1] > 0:
            print(f'\033[92m[{category_name:<15}][{i[2]} ]'
                  f'[{i[1]:<9}][{account_cur:<4}][{i[0]:<5}]')
        else:
            print(f'\033[91m[{category_name:<15}][{i[2]} ]'
                  f'[{i[1]:<9}][{account_cur:<4}][{i[0]:<5}]')


def print_by_date(account_name: str, account_cur: str,
                  from_date: datetime.date, to_date: datetime.date,
                  deals: list) -> None:
    income = 0
    costs = 0
    for i in deals:
        if i[1] > 0:
            income += i[1]
        else:
            costs += i[1]
    print(f'ACCOUNT  {account_name}\nfrom {from_date} to {to_date}')
    print(f'\033[92mINCOME: {income} '
          f'\033[91mCOSTS: {costs}')
    print(f'\033[95m[{"id":<5}][{"amount":<9}][{"CUR":<4}]'
          f'[{"date":<11}][{"type":<15}]')
    for i in deals:
        if i[1] > 0:
            print(f'\033[92m[{i[0]:<5}][{i[1]:<9}][{account_cur:<4}]'
                  f'[{i[2]} ][{i[3]:<15}]')
        else:
            print(f'\033[31m[{i[0]:<5}][{i[1]:<9}][{account_cur:<4}]'
                  f'[{i[2]} ][{i[3]:<15}]')


def print_stats(account_name: str, account_cur: str, deals: list,
                from_date: datetime.date, to_date: datetime.date) -> None:
    count_transactions = len(deals)
    period = (to_date - from_date).days
    income = 0
    costs = 0
    categories = {}
    for i in deals:
        if i[1] > 0:
            income += i[1]
        else:
            costs += i[1]
        if i[3] in categories:
            categories[i[4]] += i[1]
        else:
            categories[i[3]] = i[1]
    print(f'ACCOUNT  {account_name}')
    print(f'\033[34mDAYS: {period}  ({from_date} -> {to_date})')
    print(f'\033[34mCOUNT DEALS FOR PERIOD: {count_transactions}')
    print(f'\033[92mINCOME: {income} ' f'\033[91mCOSTS: {costs}')
    print('\033[34m[type           ][amount   ][CUR ]')
    for i in categories:
        if categories[i] > 0:
            print(f'\033[92m[{i:<15}][{categories[i]:<9}][{account_cur:<4}]')
        else:
            print(f'\033[91m[{i:<15}][{categories[i]:<9}][{account_cur:<4}]')
