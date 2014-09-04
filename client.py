import asyncio, threading

class ChatClient(asyncio.Protocol):
    def __init__(self):
        self.name = input("Type your username: ")
        #Windows doesn't have non-blocking stdin. Hacky workaround: put input into a separate thread.
        #Is there a better way?
        t = threading.Thread(target=self.input_handler)
        t.daemon = True
        t.start()

    def input_handler(self):
        while True:
            msg = input()
            if msg == 'x':
                self.transport.write(msg.encode())
            else:
                self.transport.write(('msg:'+msg).encode())

    def connection_made(self, transport):
        print("Connection made")
        self.transport = transport
        transport.write(('usr:'+self.name).encode())

    def data_received(self, data):
        print(data.decode())

    def connection_lost(self, exc):
        print('server closed the connection')
        asyncio.get_event_loop().stop()

loop = asyncio.get_event_loop()
chat = loop.create_connection(ChatClient, '127.0.0.1', 8888)
loop.run_until_complete(chat)
loop.run_forever()
loop.close()