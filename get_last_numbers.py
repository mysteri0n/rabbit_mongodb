#/usr/bin/env python
import pymongo
import datetime
import sys


def get_last_numbers(dest, quantity):
    delta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    start_date =  now.replace(
        hour=0, minute=0, second=0, microsecond=0
    ) - delta

    with pymongo.MongoClient() as client:
        db = client['auto_test_numbers']

        #return db[dest].find({}, projection=["_id"]).limit(int(quantity))
        return db[dest].find({}).limit(int(quantity))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Invalid number of argumets'
        sys.exit(1)

    numbers = get_last_numbers(sys.argv[1], sys.argv[2])

    print [n["_id"] for n in numbers]
