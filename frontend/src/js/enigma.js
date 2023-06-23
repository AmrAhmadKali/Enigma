/**
 * This variable contains the function call of key_pressed with the event specific key.
 * To be used as listener for the keydown event.
 */
const key_event = function () {
    key_pressed(event.key)
};

/**
 * Global flag to differentiate between a normal reload and one triggered by the reset button.
 * To be set true if reload is clicked. Value is evaluated in the beforeunload event.
 * @type {boolean}
 * @default - false
 */
let reset_clicked = false;

/**
 * Initiates all event listeners for the Enigma. Called on body load.
 */
function listener_init() {
    document.addEventListener("keydown", key_event);

    $(window).bind('beforeunload', function(){
        if(reset_clicked===false){
            save().then(uuid => {
                setCookie(uuid)
            })
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

/**
 * Disconnects the website with the save data in the backend by deleting the cookie and reloading without a save() call.
 * To be called in the reset button clicked event.
 */
function reset() {
    reset_clicked = true
    deleteCookie()
    localStorage.clear()
    window.location.reload()
}

/**
 * Removes the keydown event. Used to disable input to the keyboard while a menu window is opened.
 */
function remove_keydown_listener(){
    document.removeEventListener("keydown", key_event);
}

/**
 * Send the save command to the backend and promises to return the UUID.
 * Throws an error if the answer of the backend is not received within the timeout.
 * @param timeout - default value 10000 milliseconds
 * @returns {Promise<string>} - a promise to deliver the UUID
 * @throws Error
 */
function save(timeout = 10000){
    return new Promise((resolve, reject) => {
        let timer;

        awaiting.push('save');
        sendRequest('save');

        /**
         * A function with local scope which is called when the websocket receives an answer.
         * Resolves the promise and clears the timeout.
         * @param message - The promised UUID as string
         */
        function responseHandler(message) {
            awaiting.pop()
            resolve(JSON.parse(message.data).response);
            clearTimeout(timer);
        }

        socket.onmessage = responseHandler;

        // set a timer for the timeout and reject the promise if it runs out
        timer = setTimeout(() => {
            reject(new Error("timeout waiting for save"));
            socket.onmessage = on_message
        }, timeout);
    });
}

/**
 * This function send a load command to the server if a cookie is set.
 * To be called after opening a websocket connection.
 */
function load(){
    if(isCookieSaved()){
        awaiting.push('load')
        sendRequest('load', null, getCookie())
    }
}

/**
 * Clears the input and output container and sets the lamp panel color to white.
 */
function clearContainer(){
    document.querySelector(".inputContainer").innerText = ''
    document.querySelector(".outputContainer").innerText = ''
    $("[name^=l_]").css('background-color', 'white')
    $("[name^=k_]").css('background-color', 'black')
}

/**
 * Makes an encrypt call to the server if the key is valid (A-Z and space), otherwise ignores it.
 * To be called when a physical or virtual key is pressed.
 * @param key - The key that has been pressed
 */
function key_pressed(key){
    key = key.toUpperCase()
    const alphabet = ['Q','W','E','R','T','Z','U','I','O','P','L','K','J','H','G','F','D','S','A','Y','X','C','V','B','N','M', ' ']
    if(alphabet.includes(key)){
        let inputContainer = document.querySelector(".inputContainer");
        inputContainer.innerHTML += key;
        if(key === ' '){
            space_pressed()
        } else {
            highlightKey(key);
            awaiting.push('encrypt');
            sendRequest('encrypt', null, key);
        }
        console.log("Key pressed: " + key);
    } else{
        console.log("Invalid key '"+key+"' pressed");
    }
}

function highlightKey(key) {
    $('[name^="k_"]').css('background-color', 'black')
    $('[name="k_' + key + '"]').css('background-color', 'green')
}

/**
 * Appends a whitespace to the output Container, as we don't send space to the backend for encryption.
 * Only to be called by key_pressed().
 */
function space_pressed(){
    let outputContainer = document.querySelector(".outputContainer");
    outputContainer.innerHTML += ' ';

    checkCharLimit();
}

/**
 * Handles the response of an encrypt message, by writing the encrypted letter into the output box
 * and setting the offset display. Only to be called by on_message().
 * @param response - Response of the server as a string
 */
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

/**
 * Checks if the text containers contain more than 140 chars, deletes the chars that are too many starting at index 0.
 * To be called after a character has been inserted into the outputContainer.
 */
function checkCharLimit() {
    let inputContainer = document.querySelector(".inputContainer");
    let outputContainer = document.querySelector(".outputContainer");
    let inputLength = inputContainer.innerText.length

    if (inputLength > 140) {
        let input = inputContainer.innerHTML
        inputContainer.innerHTML = input.slice(input.length - 140, input.length)
        let output = outputContainer.innerHTML
        outputContainer.innerHTML = output.slice(output.length - 140, output.length)
    }
}