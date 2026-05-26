import socket
import json
import os
import time

HOST = '127.0.0.1'
PORT = 1705

try:
    DEFAULT_CLIENT_VOLUME = int(os.environ.get('SNAPCAST_DEFAULT_CLIENT_VOLUME', '78'))
except ValueError:
    DEFAULT_CLIENT_VOLUME = 78
DEFAULT_CLIENT_VOLUME = max(0, min(100, DEFAULT_CLIENT_VOLUME))

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

    def enforce_default_volumes(self, groups):
        seen_clients = set()
        for group in groups:
            for client in group.get('clients', []):
                client_id = client.get('id')
                if not client_id or client_id in seen_clients:
                    continue
                seen_clients.add(client_id)

                volume = client.get('config', {}).get('volume', {})
                current_percent = volume.get('percent')
                if current_percent is None or current_percent <= DEFAULT_CLIENT_VOLUME:
                    continue

                muted = bool(volume.get('muted', False))
                self.send_req("Client.SetVolume", {
                    "id": client_id,
                    "volume": {
                        "muted": muted,
                        "percent": DEFAULT_CLIENT_VOLUME,
                    },
                })
                print(f"Set client {client_id} volume from {current_percent} to {DEFAULT_CLIENT_VOLUME}")

    def enforce_casa_group(self, apply_default_volume=False):
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

        if apply_default_volume:
            self.enforce_default_volumes(groups)

    def run(self):
        while True:
            try:
                self.connect()
                print("Connected to Snapcast RPC")
                self.enforce_casa_group(apply_default_volume=True)
                
                while True:
                    msgs = self.read_msgs()
                    for msg in msgs:
                        # Re-evaluate grouping on any client connect or disconnect
                        if msg.get('method') == 'Client.OnConnect':
                            self.enforce_casa_group(apply_default_volume=True)
                        elif msg.get('method') in ['Client.OnDisconnect', 'Group.OnUpdate']:
                            self.enforce_casa_group()
            except Exception as e:
                print(f"Connection lost: {e}")
                time.sleep(5)
                self.sock = None

if __name__ == '__main__':
    SnapcastAutoGroup().run()
