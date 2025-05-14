import json
import hashlib
import heapq

def signature(clients):
    datos = {k: clients[k] for k in ["dpi", "firstName", "lastName", "birthDate", "job", "placeJob", "salary"]}
    return hashlib.sha256(json.dumps(datos, sort_keys=True).encode()).hexdigest()

def read_json(root):
    with open(root, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]

def process_bids(clients_file, auctions_path, exit_file):
    clients = read_json(clients_file)
    auctions = read_json(auctions_path)
    hash_clients = {str(c["dpi"]): c for c in clients}

    with open(exit_file, 'w') as out:
        for auction in auctions:
            heap = [(-c["budget"], str(c["dpi"]), c["date"]) for c in auction["customers"]]
            heapq.heapify(heap)

            for _ in range(auction["rejection"]):
                if heap:
                    heapq.heappop(heap)

            if not heap:
                continue

            neg_budget, dpi, date = heapq.heappop(heap)
            client = hash_clients.get(dpi)

            if client:
                result = {
                    "dpi": client["dpi"],
                    "budget": -neg_budget,
                    "date": date,
                    "firstName": client["firstName"],
                    "lastName": client["lastName"],
                    "birthDate": client["birthDate"],
                    "job": client["job"],
                    "placeJob": client["placeJob"],
                    "salary": client["salary"],
                    "property": auction["property"],
                    "signature": signature(client)
                }
                out.write(json.dumps(result, separators=(',', ':')) + "\n")

# ------------------ Rutas ------------------
clients_path = r'C:\Users\axelg\OneDrive\Documentos\ED1\Lab03AxelAlvarado\customer_challenge.jsonl'
auctions_path = r'C:\Users\axelg\OneDrive\Documentos\ED1\Lab03AxelAlvarado\auctions_challenge.jsonl'
exit_path = r'C:\Users\axelg\OneDrive\Documentos\ED1\Lab03AxelAlvarado\output.jsonl'

process_bids(clients_path, auctions_path, exit_path)