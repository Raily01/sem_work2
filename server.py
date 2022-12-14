import socket
import threading

host = '127.0.0.1'
port = 5014

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)

clients = []
nicknames = []
numbers = ['', '']


def counting_res(word, cur):
    if cur.isnumeric():
        s = set()
        for i in cur:
            s.add(i)
        if len(s) != 4:
            return 'NOT CORRECT'.encode('utf-8')
        bulls = 0
        cows = 0
        for i in range(4):
            if word[i] == cur[i]:
                bulls += 1
            if cur[i] in word:
                cows += 1
        cows -= bulls
        res = 'bulls:' + str(bulls) + ', cows:' + str(cows)
        return res.encode('utf-8')
    else:
        return 'NOT CORRECT'.encode('utf-8')


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            index = clients.index(client)
            if numbers[index] == message.decode('utf-8'):
                broadcast(f'WIN {nicknames[index]}'.encode('utf-8'))
                client.close()
                break
            else:
                res = counting_res(numbers[index], message.decode('utf-8'))
                res = message + ': '.encode('utf-8') + res
                client.send(res)
                ind = clients.index(client)
                ind = (ind + 1) % 2
                clients[ind].send('1'.encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    for i in range(2):
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        client.send('NUMB'.encode('utf-8'))
        number = client.recv(1024).decode('utf-8')
        numbers[(i + 1) % 2] = number

        print("Nickname is {}, set numb {}".format(nickname, number))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
    broadcast(f'USER1 {nicknames[0]} {nicknames[1]}'.encode('utf-8'))


receive()
