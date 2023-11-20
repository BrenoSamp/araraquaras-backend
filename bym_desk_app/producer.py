import pika, json

params = pika.URLParameters('amqps://ziucaoki:sHXSNCgyMx6DAPMGgZNkiCe4jjR_7Fb6@jackal.rmq.cloudamqp.com/ziucaoki')


def publish(body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='novo_ticket_setor', body=json.dumps(body))
    connection.close()