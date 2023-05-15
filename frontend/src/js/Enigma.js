function listener_init() {
    document.addEventListener("keydown", function(){key_pressed(event.key)});
}

function key_pressed(key){
    key = key.toUpperCase()
    const alphabet = ['Q','W','E','R','T','Z','U','I','O','P','L','K','J','H','G','F','D','S','A','Y','X','C','V','B','N','M', ' ']
    if(alphabet.includes(key)){
        let inputContainer = document.querySelector(".inputContainer");
        inputContainer.innerHTML += key;
        awaiting.push('encrypt');
        sendRequest('encrypt', null, key);
        console.log("Key pressed: " + key);
    }
    else{
        console.log("Invalid key '"+key+"' pressed");
    }
}

function letter_received(letter){
    console.log("Encrypted Letter Received: " + letter);
    let outputContainer = document.querySelector(".outputContainer");
    if (outputContainer.innerHTML.length % 5 === 0){
        outputContainer.innerHTML += ' ';
    }
    outputContainer.innerHTML += letter;
    //TODO: Lamp panel change letter state
}

function openwindow(){
    const newwindow = window.open("Konfiguration.html", "Konfiguration");
    newwindow.focus()
}