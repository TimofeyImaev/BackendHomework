import socket
import websockets
import asyncio

HELLO_MY_NAME_IS = socket.gethostname()
print(f"Hello my name is {HELLO_MY_NAME_IS}")

MY_IP = socket.gethostbyname(HELLO_MY_NAME_IS)
print(f"My IP address is {MY_IP}")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect(('8.8.8.8', 53))
    MY_IP = s.getsockname()[0]

print(MY_IP)

async def register_client(websocket, _):
    async for message in websocket:
        print(message)

async def main():
    async with websockets.serve(register_client, MY_IP, 8080):
        await asyncio.Future()  # Запускает сервер навсегда

if __name__ == "__main__":
    asyncio.run(main())