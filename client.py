import pika
import uuid

def on_reply_message_received(ch, method, properties, body):
    print(f"reply recieved: {body}")

# This part is used to establish a connection with RabbitMQ which is running on localhost

connection_parameters = pika.ConnectionParameters('localhost') ## Connection is present at local host
connection = pika.BlockingConnection(connection_parameters) ## Establist a Synchronus Connection with RabbitMq
channel = connection.channel()  ## Represents a virtual connection over which communication with RabbitMQ happens.


reply_queue = channel.queue_declare(queue='', exclusive=True) ## exclusive mean only this channel can recieve reply

channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True,
    on_message_callback=on_reply_message_received)

channel.queue_declare(queue='request-queue')

cor_id = str(uuid.uuid4())
print(f"Sending Request: {cor_id}")

channel.basic_publish('', routing_key='request-queue', properties=pika.BasicProperties(
    reply_to=reply_queue.method.queue, ## It will tell the sender where to send the response
    correlation_id=cor_id
), body='Can I request a reply?')

print("Starting Client")

channel.start_consuming()