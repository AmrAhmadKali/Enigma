let valuering_r1;
let valuering_r2;
let valuering_r3;


/**
 * Starts the process to open the menu by getting sending a request to get the current settings from the backend
 * and calling remove_keydown_listener()
 */
function showMenu(){
    awaiting.push('getSetting')
    sendRequest('dump')
    remove_keydown_listener()
}

/**
 * Closes the menu and adds the keydown listener.
 */
function hideMenu(){
    document.getElementById('menu').close()
    document.addEventListener("keydown", key_event)
}

/**
 * Sets the value of the menu fields according to the server answers.
 * Only to be called by the responseHandler of getSetting.
 * @param rotor_setting - The order and name of the rotors and the reflector
 * @param offsets - The offsets of the current rotors
 * @param keyrings - The current keyring setting
 */
function currentSet(rotor_setting, offsets, keyrings){
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    let reflector = rotor_setting[1].toString()
    let rotors = rotor_setting[0]
    let off_r1 = offsets[rotors[2]]
    let off_r2 = offsets[rotors[1]]
    let off_r3 = offsets[rotors[0]]

    document.getElementById('menu').showModal()

    loadVariantsToMenu()
    document.getElementById("variants").value = getCurrentVariant()

    for(let i= 1; i <= rotors.length; i++ ){
        document.getElementById('reflector').value = reflector
        document.getElementById('r'+i).value = rotors[rotors.length-i]
    }

    let mapped_off_r1 = alphabet.charAt(off_r1%26)
    let mapped_off_r2 = alphabet.charAt(off_r2%26)
    let mapped_off_r3 = alphabet.charAt(off_r3%26)

    document.getElementById('offset_r1').value = mapped_off_r1
    document.getElementById('offset_r2').value = mapped_off_r2
    document.getElementById('offset_r3').value = mapped_off_r3
    
    changeRingsetting('ring_r1', keyrings[rotors[2]], true)
    changeRingsetting('ring_r2', keyrings[rotors[1]], true)
    changeRingsetting('ring_r3', keyrings[rotors[0]], true)
}

/**
 * sets the offset display according to the server answer.
 * Only to be called by the responseHandler of getSaveData.
 * @param rotor_setting - The order and name of the rotors and the reflector
 * @param offsets - The offsets of the current rotors
 */
function setOffsetDisplay(rotor_setting, offsets){
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    let rotors = rotor_setting[0]

    let off_r1 = offsets[rotors[2]]
    let off_r2 = offsets[rotors[1]]
    let off_r3 = offsets[rotors[0]]

    let mapped_off_r1 = alphabet.charAt(off_r1%26)
    let mapped_off_r2 = alphabet.charAt(off_r2%26)
    let mapped_off_r3 = alphabet.charAt(off_r3%26)

    document.getElementById('current_R1').innerText = mapped_off_r1
    document.getElementById('current_R2').innerText = mapped_off_r2
    document.getElementById('current_R3').innerText = mapped_off_r3
}

/**
 * Reads the values of the menu form, sends the settings to the server and sets the offset display.
 */
function submitMenu(){
    let reflector = document.getElementById("reflector").value
    let r1 = document.getElementById("r1").value
    let r2 = document.getElementById("r2").value
    let r3 = document.getElementById("r3").value

    if(r1==='default'||r2==='default'||r3==='default'){
        alert("Please choose a value for each field!")
        return
    }

    let setup

    if(r3 === 'default'){
        setup = ""+reflector+' '+r1+' '+r2+""
    }
    else {
        setup = ""+reflector+' '+r1+' '+r2+' '+r3+""
    }

    awaiting.push("rotors:set")
    sendRequest("rotors", "set", setup)


    let offset_r1 = $('input[id=offset_r1]').val()
    let offset_r2 = $('input[id=offset_r2]').val()
    let offset_r3 = $('input[id=offset_r3]').val()

    awaiting.push("rotors:offset")
    sendRequest("rotors", "offset", offset_r1+offset_r2+offset_r3)

    document.getElementById('current_R1').innerText = offset_r1
    document.getElementById('current_R2').innerText = offset_r2
    document.getElementById('current_R3').innerText = offset_r3

    awaiting.push("rotors:ringoffset")
    sendRequest("rotors", "ringoffset", valuering_r1 + valuering_r2 + valuering_r3)

    if(!document.getElementById('deactivate_plugboard').checked){
        document.getElementById('plugboard-row').hidden = true
        awaiting.push('plugboard_reset')
        sendRequest('plugboard', 'reset')
    }
    else{
        document.getElementById('plugboard-row').hidden = false
    }

    document.getElementById('menu').close()
    clearContainer()
    document.addEventListener("keydown", key_event)
}

/**
 * Disables all menu options not available for the chosen variant.
 * Only to be called after a variant has been chosen.
 */
function setvariants(){
    const variant = document.getElementById("variants").value

    let i = 1
    while(localStorage.getItem(String(i))){
        let savedVariant = localStorage.getItem(String(i)).split(',')
        let name = savedVariant[1]
        if(name === variant){
            localStorage.setItem("current", String(i))
            hideVariantsInMenu(savedVariant)
            return
        }
        i++
    }
    alert("Error") //TODO

}

function hideVariantsInMenu(variant){
    let reflectorIndex
    let rotorIndex
    let plugboardIndex
    for(let i=0; i<variant.length; i++){
        if(variant[i]==="reflectors"){
            reflectorIndex = i
        }
        if(variant[i]==="rotors"){
            rotorIndex = i
        }
        if(variant[i]==="plugboard"){
            plugboardIndex = i
        }
    }

    document.getElementById("reflector").value = "default"
    document.getElementById("r1").value = "default"
    document.getElementById("r2").value = "default"
    document.getElementById("r3").value = "default"

    let reflectorArray = variant.slice(reflectorIndex+1,rotorIndex)
    let rotorArray = variant.slice(rotorIndex+1,plugboardIndex)

    if(variant[variant.length-1] === "true"){
        $('input[id="deactivate_plugboard"]').prop('checked', true)
        localStorage.setItem("plugboard", "true")
    } else {
        $('input[id="deactivate_plugboard"]').prop('checked', false)
        $('input[id="deactivate_plugboard"]').prop('disabled', true)
        localStorage.setItem("plugboard", "false")

    }

    $('option[value^="Reflector"]').prop('disabled', true)

    for(let i=0; i<reflectorArray.length; i++){
        $('option[value="'+reflectorArray[i]+'"').prop('disabled', false)
    }

    $('option[value^="Enigma I-R"]').prop('disabled', true)
    $('option[value^="Enigma B-R"]').prop('disabled', true)
    $('option[value^="Enigma M3-R"]').prop('disabled', true)

    for(let i=0; i<rotorArray.length; i++){
        $('option[value="'+rotorArray[i]+'"').prop('disabled', false)
    }

}

/**
 * Updates the ringsettings
 * @param inputid
 * @param change
 * @param reset
 */
function changeRingsetting(inputid, change, reset = false) {
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    var input = document.getElementById(inputid)
    var value = parseInt(input.value)
    if (reset) {
        value = change % 26

    }
    else {
        value = (value + change + 26) % 26
    }
    var letter = letters.charAt(value)
    var newValue = value.toString() + " " + letter
    input.innerHTML = newValue
    document.getElementById(inputid).value = newValue

    if (inputid === "ring_r1") {
        valuering_r1 = letter

    }
    if (inputid === "ring_r2") {
        valuering_r2 = letter
    }
    if (inputid === "ring_r3") {
        valuering_r3 = letter
    }
}