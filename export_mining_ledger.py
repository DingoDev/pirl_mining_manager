""" To export the database to a csv file """

import csv
import sqlite3

def import_ledger():
    """ Intake the ledger into the session """
    conn = sqlite3.connect('mining_ledger.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = conn.cursor()

    sql = """SELECT minername,
            hashrate,
            coinsmined,
            price,
            timestamped, FROM ledger ORDER BY minername ASC"""

    cursor.execute(sql)
    return cursor.fetchall()

def open_csv():
    """ Open the csv file for writing """
    excel_writer = {}
    with open('mining_ledger.csv', 'wb') as mining_ledger:
        excel_writer = csv.writer(mining_ledger, quoting=csv.QUOTE_MINIMAL)
    return excel_writer

def write_to_csv(csv_writer, ledger):
    """ Write the ledger into the csv file """
    csv_writer.writerow(['Miner name', 'Hash rate', 'Coins mined in a half hour', 'Price at time of mining', 'Timestamp'])
    for row in ledger:
        csv_writer.writerow([row[0], row[1], row[2], "$" + row[3], row[4]])

def main():
    """ To take the sqlite3 db and move it into a csv file """
    csv_writer = open_csv()
    ledger = import_ledger()
    write_to_csv(csv_writer, ledger)

if __name__ == "__main__":
    main()
