#!/usr/bin/env python
import datetime
#############################
# Action parameter
#############################
# CLIENT REQUEST
REGISTER = "register"
UNREGISTER = "unregister"
INFO_REQ = "info_request"
BOOK = "book"
SLICES = "slices_mngt"

# SERVER RESPONSE
PUBLISH = "publishing service"
REQ_ANSWER = "answer to request"

#############################
# Type for INFO_REQ & REGISTER
#############################
I_RUN = "run"
I_BOOK = "book"

#############################
# Type for BOOK
#############################
UPDATE = "update"
CREATE = "create"
DELETE = "delete"
#############################
# Type for SLICES
#############################
GET = "get"
ADD_KEY = "add_key"
RM_KEY = "remove_key"
RENEW = "renew"

#############################
# UTILS METHOD
#############################


def create_message(action, type=None, payload=None):
    message = {}
    message['action'] = action
    if type is not None:
        message['type'] = type
    else:
        message['type'] = "None"
    if payload is not None:
        message['payload'] = payload
    else:
        message['payload'] = "None"
    return message
#############################
# REGISTER
#############################
def ask_register(TYPE, shedule_start, schedule_end):
    payload = {}
    payload['start'] = shedule_start.isoformat()
    payload['end'] = schedule_end.isoformat()
    return create_message(REGISTER, TYPE, payload)


def ask_unregister():
    return create_message(UNREGISTER)

#############################
# BOOK
#############################
def ask_book_info(start, end, list=False):
    payload = {}
    payload['start'] = start.isoformat()
    payload['end'] = end.isoformat()
    payload['list'] = list
    return create_message(INFO_REQ, I_BOOK, payload)


def update_request(name, start, end, new_start=None, new_end=None):
    if new_start is None:
        new_start = start
    if new_end is None:
        new_end = end
    update_info = {}
    update_info['name'] = name
    update_info['old_start'] = start.isoformat()
    update_info['old_end'] = end.isoformat()
    update_info['new_end'] = new_end.isoformat()
    update_info['new_start'] = new_start.isoformat()
    #payload = {'slices': update_info}
    return update_info


def create_request(name, start, end):
    create_info = {}
    create_info['name'] = name
    create_info['start'] = start.isoformat()
    create_info['end'] = end.isoformat()
    return create_info


def delete_request(name, start):
    delete_info = {}
    delete_info['name'] = name
    delete_info['start'] = start.isoformat()
    return delete_info

def ask_book_modify(TYPE, request):
    return create_message(BOOK, TYPE, request)
#############################
# SLICES
#############################


def ask_slices_info(user):
    payload = {'user': user}
    message = create_message(SLICES, GET, payload)
    return message

def ask_modify_keys(TYPE ,keys, user):
    payload = {}
    payload['keys'] = [key for key in keys]
    payload['user'] = user
    message = create_message(SLICES, TYPE, payload)
    return message

def ask_renew_slice(user, slice_names):
    payload = {}
    payload['slices'] = [name for name in slice_names]
    payload['user'] = user
    message = create_message(SLICES, RENEW, payload)
    return message
