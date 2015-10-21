#!/usr/bin/env python
import pika
import pymongo
import json
import datetime
import signal
import sys


def signal_handler(signum, frame):
    """
        Suppress exception on CTRL+C
    """
    print "SIGINT received, exiting ..."
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


mongo_client = pymongo.MongoClient()
db = mongo_client['auto_test_numbers']
conn = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', heartbeat_interval=600
))
channel = conn.channel()

channel.queue_declare(queue='numbers')
print '[*] Waiting for messages. To exit press CTRL+C'


def callback(ch, method, properties, body):
    numbers_to_add = json.loads(body)
    print "[x] New request has been received at {}".format(
        datetime.datetime.now().replace(microsecond=0).__str__()
    )

    for dst, dst_data in numbers_to_add.iteritems():
        dst_collection = db.get_collection(dst)

        for n, setup_time in dst_data:
            setup_time = datetime.datetime.strptime(
                setup_time.split('.')[0], '%Y-%m-%d %H:%M:%S'
            )

            number = dst_collection.find_one({"_id": n})

            if not number:
                dst_collection.insert({"_id": n, "setup_time": setup_time})
            elif number["setup_time"] < setup_time:
                dst_collection.update_one(
                    {"_id": n}, {"$set": {"setup_time": setup_time}}
                )
                
            #dst_collection.find_one_and_update(
            #    {"_id": n}, {"$set": {"setup_time": setup_time}}, upsert=True
            #)
    
    print "[x] Request has been processed at {}".format(
        datetime.datetime.now().replace(microsecond=0).__str__()
    )


channel.basic_consume(callback, queue='numbers', no_ack=True)
channel.start_consuming()
