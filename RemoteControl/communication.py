# -*- coding: cp1251 -*-
from time import sleep
import sys, signal, requests
import os, errno
import socket
import pprint
import logging
import json
from multiprocessing import Process, freeze_support

db = {}
sock = socket.socket()
host = '84.252.134.63'
auth_token = 'Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIxNTUxNjUxfQ.jAIgdvTbsN2uV7B75FDj_QvOuxFOa6Iey3AqbDl9WXg'

def handler(signum, frame):
    print('Terminating main program')
    sock.close()
    sys.exit(1)

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGILL, handler)
signal.signal(signal.SIGABRT, handler)
signal.signal(signal.SIGTERM, handler)

def fun(port_manager, port_streamer):
    print('start translation')
    print(port_manager, port_streamer)
    streamer = None
    sock_manager = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_streamer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_manager.bind(('0.0.0.0', port_manager))
    sock_streamer.bind(('0.0.0.0', port_streamer))
    data, client_address = sock_manager.recvfrom(1024)
    sock_manager.setblocking(0)
    while True:
        try:
            data, new_address = sock_manager.recvfrom(1024)
            if data == 'reconnect':
                print ('Client reconnect')
                client_address = new_address
            elif streamer:
                sock_streamer.sendto(data, streamer)
                print(streamer, data)
        except Exception as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                #print (err) #11
                data, streamer = sock_streamer.recvfrom(1316)
                sent = sock_manager.sendto(data, client_address)
                continue
            else:
                sock_manager.close()
                sock_streamer.close()
                print(e)

def check_connection(auth_token, device_id):
    print('Device ID is ', device_id)
    try:
        response = requests.post('http://84.252.134.63:8000/config', headers={'Authorization': auth_token},  json={"id": int(device_id)})
        if response.status_code == 200:
            device = json.loads(response.text)
            if device['isReady']:
                if db.get(auth_token) is None:
                    db.update({auth_token: {device_id: None}})
                elif db.get(auth_token).get(device_id) is None:
                    db.get(auth_token).update({device_id: None})
                return True
            else:
                db.get(auth_token).update({device_id: None})
                return False

    except BaseException as e:
        print("Unexpected error:", pprint.pformat(e))
        logging.error("Unexpected error: {0}".format(pprint.pformat(e)))


if __name__ == '__main__':
    freeze_support()
    procs = []

    server_address = '0.0.0.0'
    server_port = 31337

    server = (server_address, server_port)
    sock.bind(server)
    sock.listen(1)

    while True:
        print('wait connection')
        conn, addr = sock.accept()
        print('socket accepted!')
        data = conn.recv(1024).split()
        print('after receive:', data)
        print('data length = ', len(data))
        tok = data[1] + b' ' + data[2]
        token = tok.decode('UTF-8')
        side = data[0].decode('UTF-8')
        data3 = data[3].decode('UTF-8')
        print('My token is ', token)
        if len(data) == 4 and check_connection(token, data[3]):
            #data[1] is a token. AND data[2] is data[3]
            if db.get(token).get(data[3]) is None or db.get(token).get(data[3]).get(data[0]) is None:
                print('init')
                udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_sock.bind(('0.0.0.0', 0))
                if db.get(token).get(data[3]) is not None:
                    db.get(token).get(data[3]).update({side: udp_sock.getsockname()[1], 'conn'+side: conn})
                else:
                    db.update({token: {data[3]: {side: udp_sock.getsockname()[1], 'conn'+side: conn}}})
                print("Database after check connection and init: ", db)
            else:
                print('reconnect')
                conn.send(str(db.get(token).get(data[3]).get(data[0])).encode('utf-8'))
                conn.close()
            if db.get(token).get(data[3]).get('ctrl') is not None and db.get(token).get(data[3]).get('video') is not None and db.get(token).get(data[3]).get('isRunning') is None:
                print('translation')
                procs.append(Process(target=fun, args=(db.get(token).get(data[3]).get('ctrl'), db.get(token).get(data[3]).get('video'))))
                udp_sock.close()
                procs[-1].start()
                print(str(db.get(token).get(data[3]).get('ctrl')))
                print (str(db.get(token).get(data[3]).get('video')))
                db.get(token).get(data[3]).get('connctrl').send(str(db.get(token).get(data[3]).get('ctrl')).encode('utf-8'))
                db.get(token).get(data[3]).get('connvideo').send(str(db.get(token).get(data[3]).get('video')).encode('utf-8'))
                db.get(token).get(data[3]).get('connctrl').close()
                db.get(token).get(data[3]).get('connvideo').close()
                db.get(token).get(data[3]).update({'isRunning': True})
                print("database after translation: ", db)

        else:
            print('ошибка данных')
            conn.close()
        print('end')
        sleep(1)
    print('завершается родительский процесс')