import asyncio

class ChatServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print('connection from {}'.format(self.peername))
        self.transport = transport

    def data_received(self, data):
        msg = data.decode()
        #parsing the message
        if msg.startswith("usr:"): #receiving username on connection -> record the new user
            self.username = msg[4:]
            record_new_user(self)
        elif msg.startswith("msg:"): #receiving a message -> echo it to everyone except the author
            broadcast((self.username+': '+msg[4:]), self)
        elif msg == 'x': #receiving exit command -> close connection with the user
            remove_user(self)
            self.transport.close()

users = []

def record_new_user(user):
    users.append(user)
    broadcast(user.username+' has joined!', user, True)

def remove_user(user):
    users.remove(user)
    broadcast(user.username+' has left.', user)

def broadcast(msg, author, to_author=False):
    print(msg)
    for user in users:
        if user is not author:
            user.transport.write(msg.encode())

loop = asyncio.get_event_loop()
chat = loop.create_server(ChatServer, '127.0.0.1', 8888)
server = loop.run_until_complete(chat)
print('serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("exit")
finally:
    server.close()
    loop.close()