#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import json
import datetime
import ssl
import pathlib
import logging
from r2labprot import *
from argparse import ArgumentParser as AP


parser = AP()
parser.add_argument("-a", "--address", default="127.0.0.1",
                    help="specify the address of the websocket")
parser.add_argument("-p", "--port", default= "8765",
                    help="define port for websocket")
parser.add_argument("-c", "--cert", default="cert.pem",
                    help="define path of certificate file containing\
                          the public key of the target cerv")
parser.add_argument("-s", "--secure", default=False, action='store_true',
                    help="Enable SSL/TLS for websocket")
parser.add_argument("-d", "--debug", default=False, action='store_true',
                    help="Enable debug mode")
args = parser.parse_args()
ws_ip     = args.address
ws_port   = int(args.port)
cert_path = pathlib.Path(args.cert)
ssl_tls   = args.secure
debug     = args.debug

async def service_listener(websocket):
    while 1:
        message = await websocket.recv()
        msg = json.loads(message)
        await handle_answer(msg)

#    await asyncio.sleep(1)


async def handle_answer(msg):

    action = msg['action']
    type   = msg['type']
    payload= msg['payload']

    if action == PUBLISH:
        if type == I_RUN:
            display_run(payload)
        if type == I_BOOK:
            display_book(payload)
    else:
        if action == UNREGISTER:
            handle_unregister(payload)
        if action == REGISTER:
            handle_register(type, payload)
        if action == INFO_REQ:
            handle_info_req(type, payload)
        if action == BOOK:
            handle_book(type, payload)
        if action == SLICES:
            handle_manage_slices(type, payload)


def display_run(data):
    print(f"This is a run info and server responded : {data}")
    #TODO parse different info
def display_book(data):
    print(f"This is a book info and server responded : {data}")
    #TODO parse different info
def handle_unregister(payload):
    print(f"Answer received for unregister : {payload}")
def handle_register(type, payload):
    if type == I_RUN:
        print(f"Registration for RUN service : {payload}")
    if type == I_BOOK:
        print(f"Registration for BOOK service : {payload}")
def handle_info_req(type, payload):
    if type == I_RUN:
        display_run(payload)
    if type == I_BOOK:
        display_book(payload)
def handle_book(type, payload):
    if type == UPDATE:
        for item in payload:
            print(f"Reservation with {item['name']} starting at\
                  {item['start']} update : {item['status']}")
    if type == CREATE:
        for item in payload:
            print(f"Reservation with {item['name']} starting at\
                  {item['start']} create : {item['status']}")
    if type == DELETE:
        for item in payload:
            print(f"Reservation with {item['name']} starting at\
                  {item['start']} delete : {item['status']}")


def handle_manage_slices(type, payload):
    GET = "get"
    ADD_KEY = "add_key"
    RM_KEY = "remove_key"
    RENEW = "renew"
    if type == GET:
        for item in payload['slices']:
            print(f"Slice : {item['name']} Exp : {item['expiration']}")
        for item in payload['keys']:
            print(f"Key : {item}")
    if type == ADD_KEY:
        for item in payload:
            print(f"Add key {item['key']} : {item['status']}")
    if type == RM_KEY:
        for item in payload:
            print(f"Remove key {item['key']} : {item['status']}")
    if type == RENEW:
        for item in payload:
            print(f"Renew slice {item['slice_name']} : {item['status']}")


async def connect(ssl_context):
    return await websockets.connect('wss://localhost:8765', ssl=ssl_context)

async def sender(websocket):
    #while 1:
    #    resp = input("chose what to send : ")
        start = datetime.datetime.now().replace(hour=0, minute=0, second=0,
                                               microsecond=0)
        end = start + datetime.timedelta(hours=23, minutes=59,
                                         seconds=59, microseconds=0)
        #message = ask_register(I_RUN, start, end)
        #msg = json.dumps(message)
        #await websocket.send(msg)
        #await asyncio.sleep(4)
        #message = ask_register(I_BOOK, start, end)
        #msg = json.dumps(message)
        #await websocket.send(msg)
        #await asyncio.sleep(4)
        message = ask_unregister()
        msg = json.dumps(message)
        await websocket.send(msg)
        await asyncio.sleep(4)
        do = True
        if do:
            start = datetime.datetime.now().replace(hour=0, minute=0, second=0,
                                                   microsecond=0)
            end = start + datetime.timedelta(days=2, hours=23, minutes=59,
                                             seconds=59, microseconds=0)
            message = ask_book_info(start, end)
            msg = json.dumps(message)
            await websocket.send(msg)
            await asyncio.sleep(4)
            payload = [update_request("inria_batman", start.replace(hour=8,
                                                                   minute=30),
                                      start + datetime.timedelta(hours=2))
                                      for i in range(3)]
            message = ask_book_modify(UPDATE, payload)
            msg = json.dumps(message)
            await websocket.send(msg)
            await asyncio.sleep(4)
            payload = [create_request("inria_batman", start.replace(hour=8,
                                                                    minute=55),
                                      start.replace(hour=8, minute=55)
                                      + datetime.timedelta(hours=i))
                                      for i in range(3)]
            message = ask_book_modify(CREATE, payload)
            msg = json.dumps(message)
            await websocket.send(msg)
            await asyncio.sleep(4)
            payload = [create_request("inria_batman", start.replace(hour=9,
                                                                    minute=34),
                                      start.replace(hour=9, minute=34)
                                      + datetime.timedelta(hours=i))
                                      for i in range(3)]
            message = ask_book_modify(DELETE, payload)
            msg = json.dumps(message)
            await websocket.send(msg)
            await asyncio.sleep(4)
            message = ask_slices_info("ybleyfue")
            msg = json.dumps(message)
            await websocket.send(msg)
            await asyncio.sleep(4)
            message = ask_modify_keys(ADD_KEY, ["key1", "key2"], "ybleyfuez")
            msg = json.dumps(message)
            await websocket.send(msg)
            await asyncio.sleep(4)
            message = ask_modify_keys(RM_KEY, ["key1", "key2"], "ybleyfuez")
            msg = json.dumps(message)
            await websocket.send(msg)
            await asyncio.sleep(4)
            message = ask_renew_slice("ybleyfuez", ["inria_batman",
                                                    "inria_school"])
            msg = json.dumps(message)
            await websocket.send(msg)
            await asyncio.sleep(4)
ssl_context = None
if ssl_tls:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.load_verify_locations(pathlib.Path('cert.pem'))
if debug:
    logger = logging.getLogger('websockets')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
websocket = asyncio.get_event_loop().run_until_complete(connect(ssl_context))

asyncio.get_event_loop().create_task(service_listener(websocket))
asyncio.get_event_loop().run_until_complete(sender(websocket))
asyncio.get_event_loop().run_forever()
