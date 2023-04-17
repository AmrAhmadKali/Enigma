let socket;

// this will automatically pick the websocket up, making the assumption that it runs on the same host as the Website
socket = new WebSocket('ws://' + document.location.hostname + ':25500/', 'chat');

socket.onopen = sock_open
socket.onmessage = on_message

function sock_open() {
    sendRequest("help");
}

function addEntry(val, index, array) {
    var container = $('#help');
    container.append("<tr id='help-tr'>" +
        "<td>" + val.cmd + "</td>" +
        "<td>" + val.params + "</td>" +
        "<td>" + val.desc + "</td>" +
        "</tr>");

}

function on_message(msg) {
    var data = JSON.parse(msg.data);
    /*
    TODO: Replace with actual logic
     */
    $('#status').append(data.status);
    data.response.forEach(addEntry);
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
        socket.send('{"cmd": "' + cmd + '", "sub": "' + sub + '"}');
    } else {
        socket.send('{"cmd": "' + cmd + '", "sub": "' + sub + '", "params": "' + params + '"}');

    }
}