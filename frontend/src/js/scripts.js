let socket;

// this will automatically pick the websocket up, making the assumption that it runs on the same host as the Website
socket = new WebSocket('ws://' + document.location.hostname + ':25500/', 'chat');

socket.onopen = sock_open
socket.onmessage = on_message
let awaiting = [];

function sock_open() {
    // sendRequest("help");
}

function on_message(msg) {
    var data = JSON.parse(msg.data);
    let req = awaiting.pop();

    switch (req) {
        case 'help': {
            $('#help').remove();
            $('#main').append("<div id='help'><a id='status'>Status Code: </a><table id='help-table'>   " +
                "<tr><td>Command</td><td>Parameters</td><td>Regex</td><td>Description</td></tr>" +
                "</table></div>")
            $('#status').append(data.status);
            data.response.forEach((val, index, array) => {
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
        }
        case 'encrypt': { letter_received(data.response); }
    }

}

/*
Use this for sending requests to the websocket...
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
