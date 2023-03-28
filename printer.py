import datetime

def print_resent(transactions: list, balance_list: list) -> None:
    balance = balance_list[0][1]
    transactions = transactions[:10]
    print(f'\033[34mBALANCE: {balance}')
    print(f'\033[34m[{"id":<5}][{"amount":<7}][{"date":<11}][{"type":<15}]')
    for i in transactions:
        if i[1] > 0:
            print(f'\033[92m[{i[0]:<5}][{i[1]:<7}][{i[2]} ][{i[3]:<15}]')
        else:
            print(f'\033[31m[{i[0]:<5}][{i[1]:<7}][{i[2]} ][{i[3]:<15}]')

def print_all(transactions: list, balance_list: list) -> None:
    balance = balance_list[0][1]
    income = 0
    costs = 0
    for i in transactions:
        if i[1] > 0:
            income += i[1]
        else:
            costs += i[1]
    print(f'\033[34mBALANCE: {balance} '
          f'\033[92mINCOME: {income} '
          f'\033[91mCOSTS: {costs}')
    print(f'\033[34m[{"id":<5}][{"amount":<7}][{"date":<11}][{"type":<15}]')
    for i in transactions:
        if i[1] > 0:
            print(f'\033[92m[{i[0]:<5}][{i[1]:<7}][{i[2]} ][{i[3]:<15}]')
        else:
            print(f'\033[31m[{i[0]:<5}][{i[1]:<7}][{i[2]} ][{i[3]:<15}]')

def print_category(transactions: list) -> None:
    ALL = 0
    for i in transactions:
        ALL += i[1]
    if ALL > 0:
        print(f'\033[92mALL {ALL}')
    else:
        print(f'\033[91mALL {ALL}')
    print(f'\033[95m[{"type":<15}][{"date":<11}][{"amount":<7}][{"id":<5}]')
    for i in transactions:
        if i[1] > 0:
            print(f'\033[92m[{i[3]:<15}][{i[2]} ][{i[1]:<7}][{i[0]:<5}]')
        else:
            print(f'\033[91m[{i[3]:<15}][{i[2]} ][{i[1]:<7}][{i[0]:<5}]')

def print_by_date(transactions: list) -> None:
    income = 0
    costs = 0
    for i in transactions:
        if i[1] > 0:
            income += i[1]
        else:
            costs += i[1]
    print(f'\033[92mINCOME: {income} ' f'\033[91mCOSTS: {costs}')
    print(f'\033[95m[{"id":<5}][{"amount":<7}][{"date":<11}][{"type":<15}]')
    for i in transactions:
        if i[1] > 0:
            print(f'\033[92m[{i[0]:<5}][{i[1]:<7}][{i[2]} ][{i[3]:<15}]')
        else:
            print(f'\033[31m[{i[0]:<5}][{i[1]:<7}][{i[2]} ][{i[3]:<15}]')

def print_stats(transactions: list, from_date: datetime.date,
                to_date: datetime.date) -> None:
    count_transactions = len(transactions)
    period = (to_date - from_date).days
    income = 0
    costs = 0
    categories = {}
    for i in transactions:
        if i[1] > 0:
            income += i[1]
        else:
            costs += i[1]
        if i[3] in categories:
            categories[i[3]] += i[1]
        else:
            categories[i[3]] = i[1]
    print(f'\033[34mDAYS: {period}  ({from_date} -> {to_date})')
    print(f'\033[34mCOUNT TRANSACTIONS FOR PERIOD: {count_transactions}')
    print(f'\033[92mINCOME: {income} ' f'\033[91mCOSTS: {costs}')
    print(f'\033[34m[type           ][amount ]')
    for i in categories:
        if categories[i] > 0:
            print(f'\033[92m[{i:<15}][{categories[i]:<7}]')
        else:
            print(f'\033[91m[{i:<15}][{categories[i]:<7}]')
