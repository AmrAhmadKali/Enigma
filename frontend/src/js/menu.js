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
    
    changevalue('ring_r1', keyrings[rotors[2]], true)
    changevalue('ring_r2', keyrings[rotors[1]], true)
    changevalue('ring_r3', keyrings[rotors[0]], true)

    // TODO call still necessary?
    setvariants(rotors.length)
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

    document.getElementById('menu').close()
    clearContainer()
    document.addEventListener("keydown", key_event)
}

/**
 * Disables all menu options not available for the chosen variant.
 * Only to be called after a variant has been chosen.
 * @param rotor_count - TODO: nötig?
 */
function setvariants(rotor_count = null){
    const variant = document.getElementById("variants").value

    if(rotor_count === null){
        document.getElementById("reflector").value = "default"
        document.getElementById("r1").value = "default"
        document.getElementById("r2").value = "default"
        document.getElementById("r3").value = "default"
    }

    switch(variant){
        case "B":{
            //$('tr[id="menu_row3"]').prop('hidden', true)

            $('[value="Reflector A"]').prop('disabled', true)
            $('[value="Reflector B"]').prop('disabled', true)
            $('[value="Reflector C"]').prop('disabled', true)
            $('[value="Reflector UKW"]').prop('disabled', false)


            $('option[value^="Enigma B-"]').prop('disabled', false)
            $('option[value^="Enigma I-"]').prop('disabled', true)
            $('option[value^="Enigma M3-"]').prop('disabled', true)
            break
        }

        case "1":{
            //$('tr[id="menu_row3"]').prop('hidden', false)

            $('[value="Reflector A"]').prop('disabled', false)
            $('[value="Reflector B"]').prop('disabled', false)
            $('[value="Reflector C"]').prop('disabled', false)
            $('[value="Reflector UKW"]').prop('disabled', true)


            $('option[value^="Enigma B-"]').prop('disabled', true)
            $('option[value^="Enigma I-"]').prop('disabled', false)
            $('option[value^="Enigma M3-"]').prop('disabled', true)
            break
        }

        case "M3":{
           //$('tr[id="menu_row3"]').prop('hidden', false)

            $('[value="Reflector A"]').prop('disabled', true)
            $('[value="Reflector B"]').prop('disabled', false)
            $('[value="Reflector C"]').prop('disabled', false)
            $('[value="Reflector UKW"]').prop('disabled', true)


            $('option[value^="Enigma B-"]').prop('disabled', true)
            $('option[value^="Enigma I-"]').prop('disabled', true)
            $('option[value^="Enigma M3-"]').prop('disabled', false)
            break
        }

        case "All":{
            //$('tr[id="menu_row3"]').prop('hidden', false)
            $('[value^=Reflector]').prop('disabled', false)
            $('option[value^=Enigma]').prop('disabled', false)
            break
        }

    }
}

/**
 * TODO
 * @param inputid
 * @param change
 * @param reset
 */
function changevalue(inputid, change, reset = false) {
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