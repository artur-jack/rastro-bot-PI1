import websocket

def on_message(ws, message):
    print(f"{message}")

def on_open(ws):
    print("Conexão aberta")
    ws.send("Conectado ao servidor")

def on_close(ws, close_status_code, close_msg):
    print(f"Conexão fechada: {close_status_code} - {close_msg}")

def on_error(ws, error):
    print(f"Erro: {error}")

if _name_ == "_main_":
    websocket_url = "ws://192.168.4.1:81"

    ws = websocket.WebSocketApp(
        websocket_url,
        on_message=on_message,
        on_open=on_open,
        on_close=on_close,
        on_error=on_error
    )

    ws.run_forever()
