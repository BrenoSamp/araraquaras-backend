import pika, json

params = pika.URLParameters('amqps://cuvxizzy:aFGKx1-N9z43KdNq3gHJiaDGsflN2dO1@albatross.rmq.cloudamqp.com/cuvxizzy')


def publish(body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='novo_ticket_setor', body=json.dumps(body))
    connection.close()