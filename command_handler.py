import datetime

#from enum import Enum

from db_manager import init_db
from db_manager import add_transaction
from db_manager import select_all
from db_manager import select_by_category
from db_manager import select_by_date

from printer import print_category
from printer import print_resent
from printer import print_by_date

#class Month(Enum):
 #   JANUARY = '31'
   # FEBRUARY = '28'
  #  MARCH = '31'
    #APRIL = '30'
#    MAY = '31'
 #   JUNE = '30'
  #  JULY = '31'
   # AUGUST = '31'
    #SEPTEMBER = '30'
#    OCTOBER = '31'
 #   NOVEMBER = '30'
  #  DECEMBER = '31'
    

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
        try:
            from_date = argv[2]
            year = int(from_date[0:4])
            month = int(from_date[5:7])
        except IndexError:
            now = datetime.date.today()
            year = now.year
            month = now.month
            from_date = f'{year}-{month}-01'
        if month == 12:
            to_date = f'{year+1}-01-01'
        else:
            to_date = f'{year}-{month+1}-01'
        print(from_date)
        print(f'year: {year}, month: {month}')
        print(to_date)

        print_by_date(select_by_date(cur, from_date, to_date))
