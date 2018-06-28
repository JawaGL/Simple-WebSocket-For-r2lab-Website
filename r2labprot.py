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
    """
    Create a message under the form of a dictionary to trasfer it in JSON
    Action represent the request of message
    Type represent the type of the requested
    Payload vary but will contain the effective information
    """
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
    """
    Create a message to ask a registration to the server
    TYPE is either I_RUN or I_BOOK. I_RUN register you to the RUN INFO
    multicat. I_BOOK to the BOOK info.
    schedule_start and schedule_end define the start and the end of the
    time slots display of the reservation.
    Uppon receiption, the server will either add the socket to the multicast
    or modify it with the new information.
    """
    payload = {}
    payload['start'] = shedule_start.isoformat()
    payload['end'] = schedule_end.isoformat()
    return create_message(REGISTER, TYPE, payload)


def ask_unregister():
    """
    Tell the server to unsubscribe you from the diffusion list
    """
    return create_message(UNREGISTER)

#############################
# BOOK
#############################
def ask_book_info(start, end):
    """
    Message to tell the server to give you information about the time slots
    booked.

    Start : Begining of the time slot window you are considering
    end   : end of the said time slots
    """
    payload = {}
    payload['start'] = start.isoformat()
    payload['end'] = end.isoformat()
    return create_message(INFO_REQ, I_BOOK, payload)


def update_request(name, start, end, new_start=None, new_end=None):
    """
    Generate payload to update 1 slice. This **DOES NOT** generate a complete,
    message
    name : name of the slice
    start : initial begining of the reservation
    end : initial end of the reservation
    new_start : new value for the start parameter. If is None, it will remain
                intact
    new_end  : new value for the end parameter. If is None, it will remain
               intact

    Common usage :
            payload = [update_request(aname, astart,
                                      aend, anewstart, anewend)
                       for aname, astart, aend,
                           anewstart, anewend in SHouldBeUpdated]
    """
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
    """
    Generate payload to create 1 slice reservation. This **DOES NOT** generate
    a complete message.

    name : name of the slice
    start :  begining of the reservation
    end :  end of the reservation

    Common usage :
            payload = [update_request(aname, astart, aend)
                       for aname, astart, aend, in SHouldBeCreated]
    """
    create_info = {}
    create_info['name'] = name
    create_info['start'] = start.isoformat()
    create_info['end'] = end.isoformat()
    return create_info


def delete_request(name, start):
    """
    Generate payload to delete 1 slice reservation. This **DOES NOT** generate
    a complete message.

    name : name of the slice
    start :  begining of the reservation

    Common usage :
            payload = [update_request(aname, astart)
                       for aname, astart in SHouldBeDeleted]
    """
    delete_info = {}
    delete_info['name'] = name
    delete_info['start'] = start.isoformat()
    return delete_info


def ask_book_modify(TYPE, request):
    """
    Create a message to ask the server to manage reservations.

    TYPE : is UPDATE, CREATE or DELETE
    request : is the payload generated by function ****_request(*)
    """
    return create_message(BOOK, TYPE, request)
#############################
# SLICES
#############################


def ask_slices_info(user):
    """
    Create a message to ask the server to get the user's slices information.

    The server respond : {'slices': [{'name': slice_name,
                                      'expiration': expiration}, ...],
                          'keys': [key1, key2, ...] }

    user : is the user for which we want the information
    """
    payload = {'user': user}
    message = create_message(SLICES, GET, payload)
    return message

def ask_modify_keys(TYPE ,keys, user):
    """
    Create a message to ask the server to either add or remove keys
    for a given user.

    TYPE : either RM_KEY or ADD_KEY
    keys : list of keys
    user : the user for which we want the modification xxx SECURITY !?
    """
    payload = {}
    payload['keys'] = [key for key in keys]
    payload['user'] = user
    message = create_message(SLICES, TYPE, payload)
    return message

def ask_renew_slice(user, slice_names):
    """
    Create a message to ask the server to  renew the validity of a slice
    xxx IS IT LIKE THIS IN THE DB?
    user : the user for which we want the renewal
    slice_names : the name of the slice to renew

    """
    payload = {}
    payload['slices'] = [name for name in slice_names]
    payload['user'] = user
    message = create_message(SLICES, RENEW, payload)
    return message
