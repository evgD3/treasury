import tabulate


def print_resent(transactions: list) -> None:
    balance = 0
    for i in transactions:
        balance += i[1]
    transactions = transactions[-10:]
    transactions = transactions[::-1]
    print(f'\033[34mBALANCE: {balance}')
    #print('\033[95mRESENT:')
    print('\033[95m[id]     [amount]   [date]        [type]')
    for i in transactions:
        if i[1]>0:
            print(f'\033[92m [{i[0]}]   [{i[1]}]         [{i[2]}]   [{i[3]}]')
        else:
            print(f'\033[31m [{i[0]}]   [{i[1]}]         [{i[2]}]   [{i[3]}]')


def print_category(transactions: list) -> None:
    ALL = 0
    for i in transactions:
        ALL += i[1]
    if ALL > 0:
        print(f'\033[92mALL {ALL}')
    else:
        print(f'\033[91mALL {ALL}')
    print('\033[95m [type]     [date]        [amount]        [id]')
    for i in transactions:
        if i[1]>0:
            print(f'\033[92m [{i[3]}]   [{i[2]}]         [{i[1]}]   [{i[0]}]')
        else:
            print(f'\033[91m [{i[3]}]   [{i[2]}]         [{i[1]}]   [{i[0]}]')


def print_by_date(transactions: list) -> None:
    up = 0
    down = 0
    for i in transactions:
        if i[1] > 0:
            up += i[1]
        else:
            down += i[1]
    print(f'\033[92mUP: {up} ' f'\033[91mDOWN: {down}')

    print('\033[95m[id]     [amount]   [date]        [type]')
    for i in transactions:
        if i[1]>0:
            print(f'\033[92m [{i[0]}]   [{i[1]}]         [{i[2]}]   [{i[3]}]')
        else:
            print(f'\033[31m [{i[0]}]   [{i[1]}]         [{i[2]}]   [{i[3]}]')



