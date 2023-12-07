# treasury

simple cli finance manager

## the following options are now available:
- add income/expense
- display a list of all operations
- display transactions list for the selected category
- display transactions list for the current month
- display all transactions
- display monthly and yearly statistics

## installation

clone repo

`git clone https://codeberg.org/ejix/treasury.git`

install dependencies

`poetry install`

use

## usage:

`usage: treasury [account name] [-action]`
    
`actions:
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
      -ac               add category
      -ec               edit category`
