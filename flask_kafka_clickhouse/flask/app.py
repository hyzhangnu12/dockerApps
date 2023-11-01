from flask import Flask
from kafka import KafkaProducer, KafkaConsumer
from datetime import datetime
import json

server = Flask(__name__)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],
    api_version=(0,11,5),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer = KafkaConsumer(
    'posts',
    bootstrap_servers='localhost:9093',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    api_version=(0,11,5),
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

@server.route('/', methods=['GET'])
def home():
    return "welcome to the flask + kafka + clickhouse app!"

@server.route('/write', methods=['GET'])
def send():
    producer.send('post', {'author': 'Tommy', \
                           'content': 'Tommy is a good boy!', \
                           'created_at': datetime.now().isoformat()})
    return 'ok'
    
@server.route('/read', methods=['GET'])
def read():
    res = []
    for message in consumer:
        res.append(message.value)
    return res

if __name__ == '__main__':
    server.run()
