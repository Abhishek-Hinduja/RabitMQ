import pika

def on_request_message_received(ch, method, properties, body):
    print(f"Received Request: {properties.correlation_id}")
    response = f'Hey, it\'s your reply to {properties.correlation_id}'
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=response
    )

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='request-queue')

channel.basic_consume(
    queue='request-queue',
    auto_ack=True,
    on_message_callback=on_request_message_received
)

print("Starting Server")
channel.start_consuming()
