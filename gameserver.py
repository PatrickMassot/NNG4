#!/usr/bin/env python
import os
import signal
import asyncio
from pathlib import Path
from asyncio.subprocess import Process, PIPE

from websockets.server import serve, WebSocketServerProtocol

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
    port = int(os.environ.get("PORT", "8765"))
    async with serve(handler, "", port):
        await stop

if __name__ == "__main__":
    asyncio.run(main())
