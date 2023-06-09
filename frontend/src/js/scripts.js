/**
 * global variable for the websocket object
 */
let socket;

// this will automatically pick the websocket up, making the assumption that it runs on the same host as the Website
if (document.location.hostname === "frontend") {
    socket = new WebSocket('ws://backend:25500/', 'chat');
} else {
    socket = new WebSocket('ws://' + document.location.hostname + ':25500/', 'chat');
}


socket.onopen = sock_open
socket.onmessage = on_message
/**
 * Array containing all pending server requests, can be different as sent commands.
 * @type {string[]}
 */
let awaiting = [];

/**
 * calls load on socket connection established event
 */
function sock_open() {
    load();
}


/**
 * handles websocket answers by popping awaiting
 * @param msg
 */
function on_message(msg) {
    const data = JSON.parse(msg.data);
    let req = awaiting.pop();

    console.log(data)
    if (data.status !== 200){
        alert("Error Code "+data.status+" received")
        return
    }

    switch (req) {
        case 'help': {
            $('#help').remove();
            $('#main').append("<div id='help'><a id='status'>Status Code: </a><table id='help-table'>   " +
                "<tr><td>Command</td><td>Parameters</td><td>Regex</td><td>Description</td></tr>" +
                "</table></div>")
            $('#status').append(data.status);
            data.response.forEach((val, _, _1) => {
                $('#help-table').append("<tr id='help-tr'>" +
                    "<td>" + val.cmd + "</td>" +
                    "<td>" + val.params + "</td>" +
                    "<td>" + val.regex + "</td>" +
                    "<td>" + val.desc + "</td>" +
                    "</tr>");
            });
            break;
        }
        case 'dump': {
            $('#dump').remove();
            $('#main').append("<div id='dump'><a id='d-status'>Status Code: </a><br></div>")
            $('#d-status').append(data.status);
            $(`#dump`).append(msg.data);
            break;
        }
        case 'getSetting':{
            currentSet(data.response.rotor_order, data.response.rotors)
            return;
        }
        case 'encrypt': {
            letter_received(data.response);
            break;
        }
        case 'load': {
            awaiting.push('getSaveData')
            sendRequest('dump')
            break
        }
        case 'getSaveData': {
            setOffsetDisplay(data.response.rotor_order, data.response.rotors)
            setPlugboard(data.response.plugboard)
            break
        }
        //case 'rotors:set': {
          //  alert('Rotors successfully set')
           // break
        //}
        //case 'rotors:offset': {
           // alert('Offset successfully set')
            //break
        //}
    }
}

/**
 * Used to send requests to the websocket server. A push to awaiting is necessary before calling this function.
 * @param cmd - main command
 * @param sub - sub command
 * @param params - command parameter
 */
function sendRequest(cmd, sub, params) {
    if (sub == null && params == null) {
        socket.send('{"cmd": "' + cmd + '"}');
    } else if (sub == null && params != null) {
        socket.send('{"cmd": "' + cmd + '", "params": "' + params + '"}');
    } else if (params == null && sub != null) {
        socket.send('{"cmd": "' + cmd + '", "sub_cmd": "' + sub + '"}');
    } else {
        socket.send('{"cmd": "' + cmd + '", "sub_cmd": "' + sub + '", "params": "' + params + '"}');

    }
}
