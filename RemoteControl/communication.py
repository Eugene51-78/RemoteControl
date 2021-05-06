# -*- coding: cp1251 -*-
from time import sleep
import sys, signal, requests
import os, errno
import socket
from multiprocessing import Process, freeze_support

db = {}
sock = socket.socket()
host = '84.252.134.63'
auth_token = 'Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIwMjkxOTI1fQ.Suk1-DBN25JH_IZwcggBdDngxWuaQZabn9cZNJqXNEs'

def handler(signum, frame):
    print('Terminating main program')
    # remove_pid()
    sock.close()
    sys.exit(1)


signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGILL, handler)
signal.signal(signal.SIGABRT, handler)
signal.signal(signal.SIGTERM, handler)


def fun(pctrl, pvideo):
    print
    'start process '
    print
    pctrl, pvideo
    host = None
    ctrl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ctrl.bind(('0.0.0.0', pctrl))
    video.bind(('0.0.0.0', pvideo))
    print
    'Wait'
    data, client_address = ctrl.recvfrom(1024)
    ctrl.setblocking(0)
    while True:
        try:
            data, new_address = ctrl.recvfrom(1024)
            if data == 'reconnect':
                print
                'Client reconnect'
                client_address = new_address
            elif host is not None:
                sent = video.sendto(data, host)
        except e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                data, host = video.recvfrom(1316)
                sent = ctrl.sendto(data, client_address)
                # sleep(1)
                continue
            else:
                # a "real" error occurred
                ctrl.close()
                video.close()
                print
                e
                # sys.exit(1)


def check_connection(auth_token, device_id):
    try:
        response = requests.get('http://84.252.134.63:8000/config', headers={'Authorization': auth_token})
        print (response)
        if response.get('success') == True:
            if response.get('data').get('is_connect'):
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
        print('after receive')
        print(data)
        if len(data) == 4:
            print('we have 4 length')
        token = data[1] + b' ' + data[2]
        print('My token is ', token)
        if len(data) == 4 and check_connection(token, data[2]):
            if db.get(data[1]).get(data[2]) is None or db.get(data[1]).get(data[2]).get(data[0]) is None:
                print
                'init'
                udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_sock.bind(('0.0.0.0', 0))
                if db.get(data[1]).get(data[2]) is not None:
                    db.get(data[1]).get(data[2]).update({data[0]: udp_sock.getsockname()[1], 'conn' + data[0]: conn})
                else:
                    db.update({data[1]: {data[2]: {data[0]: udp_sock.getsockname()[1], 'conn' + data[0]: conn}}})
                    # conn.send(str(db.get(data[1]).get(data[2]).get(data[0])))
                # udp_sock.close()
                # conn.close()
            else:
                print
                'reconnect'
                conn.send(str(db.get(data[1]).get(data[2]).get(data[0])))
                conn.close()
            if db.get(data[1]).get(data[2]).get('ctrl') is not None and db.get(data[1]).get(data[2]).get(
                    'video') is not None and db.get(data[1]).get(data[2]).get('isRunning') is None:
                print
                'translation'
                procs.append(Process(target=fun, args=(
                db.get(data[1]).get(data[2]).get('ctrl'), db.get(data[1]).get(data[2]).get('video'))))
                udp_sock.close()
                procs[-1].start()
                print
                str(db.get(data[1]).get(data[2]).get('ctrl'))
                print
                str(db.get(data[1]).get(data[2]).get('video'))
                db.get(data[1]).get(data[2]).get('connctrl').send(str(db.get(data[1]).get(data[2]).get('ctrl')))
                db.get(data[1]).get(data[2]).get('connvideo').send(str(db.get(data[1]).get(data[2]).get('video')))
                db.get(data[1]).get(data[2]).get('connctrl').close()
                db.get(data[1]).get(data[2]).get('connvideo').close()
                db.get(data[1]).get(data[2]).update({'isRunning': True})

        else:
            print('ошибка данных')
            conn.close()
        print('end')
        sleep(1)
    print('завершается родительский процесс')