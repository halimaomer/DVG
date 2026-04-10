# DVG-1 - Digitalisierung eines Geschäftsprozesses

Projekt in Rahmen des Modul **Digitalisierung von Geschäftsprozessen**
Hochschule Karlsruhe


## Projektbeschreibung

Digitalisierung der Eingangsrechungsverarbeitung eines mittelständischen Unternehmens.


## Projektstruktur

DVG-1/
|---client/               # Client: speichert Rechnungsdaten & veranlasst Zahlung
|---invoice_metadata/     # gRPC Server: speichert Rechnungsdaten
|---payment_system/       # Zahlungssystem: verarbeitet Zahlungsaufträge via RabbitMQ
|---proto/                # Protobuf Definition
|---.gitignore            # Git Ausnahmen
|---docker-compose.yml    # RabbitMQ Contanier
|---README.md             # Projektdokumentation
|---requirements.txt      # Python Abhängigkeiten


## Technologien
- **gRPC** (Google Remote Procedure Call)- Kommunikation zwischen Client und Metadaten-Service
- **RabbitMQ**  - Message Broker für Zahlungsaudträge
- **Protobuf**  - Serialisierung der Nachrichten
- **Docker**    - RabbitMQ läuft als Contanier


----

## Voraussetzungen

- Python 3.13
- Docker & Docker Compose


## Installation

```bash/powershell
pip install -r requirements.txt
```


----


## Starten

**1. RabbitMQ starten:**

```bash/powershell
docker-compose up -d
```

**2. gRPC Server starten (Terminal 1):**

```bash/powershell
python -m invoice_metadata.server
```

**3. Payment System starten (Terminal 2):**

```bash/powershell
python -m payment_system.payment
```

**4. Client starten (Terminal 3):**

```bash/powershell
python -m client.client
```



## Stoppen

**Client, gRPC Server & Payment System** (in jeweiligem Terminal):

```bash/powershell
Ctrl + C
```

**RabbitMq Contanier stoppen:**
```
bash/powershell
docker-compose down
```



----


## RabbitMQ Management UI

http://localhost:15672
Login: `user` / `password`



----