import asyncio
import websockets
import json

async def connect_to_websocket():
    ws_url = "wss://ai.comfly.chat/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
    headers = [
        ("Authorization", "Bearer sk-OD0ecDsrOcRcpQHT9532001481374a278aC86c1c199c2cDf"),
        ("OpenAI-Beta", "realtime=v1")
    ]
    print(f"Connecting to WebSocket: {ws_url} with headers: {headers}")

    try:
        async with websockets.connect(ws_url, extra_headers=headers) as websocket:
            print("Connected to WebSocket.")
            await websocket.send(json.dumps({"type": "test"}))
            response = await websocket.recv()
            print("Response:", response)
    except Exception as e:
        print(f"WebSocket connection failed: {e}")

asyncio.run(connect_to_websocket())