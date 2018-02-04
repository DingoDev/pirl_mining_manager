"""
    To view the current miners on the public Pirl miner
"""

import time
import sqlite3
import urllib2
import datetime
import pip

try:
    import requests
except ImportError:
    pip.main(['install', 'requests'])
    import requests

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    pip.main(['install', 'BeautifulSoup'])
    from BeautifulSoup import BeautifulSoup

POOL_MINER_API = "http://pirl.minerpool.net/api/accounts/"
POOL_MINER_ACCOUNT = "" # TODO put your account here

PIRL_COIN_MARKET_CAP = "https://coinmarketcap.com/currencies/pirl/"

HEALTHY = True

def pull_from_pool():
    """ Hit the miner api and grab all the mining information """
    try:
        res = requests.get(POOL_MINER_API + POOL_MINER_ACCOUNT)
        if res.ok:
            print "We hit the Pirl miner API just fine"
            res.json()
        else:
            print("A non-ok status code was returned", res.status_code)
            return False
    except Exception as e:
        print("Error code", e)
        return False

def get_pirl_price():
    """ HTML scraping the price, there is some API but it's a little weird """
    price = 0
    try:
        page = urllib2.urlopen(PIRL_COIN_MARKET_CAP)
        soup = BeautifulSoup(page)
        # Grab the price from the page, given lovingly a good class name
        price = soup.find('span', {'class': 'data-currency-value'}).text
    except Exception as e:
        print "Error ocurred in find the price, will set as 0 for this iteration"
        print e
    return price

def write_to_db(pool_information, price):
    """ Write all the worker information to the database """
    conn = sqlite3.connect('mining_ledger.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS ledger (
        minername TEXT NOT NULL,
        hashrate INTEGER,
        coinsmined REAL,
        price REAL,
        timestamped TIMESTAMP
    )"""
    cursor.execute(sql)

    # Time stamp for when we gathered the information
    current_time = datetime.datetime.now()

    # All the worker objects
    workers = pool_information['workers']

    worker_keys = []

    for key in workers:
        worker_keys.append(key)

    avg_hash = 0

    for worker in worker_keys:
        avg_hash = avg_hash + workers[worker['hr2']]
        cursor.execute("""INSERT INTO ledger (minername,
        hashrate,
        coinsmined,
        price,
        timestamped) VALUES (?, ?, ?, ?, ?)""", (worker,
                                           workers[worker]['hr2'],
                                           workers[worker]['hr2'] * 0.001, # approx 1mh/s for 30 mins = 0.001 pirl
                                           price,
                                           current_time))

    avg_hash = avg_hash / len(worker_keys)

    print "Writing entries gathered from this iteration to the table at time {}".format(current_time)
    print "THere are currently {} many miners".format(len(worker_keys))
    print "Current average hashrate is {}".format(avg_hash)
    # Commit the entries to the table
    conn.commit()
    conn.close()

def main():
    """ The main function """
    if not POOL_MINER_ACCOUNT:
        print("You need to add your key for accessing your accounts API")
        exit(1)

    while HEALTHY:
        pool_information = pull_from_pool()
        # Check that the information could be pulled down
        if pool_information:
            price = get_pirl_price()
            # Write all the information gathered to the sqlite3 database
            write_to_db(pool_information, price)
        # Wait for a half hour
        time.sleep(1800)

if __name__ == "__main__":
    main()