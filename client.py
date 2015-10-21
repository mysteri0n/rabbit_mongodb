#!/usr/bin/env python
import pika, json


conn = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'
))

channel = conn.channel()
channel.queue_declare(queue='numbers')

data = {'380': []}

for i in xrange(1000000):
    data['380'].append(
        ('380{}'.format(str(i).rjust(7, '0')), '2015-10-04 12:05:36')
    ) 

channel.basic_publish(
    exchange='',
    routing_key='numbers',
    body=json.dumps(data)
)

print '[x] Sent message to server'

conn.close()
