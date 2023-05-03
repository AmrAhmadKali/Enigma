function clear_inputContainer() {
    let inputContainer = document.querySelector(".inputContainer");
    inputContainer.value = null;
}

function key_pressed(key){
    key = key.toUpperCase()
    const alphabet = ['Q','W','E','R','T','Z','U','I','O','P','L','K','J','H','G','F','D','S','A','Y','X','C','V','B','N','M']
    if(alphabet.includes(key)){
        let inputContainer = document.querySelector(".inputContainer");
        inputContainer.value = inputContainer.value + key;
        awaiting.push('encrypt');
        sendRequest('encrypt', null, key);
        console.log("Key pressed: " + key);
    }
}

function letter_received(letter){
    console.log("Ecrypted Letter Received: " + letter);
    let outputContainer = document.querySelector(".outputContainer");
    outputContainer.innerText += letter;
    //TODO: Lamp panel change letter state
}

function openwindow(){
    const newwindow = window.open("Konfiguration.html", "Konfiguration");
    newwindow.focus()
}