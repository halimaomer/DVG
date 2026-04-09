from concurrent import futures
import grpc

from . import invoice_pb2
from . import invoice_pb2_grpc


class RechnungService(invoice_pb2_grpc.RechnungServiceServicer):
    def __init__(self):
        self.db = {}

    def SpeichereMetadaten(self, request, context):
        self.db[request.rechnungs_nummer] = request

        status_name = invoice_pb2.RechnungsStatus.Name(request.status)

        print("\n--- Neue Rechnung gespeichert ---")
        print(f"Nummer: {request.rechnungs_nummer}")
        print(f"Status: {status_name}")
        print("---------------------------------\n")

        return invoice_pb2.RechnungResponse(
            erfolg=True,
            nachricht="Gespeichert"
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    invoice_pb2_grpc.add_RechnungServiceServicer_to_server(
        RechnungService(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("Server läuft auf Port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()