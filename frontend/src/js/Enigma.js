function key_pressed(key){
    let inputContainer = document.querySelector(".inputContainer");
    inputContainer.innerText += key;
    awaiting.push('encrypt');
    sendRequest('encrypt', null, key);
    console.log("Key pressed: " + key);
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