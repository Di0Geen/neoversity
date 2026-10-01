import json
import logging
import mimetypes
import os
import signal
import socket
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from multiprocessing import Event, Process
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from pymongo import MongoClient
from pymongo.errors import PyMongoError

BASE_DIR = Path(__file__).resolve().parent
SOCKET_ADDRESS = ("127.0.0.1", 5000)
MAX_SIZE = 64 * 1024
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
ROUTES = {f"/{name}": name for name in (
    "index.html", "message.html", "style.css", "logo.png"
)}
ROUTES.update({"/": "index.html", "/message": "message.html"})
logging.basicConfig(level=logging.INFO, format="%(processName)s: %(message)s")


def read_packet(connection):
    with connection.makefile("rb") as stream:
        data = stream.readline(MAX_SIZE + 1)
    if len(data) > MAX_SIZE or not data.endswith(b"\n"):
        raise ValueError("Invalid packet")
    return json.loads(data)


def validate_message(data):
    if not isinstance(data, dict) or any(
        not isinstance(data.get(key), str) or not data[key].strip()
        for key in ("username", "message")
    ):
        raise ValueError("Username and message are required")
    return {key: data[key] for key in ("username", "message")}


class Handler(BaseHTTPRequestHandler):
    def send_file(self, name, status=200):
        content = (BASE_DIR / name).read_bytes()
        self.send_response(status)
        self.send_header("Content-Type", mimetypes.guess_type(name)[0]
                         or "application/octet-stream")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        name = ROUTES.get(urlsplit(self.path).path)
        self.send_file(name or "error.html", 200 if name else 404)

    def do_POST(self):
        if urlsplit(self.path).path != "/message":
            return self.send_file("error.html", 404)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_SIZE:
                return self.send_error(413 if length > MAX_SIZE else 400)
            fields = parse_qs(self.rfile.read(length).decode("utf-8"),
                              keep_blank_values=True)
            payload = validate_message({key: value[0] for key, value in fields.items()})
            packet = (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")
            if len(packet) > MAX_SIZE:
                return self.send_error(413)
        except ValueError:
            return self.send_error(400, "Invalid form data")

        try:
            with socket.create_connection(SOCKET_ADDRESS, timeout=10) as connection:
                connection.sendall(packet)
                if read_packet(connection) != {"ok": True}:
                    raise ValueError("Message was not saved")
        except (OSError, ValueError):
            logging.exception("Cannot save message")
            return self.send_error(503, "Message storage unavailable")
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


def run_socket_server(ready):
    with MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000, timeoutMS=5000) as client:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(SOCKET_ADDRESS)
            server.listen()
            ready.set()
            logging.info("TCP server: port 5000")
            while True:
                connection, _ = server.accept()
                with connection:
                    connection.settimeout(10)
                    try:
                        payload = validate_message(read_packet(connection))
                        client.messages_db.messages.insert_one({
                            "date": str(datetime.now()), **payload
                        })
                        connection.sendall(b'{"ok":true}\n')
                        logging.info("Message saved")
                    except (OSError, ValueError, PyMongoError):
                        logging.exception("Message processing failed")


def run_http_server():
    with ThreadingHTTPServer(("0.0.0.0", 3000), Handler) as server:
        logging.info("HTTP server: port 3000")
        server.serve_forever()


def stop(signum, frame):
    raise KeyboardInterrupt


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, stop)
    ready = Event()
    processes = [Process(target=run_socket_server, args=(ready,)),
                 Process(target=run_http_server)]
    try:
        processes[0].start()
        if not ready.wait(10):
            raise RuntimeError("Socket server did not start")
        processes[1].start()
        while all(process.is_alive() for process in processes):
            processes[1].join(timeout=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        for process in processes:
            if process.is_alive():
                process.terminate()
        for process in processes:
            if process.pid is not None:
                process.join()