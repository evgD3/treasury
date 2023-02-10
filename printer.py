def print_resent(transactions: list) -> None:
    balance = 0
    for i in transactions:
        balance += i[1]
    transactions = transactions[-10:]
    transactions = transactions[::-1]
    print(f'\033[34mBALANCE: {balance}')
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
    print(f'\033[92m INCOME: {income} ' f'\033[91m COSTS: {costs}')

    print('\033[95m[id]     [amount]   [date]        [type]')
    for i in transactions:
        if i[1] > 0:
            print(f'\033[92m [{i[0]}]   [{i[1]}]         [{i[2]}]   [{i[3]}]')
        else:
            print(f'\033[31m [{i[0]}]   [{i[1]}]         [{i[2]}]   [{i[3]}]')
