function listener_init() {
    document.addEventListener("keydown", function(){key_pressed(event.key)});

    loadCookie();

    document.getElementById('showMenuBtn').addEventListener('click', () => {
        document.getElementById('menu').showModal()
    });

    document.getElementById('resetBtn').addEventListener('click', function(){deleteCookie(); window.location.reload()});
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

function letter_received(letter){
    console.log("Encrypted Letter Received: " + letter);
    let outputContainer = document.querySelector(".outputContainer");
    outputContainer.innerHTML += letter;
    $("[name^=l_]").css('background-color', 'white')
    $('[name="l_'+letter+'"]').css('background-color', 'yellow')
    checkCharLimit()
    changeCookie()
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

function generateUUID() {
    let chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let uuid = '';
    for(let i = 0; i < 20; i++) {
        uuid += chars[Math.floor(Math.random() * chars.length)];
    }
    return uuid;
}

function changeCookie(){
    let settings = getCookie();
    if (settings.length !== 0) {
        deleteCookie();
        setCookie(settings[0]);
    }else{
        let uuid = generateUUID();
        setCookie(uuid);
    }
}

function deleteCookie(){
    document.cookie = "enigma_settings=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

function setCookie(uuid) {
    let input = document.querySelector(".inputContainer");
    let cypher = document.querySelector(".outputContainer");
    const d = new Date();
    d.setTime(d.getTime() + (7 * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    let cookie_value = "UUID=" + uuid + ":input=" + input.innerHTML + ":cypher=" + cypher.innerHTML;
    document.cookie = "enigma_settings"+ "=" + cookie_value + ";" + expires + ";path=/";
}

function getCookie() {
  let settings = "enigma_settings=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(settings) === 0) {
      return c.substring(settings.length, c.length).split(":").map(function (x){return x.slice(x.indexOf("=") + 1)});
    }
  }
  return [];
}

function loadCookie(){
    let settings = getCookie();
    if (settings.length !== 0){
        let inputContainer = document.querySelector(".inputContainer");
        let outputContainer = document.querySelector(".outputContainer");

        inputContainer.innerHTML = settings[1];
        outputContainer.innerHTML = settings[2];
    }
}