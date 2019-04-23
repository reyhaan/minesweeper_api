import socketio

# asyncio
sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('####### I\'m connected!')

@sio.on('disconnect')
def on_disconnect():
    print('####### I\'m disconnected!')

sio.connect('https://shuttleup-kafka-server.herokuapp.com/socket.io/')
# sio.wait()