const key_event = function () {
    key_pressed(event.key)
};

let reset_clicked = false;

function listener_init() {
    document.addEventListener("keydown", key_event);

    $(window).bind('beforeunload', function(){
        if(reset_clicked===false){
            save().then(message => {
                setCookie(JSON.parse(message.data).response)
            })
            // event.preventDefault();
            return '1234'
        } });

    document.getElementById('showMenuBtn').addEventListener('click', function(){ showMenu() });

    document.getElementById('clearBtn').addEventListener('click', function(){ clearContainer() });

    document.getElementById('resetBtn').addEventListener('click', function(){
        if (window.confirm("Do you really want to delete all save data?")) {
            reset()
        }
    });

}

function reset() {
    reset_clicked = true
    deleteCookie()
    window.location.reload()
}

function remove_keydown_listener(){
    document.removeEventListener("keydown", key_event);
}

function save(timeout = 10000){
    return new Promise((resolve, reject) => {
        let timer;

        awaiting.push('save');
        sendRequest('save');


        function responseHandler(message) {
            // resolve promise with the value we got
            resolve(message);
            clearTimeout(timer);
        }

        socket.onmessage = responseHandler;

        // set timeout so if a response is not received within a
        // reasonable amount of time, the promise will reject
        timer = setTimeout(() => {
            reject(new Error("timeout waiting for save"));
            socket.onmessage = on_message
        }, timeout);
    });
}

function load(){
    console.log(isCookieSaved())
    if(isCookieSaved()){
        awaiting.push('load')
        sendRequest('load', null, getCookie())
    }
}

function clearContainer(){
    document.querySelector(".inputContainer").innerText = ''
    document.querySelector(".outputContainer").innerText = ''
    $("[name^=l_]").css('background-color', 'white')
}

function key_pressed(key){
    key = key.toUpperCase()
    const alphabet = ['Q','W','E','R','T','Z','U','I','O','P','L','K','J','H','G','F','D','S','A','Y','X','C','V','B','N','M', ' ']
    if(alphabet.includes(key)){
        let inputContainer = document.querySelector(".inputContainer");
        inputContainer.innerHTML += key;
        if(key === ' '){
            space_pressed()
        } else {
            awaiting.push('encrypt');
            sendRequest('encrypt', null, key);
        }
        console.log("Key pressed: " + key);
    } else{
        console.log("Invalid key '"+key+"' pressed");
    }
}

function space_pressed(){
    let outputContainer = document.querySelector(".outputContainer");
    outputContainer.innerHTML += ' ';

    checkCharLimit();
}

function letter_received(response) {
    let letter = response[0]
    let rotors = response[1]
    console.log("Encrypted Letter Received: " + letter);
    let outputContainer = document.querySelector(".outputContainer");
    outputContainer.innerHTML += letter;
    $("[name^=l_]").css('background-color', 'white')
    $('[name="l_' + letter + '"]').css('background-color', 'yellow')

    document.getElementById('current_R1').innerText = rotors[0]
    document.getElementById('current_R2').innerText = rotors[1]
    document.getElementById('current_R3').innerText = rotors[2]

    checkCharLimit()
}


function checkCharLimit() {
    let inputContainer = document.querySelector(".inputContainer");
    let outputContainer = document.querySelector(".outputContainer");
    let inputLength = inputContainer.innerText.length
    let outputLength = outputContainer.innerText.length

    // if(inputLength !== outputLength){
    //     throw "Input and Output Container out of sync"
    // }
    if (inputLength > 140) {
        let input = inputContainer.innerHTML
        inputContainer.innerHTML = input.slice(input.length - 140, input.length)
        let output = outputContainer.innerHTML
        outputContainer.innerHTML = output.slice(output.length - 140, output.length)
    }
}