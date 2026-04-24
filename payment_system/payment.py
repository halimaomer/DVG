import json
import time
import pika


QUEUE_NAME = "zahlungs_auftraege"


def callback(ch, method, properties, body):
    try:
        zahlungsdaten = json.loads(body.decode("utf-8"))
        rechnungsnr = zahlungsdaten.get("rechnungs_nummer")
        betrag = zahlungsdaten.get("betrag")
        waehrung = zahlungsdaten.get("waehrung", "EUR")

        print(f"Rechnung erhalten: {rechnungsnr}")
        print(f"Betrag: {betrag} {waehrung}")

        time.sleep(1)

        print(f"Zahlung für {rechnungsnr} erfolgreich durchgeführt.")
        print("-" * 40)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Fehler bei der Verarbeitung: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_payment_system():
    try:
        credentials = pika.PlainCredentials("user", "password")

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost",
                port=5672,
                credentials=credentials
            )
        )

        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=callback
        )

        print("Zahlungssystem gestartet.")
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError:
        print("Fehler: RabbitMQ ist nicht erreichbar.")

if __name__ == "__main__":
    start_payment_system()