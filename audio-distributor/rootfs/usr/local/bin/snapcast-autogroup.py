import socket
import json
import time

HOST = '127.0.0.1'
PORT = 1705

class SnapcastAutoGroup:
    def __init__(self):
        self.sock = None
        self.buffer = ""
        self.rpc_id = 0

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

    def send_req(self, method, params=None):
        self.rpc_id += 1
        req = {"id": self.rpc_id, "jsonrpc": "2.0", "method": method}
        if params:
            req["params"] = params
        self.sock.sendall((json.dumps(req) + '\n').encode('utf-8'))
        return self.rpc_id

    def read_msgs(self):
        data = self.sock.recv(65535).decode('utf-8')
        if not data:
            raise ConnectionError("Disconnected")
        self.buffer += data
        msgs = []
        while '\n' in self.buffer:
            line, self.buffer = self.buffer.split('\n', 1)
            if line.strip():
                try:
                    msgs.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return msgs

    def get_status(self):
        req_id = self.send_req("Server.GetStatus")
        while True:
            msgs = self.read_msgs()
            for msg in msgs:
                if msg.get('id') == req_id:
                    return msg.get('result', {}).get('server', {}).get('groups', [])

    def enforce_casa_group(self):
        groups = self.get_status()
        if not groups:
            return
        
        casa_group = None
        for g in groups:
            if g.get('name') == 'Casa':
                casa_group = g
                break
        
        if not casa_group:
            casa_group = groups[0]
            self.send_req("Group.SetName", {"id": casa_group['id'], "name": "Casa"})
            print(f"Renamed group {casa_group['id']} to Casa")
        
        all_clients = []
        for g in groups:
            for c in g.get('clients', []):
                if c['id'] not in all_clients:
                    all_clients.append(c['id'])
        
        casa_client_ids = [c['id'] for c in casa_group.get('clients', [])]
        
        if set(all_clients) != set(casa_client_ids):
            print(f"Moving clients to Casa group: {all_clients}")
            self.send_req("Group.SetClients", {"id": casa_group['id'], "clients": all_clients})

        # Enforce 100% volume for all clients so Spotify reaches max expected volume
        for g in groups:
            for c in g.get('clients', []):
                vol = c.get('config', {}).get('volume', {})
                if vol.get('percent') != 100 or vol.get('muted'):
                    print(f"Setting volume to 100% for client {c['id']}")
                    self.send_req("Client.SetVolume", {"id": c['id'], "volume": {"muted": False, "percent": 100}})

    def run(self):
        while True:
            try:
                self.connect()
                print("Connected to Snapcast RPC")
                self.enforce_casa_group()
                
                while True:
                    msgs = self.read_msgs()
                    for msg in msgs:
                        # Re-evaluate grouping on any client connect or disconnect
                        if msg.get('method') in ['Client.OnConnect', 'Client.OnDisconnect', 'Group.OnUpdate']:
                            self.enforce_casa_group()
            except Exception as e:
                print(f"Connection lost: {e}")
                time.sleep(5)
                self.sock = None

if __name__ == '__main__':
    SnapcastAutoGroup().run()
