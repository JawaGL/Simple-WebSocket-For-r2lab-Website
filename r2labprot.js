// Previewer.js
// LIBRARY CLASS
//#############################
//# Action parameter
//#############################
//# CLIENT REQUEST
var REGISTER = "register";
var UNREGISTER = "unregister";
var INFO_REQ = "info_request";
var BOOK = "book";
var SLICES = "slices_mngt";

//# SERVER RESPONSE
var PUBLISH = "publishing service";
var REQ_ANSWER = "answer to request";

//#############################
//# Type for INFO_REQ & REGISTER
//#############################
var I_RUN = "run";
var I_BOOK = "book";

//#############################
//# Type for BOOK
//#############################
var UPDATE = "update";
var CREATE = "create";
var DELETE = "delete";
//#############################
//# Type for SLICES
//#############################
var GET = "get";
var ADD_KEY = "add_key";
var RM_KEY = "remove_key";
var RENEW = "renew";

function preparemessage(){
  var msg= {
              action : "None",
              type : "None",
              payload : {

              }

            };
  return msg;
}

//#############################
//# UTILS METHOD
//#############################


function create_message(action, type="None", payload="None"){
    var message = preparemessage();
    message['action'] = action;
    if(type != "None"){
        message['type'] = type;
    }
    if(payload !="None"){
        message['payload'] = payload;
    }
    return message;
}
//#############################
//# REGISTER
//#############################
function ask_register(TYPE, shedule_start, schedule_end){
    payload = {};
    payload['start'] = shedule_start;
    payload['end'] = schedule_end;
    return create_message(REGISTER, TYPE, payload);
}
function ask_unregister(){
    return create_message(UNREGISTER);
}

//#############################
//# BOOK
//#############################
function ask_book_info(start, end, list=false){
    payload = {};
    payload['start'] = start;
    payload['end'] = end;
    payload['list'] = list;
    return create_message(INFO_REQ, I_BOOK, payload);
}

function update_request(name, start, end, new_start="None", new_end="None"){
    if (new_start == "None"){
        new_start = start;
    }
    if (new_end == "None"){
        new_end = end;
    }
    update_info = {};
    update_info['name'] = name;
    update_info['old_start'] = start;
    update_info['old_end'] = end;
    update_info['new_end'] = new_end;
    update_info['new_start'] = new_start;
    return update_info;
}
function create_request(name, start, end){
      create_info = {};
      create_info['name'] = name;
      create_info['start'] = start;
      create_info['end'] = end;
      return create_info;
}

function delete_request(name, start){
      delete_info = {};
      delete_info['name'] = name;
      delete_info['start'] = start;
      return delete_info;
}
function ask_book_modify(TYPE, request){
      return create_message(BOOK, TYPE, request);
}
//#############################
//# SLICES
//#############################
function ask_slices_info(user){
    payload = {'user': user};
    message = create_message(SLICES, GET, payload);
    return message;
}
function ask_modify_keys(TYPE ,keys, user){
    payload = {};
    payload['keys'] = [];
    for(let key of keys){
      payload['keys'].push(key);
    };
    payload['user'] = user;
    message = create_message(SLICES, TYPE, payload);
    return message;
}
function ask_renew_slice(user, slice_names){
    payload = {};
    payload['slices']= [];
    for(let name of slice_names){
      payload['slices'].push(name);
    }
    payload['user'] = user;
    message = create_message(SLICES, RENEW, payload);
    return message;
}
