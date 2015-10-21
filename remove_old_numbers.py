#/usr/bin/env python
import pymongo
import datetime


def remove_old_numbers():
    delta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    start_date =  now.replace(
        hour=0, minute=0, second=0, microsecond=0
    ) - delta

    with pymongo.MongoClient() as client:
        db = client['auto_test_numbers']

        for coll_name in db.collection_names(include_system_collections=False):
            #print "Delete old entries in collection {} ...".format(coll_name)
            #entries = db[coll_name].find(
            #    {"setup_time": {"$lt": start_date}}
            #).distinct('_id')
            #print '{}'.format(entries)
            db[coll_name].delete_many({"setup_time": {"$lt": start_date}})


if __name__ == '__main__':
    remove_old_numbers()
