#!/usr/bin/env python
import os
"""
Example server for NNG4, SSL version. It will read environment variables
NNG4CERT: path to a fullchain SSL certificate
NNG4KEY: path to a SSL private key
NNG4PORT: port to use
NNG4IP: (local) server IP
"""
import signal
import asyncio
from pathlib import Path
from asyncio.subprocess import Process, PIPE
import ssl

from websockets.server import serve, WebSocketServerProtocol


ssl_cert = os.environ.get('NNG4CERT', 'fullchain.pem')
ssl_key = os.environ.get('NNG4KEY', 'privkey.pem')
port = int(os.environ.get("NNG4PORT", "8765"))
ip = os.environ.get("NNG4IP", "192.168.0.10")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(ssl_cert, keyfile=ssl_key)

BIN_FOLDER = Path(__file__).parent / "build" / "bin"

async def write_stdout(proc: Process, msg : str) -> None:
    """Write the given msg string to the given process stdin
    and wait until stdin has been drained."""
    assert proc.stdin is not None
    proc.stdin.write(msg.encode())
    await proc.stdin.drain()

async def get_stdout_json_str(proc: Process) -> str:
    """Hacky way to read stdout until some valid json string is read."""
    assert proc.stdout is not None
    resp = ""
    while not resp.endswith("}\n"):
        piece = await proc.stdout.readline()
        resp += piece.decode()
    return resp.strip()

async def handler(websocket: WebSocketServerProtocol) -> None:
    proc: Process = await asyncio.create_subprocess_exec(
        BIN_FOLDER /"nng",
        cwd=BIN_FOLDER,
        stdin=PIPE, stdout=PIPE, stderr=PIPE)
    await websocket.send("ok")
    try:
        async for message in websocket:
            assert type(message) is str
            await write_stdout(proc, message + "\n")
            resp: str = await get_stdout_json_str(proc)
            await websocket.send(resp)

    finally:
        proc.terminate()
        del proc

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with serve(handler, ip, port, ssl=ssl_context):
        await stop

if __name__ == "__main__":
    asyncio.run(main())
