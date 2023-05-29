function listener_init() {
    document.addEventListener("keydown", function(){key_pressed(event.key)});

    cookie.loadCookie();

    document.getElementById('showMenuBtn').addEventListener('click', () => {
        document.getElementById('menu').showModal()
    });

    document.getElementById('resetBtn').addEventListener('click', function(){cookie.deleteCookie(); window.location.reload()});
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

function letter_received(response){
    let letter = response[0]
    let rotors = response[1]
    console.log("Encrypted Letter Received: " + letter);
    let outputContainer = document.querySelector(".outputContainer");
    outputContainer.innerHTML += letter;
    $("[name^=l_]").css('background-color', 'white')
    $('[name="l_'+letter+'"]').css('background-color', 'yellow')

    document.getElementById('current_R1').innerText = rotors[0]
    document.getElementById('current_R2').innerText = rotors[1]
    document.getElementById('current_R3').innerText = rotors[2]
    document.getElementById('current_R4').innerText = rotors[3]
    document.getElementById('current_R5').innerText = rotors[4]

    checkCharLimit()
    cookie.changeCookie()
}


function checkCharLimit(){
    let inputContainer = document.querySelector(".inputContainer");
    let outputContainer = document.querySelector(".outputContainer");
    let inputLength = inputContainer.innerText.length
    let outputLength = outputContainer.innerText.length

    if(inputLength !== outputLength){
        throw "Input and Output Container out of sync"
    }
    if (inputLength > 140){
        inputContainer.innerHTML = inputContainer.innerHTML.slice(1, inputContainer.innerHTML.length)
        outputContainer.innerHTML = outputContainer.innerHTML.slice(1, outputContainer.innerHTML.length)
    }
}