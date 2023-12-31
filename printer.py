import datetime


def print_resent(account: str, transactions: list) -> None:
    transactions = transactions[:10]
    print(f'ACCOUNT  {account}')
    print(f'\033[34m[{"id":<5}][{"CUR":<4}][{"amount":<9}]'
          f'[{"date":<11}][{"type":<15}]')
    for i in transactions:
        if i[2] > 0:
            print(f'\033[92m[{i[0]:<5}][{i[1]:<4}]'
                  f'[{i[2]:<9}][{i[3]} ][{i[4]:<15}]')
        else:
            print(f'\033[31m[{i[0]:<5}][{i[1]:<4}]'
                  f'[{i[2]:<9}][{i[3]} ][{i[4]:<15}]')



def print_all(account: str, transactions: list) -> None:
    income = 0
    costs = 0
    for i in transactions:
        if i[2] > 0:
            income += i[2]
        else:
            costs += i[2]
    print(f'ACCOUNT  {account}')
    print(f'\033[92mINCOME: {income} '
          f'\033[91mCOSTS: {costs}')
    print(f'\033[34m[{"id":<5}][{"CUR":<4}][{"amount":<9}]'
          f'[{"date":<11}][{"type":<15}]')
    for i in transactions:
        if i[2] > 0:
            print(f'\033[92m[{i[0]:<5}][{i[1]:<4}]'
                  f'[{i[2]:<9}][{i[3]} ][{i[4]:<15}]')
        else:
            print(f'\033[31m[{i[0]:<5}][{i[1]:<4}]'
                  f'[{i[2]:<9}][{i[3]} ][{i[4]:<15}]')


def print_category(account: str, transactions: list) -> None:
    ALL = 0
    print(f'ACCOUNT  {account}')
    for i in transactions:
        ALL += i[1]
    if ALL > 0:
        print(f'\033[92mALL {ALL}')
    else:
        print(f'\033[91mALL {ALL}')
    print(f'\033[95m[{"type":<15}][{"date":<11}]'
          f'[{"amount":<9}][{"CUR":<4}][{"id":<5}]')
    for i in transactions:
        if i[1] > 0:
            print(f'\033[92m[{i[3]:<15}][{i[2]} ]'
                  f'[{i[1]:<9}][{i[4]:<4}][{i[0]:<5}]')
        else:
            print(f'\033[91m[{i[3]:<15}][{i[2]} ]'
                  f'[{i[1]:<9}][{i[4]:<4}][{i[0]:<5}]')


def print_by_date(account: str, transactions: list) -> None:
    income = 0
    costs = 0
    for i in transactions:
        if i[1] > 0:
            income += i[1]
        else:
            costs += i[1]
    print(f'ACCOUNT  {account}')
    print(f'\033[92mINCOME: {income} '
          f'\033[91mCOSTS: {costs}')
    print(f'\033[95m[{"id":<5}][{"amount":<9}][{"CUR":<4}]'
          f'[{"date":<11}][{"type":<15}]')
    for i in transactions:
        if i[1] > 0:
            print(f'\033[92m[{i[0]:<5}][{i[1]:<9}][{i[2]:<4}][{i[3]} ][{i[4]:<15}]')
        else:
            print(f'\033[31m[{i[0]:<5}][{i[1]:<9}][{i[2]:<4}][{i[3]} ][{i[4]:<15}]')



def print_stats(account: str, transactions: list,
                from_date: datetime.date, to_date: datetime.date) -> None:
    count_transactions = len(transactions)
    period = (to_date - from_date).days
    income = 0
    costs = 0
    categories = {}
    currency = transactions[1][2]
    for i in transactions:
        if i[1] > 0:
            income += i[1]
        else:
            costs += i[1]
        if i[4] in categories:
            categories[i[4]] += i[1]
        else:
            categories[i[4]] = i[1]
    print(f'ACCOUNT  {account}')
    print(f'\033[34mDAYS: {period}  ({from_date} -> {to_date})')
    print(f'\033[34mCOUNT TRANSACTIONS FOR PERIOD: {count_transactions}')
    print(f'\033[92mINCOME: {income} ' f'\033[91mCOSTS: {costs}')
    print('\033[34m[type           ][amount   ][CUR ]')
    for i in categories:
        if categories[i] > 0:
            print(f'\033[92m[{i:<15}][{categories[i]:<9}][{currency:<4}]')
        else:
            print(f'\033[91m[{i:<15}][{categories[i]:<9}][{currency:<4}]')
