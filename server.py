#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import random
import websockets
import json
import ssl
import datetime
import pathlib
import logging
from r2labprot import *
from argparse import ArgumentParser as AP

USERS = set()


parser = AP()
parser.add_argument("-a", "--address", default="127.0.0.1",
                    help="specify the address the websocket will be listening \
                          to")
parser.add_argument("-p", "--port", default= "8765",
                    help="define port for websocket")
parser.add_argument("-k", "--key", default="key.pem",
                    help="define path of the private key file")
parser.add_argument("-c", "--cert", default="cert.pem",
                    help="define path of certificate file containing\
                          the public key")
parser.add_argument("-s", "--secure", default=False, action='store_true',
                    help="Enable SSL/TLS for websocket")
parser.add_argument("-d", "--debug", default=False, action='store_true',
                    help="Enable debug mode")
args = parser.parse_args()
ws_ip     = args.address
ws_port   = int(args.port)
key_path  = pathlib.Path(args.key)
cert_path = pathlib.Path(args.cert)
ssl_tls   = args.secure
debug     = args.debug

async def publish_info():
    while True:
        for websocket, type, start, end in USERS:
            message = await info_req({'action': PUBLISH, 'type': type,
                                      'payload': {'start': start, 'end': end,
                                      'list': False}})
            #message = create_message(PUBLISH, payload=f"Hello {type}")
            msg = json.dumps(message)
            await websocket.send(msg)
        await asyncio.sleep(random.random() * 3)

async def is_already_registered(websocket):
    websock = [ws for ws, _type, start, end in USERS]
    return websocket in websock
async def update_register(websocket, type, start, end):
    tuples = [tuple for tuple in USERS if websocket in tuple]
    for tuple in tuples:
        USERS.remove(tuple)
    USERS.add((websocket, type, start, end))

async def register(websocket, type, payload):
    ret = await is_already_registered(websocket)
    answer = "OK"
    try :
        if not ret:
            USERS.add((websocket, type, payload['start'], payload['end']))
        else:
            await update_register(websocket, type, payload['start'],
                                  payload['end'])
    except Exception as e :
        answer = e
    return create_message(INFO_REQ, type,
                            payload=answer)

async def unregister(websocket):
    tuples = [tuple for tuple in USERS if websocket in tuple]
    type = None
    answer = "Not registered"
    for tuple in tuples:
        answer = "OK"
        USERS.remove(tuple)
        type = tuple[1]
    return create_message(UNREGISTER, type, payload=answer)

async def info_req(data):
    type = data['type']
    if type == I_RUN:
        payload = await getruninfo(data['payload'])
    if type == I_BOOK:
        payload = await getbookinfo(data['payload'])
    return create_message(data['action'], data['type'],
                            payload=payload)


async def getruninfo(payload):
    start = datetime.datetime\
                .strptime(payload['start'], "%Y-%m-%dT%H:%M:%S")
    end = datetime.datetime\
                .strptime(payload['end'], "%Y-%m-%dT%H:%M:%S")
    # Access DB to get info's that should be display on the RUN page
    # And format them in a dictionary
    return "bla_RUN info"


async def getbookinfo(payload):
    # Dates are in iso format - Should we let it that way?
    start = datetime.datetime\
                .strptime(payload['start'], "%Y-%m-%dT%H:%M:%S")
    end = datetime.datetime\
                .strptime(payload['end'], "%Y-%m-%dT%H:%M:%S")
    if not payload['list']:
        # Access DB to get info's that should be display on the BOOK page
        # And format them in a dictionary
        pass
    else:
        # Only fetch the list of the reservation for the timestamp
        pass
    return "bla_BOOK info"
async def book(data):
    type = data['type']
    if type == UPDATE:
        payload = await book_update(data['payload'])
    if type == CREATE:
        payload = await book_create(data['payload'])
    if type == DELETE:
        payload = await book_delete(data['payload'])
    return create_message(data['action'], data['type'],
                            payload=payload)


async def book_create(payload):
    slices = payload
    result = []
    for slice in slices:
        slice_name = slice['name']
        start = slice['start']
        end = slice['end']
        result.append({'name': slice_name, 'start': start, 'status': "ok"})
    return result


async def book_update(payload):
    slices = payload
    result = []
    for slice in slices:
        slice_name = slice['name']
        old_start = slice['old_start']
        new_start = slice['new_start']
        old_end = slice['old_end']
        new_end = slice['new_end']
        #access db to modify slices
        result.append({'name': slice_name, 'start': old_start, 'status': "ok"})
    return result


async def book_delete(payload):
    slices = payload
    result = []
    for slice in slices:
        slice_name = slice['name']
        start = slice['start']
        result.append({'name': slice_name, 'start': start, 'status': "ok"})
    return result

async def irc_stuff():
    # TODO?
    pass
async def manage_slices(data):
    type = data['type']
    if type == GET:
        payload = await get_slice_info(data['payload'])
    if type == ADD_KEY:
        payload = await add_key(data['payload'])
    if type == RM_KEY:
        payload = await add_key(data['payload'])
    if type == RENEW:
        payload = await renew_slice(data['payload'])
    return create_message(data['action'], data['type'],
                                payload=payload)

async def get_slice_info(payload):
    user = payload['user']
    result = {}
    # Access db to get every slice + slices info relative to the user
    slices = [{'name': "inria_batman", 'expiration': "2018-06-27"},
              {'name': "inria_school", 'expiration': "2018-06-27"},
              {'name': "inria_r2lab.tutorial", 'expiration': "2018-06-27"}
              ]
    keys = ["key1", "key2"]
    result['slices'] = slices
    result['keys'] = keys
    return result

async def add_key(payload):
    keys = [key for key in payload['keys']]
    user = payload['user']
    result = []
    ## Access db to register the keys
    for i in range(1, len(keys)+1):
        result.append({'key': f"key{i}", 'status': "OK"})
    return result

async def rm_key(payload):
    keys = [key for key in payload['keys']]
    user = payload['user']
    result = []
    ## Access db to register the keys
    for i in range(1, len(keys)+1):
        result.append({'key': f"key{i}", 'status': "OK"})
    return result

async def renew_slice(payload):
    slice_names = [slice for slice in payload['slices']]
    user = payload['user']
    result = []
    ## Access db to renew slices for the given user
    for i in slice_names:
        result.append({'slice_name': f"{i}", 'status': "OK"})
    return result

async def request_rcv(websocket, path):
    try:
        while True:
            message = await websocket.recv()
        #async for message in websocket:
            msg = json.loads(message)
            print(f"{msg} message recieve")
            if msg['action'] == UNREGISTER:
                answer = await unregister(websocket)
            if msg['action'] == REGISTER:
                answer = await register(websocket, msg['type'], msg['payload'])
            if msg['action'] == INFO_REQ:
                answer = await info_req(msg)
            if msg['action'] == BOOK:
                answer = await book(msg)
            if msg['action'] == SLICES:
                answer = await manage_slices(msg)
            #message = message + " Truc"
            #await websocket.send(message)
            asw = json.dumps(answer)
            await websocket.send(asw)
            #data = json.loads(message)
            #if data['action'] == "reqinfo":
            #    pass
    except websockets.exceptions.ConnectionClosed:
        await unregister(websocket)
if debug:
    logger = logging.getLogger('websockets')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

ssl_context = None
if ssl_tls:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=cert_path,
                                keyfile=key_path)
start_server = websockets.serve(request_rcv, ws_ip, ws_port,
                                ssl=ssl_context)
aloop = asyncio.get_event_loop()
aloop.create_task(publish_info())
aloop.run_until_complete(start_server)
aloop.run_forever()
