import grpc
import pika
import json

from invoice_metadata import invoice_pb2
from invoice_metadata import invoice_pb2_grpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = invoice_pb2_grpc.RechnungServiceStub(channel)

    request = invoice_pb2.RechnungRequest(
        rechnungs_nummer="001",
        lieferant="Lekkerland",
        betrag=99.99,
        waehrung="EUR",
        datum="2026-04-09",
        status=invoice_pb2.OFFEN
    )

    try:
        response = stub.SpeichereMetadaten(request)
        print("gRPC Antwort vom Server:")
        print(f"Erfolg: {response.erfolg}, Nachricht: {response.nachricht}")
        
        if response.erfolg:
            credentials = pika.PlainCredentials("user", "password")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="localhost",
                    credentials=credentials
                )
            )
            mq_channel = connection.channel()
            
            mq_channel.queue_declare(queue='zahlungs_auftraege')

            zahlungs_daten = {
                "rechnungs_nummer": request.rechnungs_nummer,
                "betrag": request.betrag,
                "waehrung": request.waehrung
            }

            mq_channel.basic_publish(
                exchange='',
                routing_key='zahlungs_auftraege',
                body=json.dumps(zahlungs_daten)
            )
            
            print(f"RabbitMQ: Zahlungsauftrag für {request.rechnungs_nummer} gesendet.")
            connection.close()

    except grpc.RpcError as e:
        print(f"Fehler: gRPC Server nicht erreichbar ({e.details()})")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")

if __name__ == "__main__":
    run()
