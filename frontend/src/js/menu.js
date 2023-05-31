function showMenu(){
    awaiting.push('getSetting')
    sendRequest('dump')
    remove_keydown_listener()
}

function hideMenu(){
    document.getElementById('menu').close()
    document.addEventListener("keydown", key_event)
}

function currentSet(rotor_setting, offsets){
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

    let mapped_off_r1 = alphabet.charAt(off_r1)
    let mapped_off_r2 = alphabet.charAt(off_r2)
    let mapped_off_r3 = alphabet.charAt(off_r3)

    document.getElementById('offset_r1').value = mapped_off_r1
    document.getElementById('offset_r2').value = mapped_off_r2
    document.getElementById('offset_r3').value = mapped_off_r3

    setvariants(rotors.length)
}

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


    let offset_r1 =     $('input[id=offset_r1]').val()
    let offset_r2 =    $('input[id=offset_r2]').val()
    let offset_r3 =     $('input[id=offset_r3]').val()

    if(document.getElementById('menu_row3').hidden === true){
        awaiting.push("rotors:offset")
        sendRequest("rotors", "offset", offset_r1+offset_r2)
    } else {
        awaiting.push("rotors:offset")
        sendRequest("rotors", "offset", offset_r1+offset_r2+offset_r3)
    }

    document.getElementById('menu').close()
    document.addEventListener("keydown", key_event)
}

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
            $('tr[id="menu_row3"]').prop('hidden', true)

            $('[value="Reflector A"]').prop('disabled', true)
            $('[value="Reflector B"]').prop('disabled', false)
            $('[value="Reflector C"]').prop('disabled', true)

            $('option[value^="Enigma B-"]').prop('disabled', false)
            $('option[value^="Enigma I-"]').prop('disabled', true)
            $('option[value^="Enigma M3-"]').prop('disabled', true)
            break
        }

        case "1":{
            $('tr[id="menu_row3"]').prop('hidden', false)

            $('[value="Reflector A"]').prop('disabled', false)
            $('[value="Reflector B"]').prop('disabled', false)
            $('[value="Reflector C"]').prop('disabled', false)

            $('option[value^="Enigma B-"]').prop('disabled', true)
            $('option[value^="Enigma I-"]').prop('disabled', false)
            $('option[value^="Enigma M3-"]').prop('disabled', true)
            break
        }

        case "M3":{
            $('tr[id="menu_row3"]').prop('hidden', false)

            $('[value="Reflector A"]').prop('disabled', true)
            $('[value="Reflector B"]').prop('disabled', false)
            $('[value="Reflector C"]').prop('disabled', false)

            $('option[value^="Enigma B-"]').prop('disabled', true)
            $('option[value^="Enigma I-"]').prop('disabled', true)
            $('option[value^="Enigma M3-"]').prop('disabled', false)
            break
        }

        case "All":{
            $('tr[id="menu_row3"]').prop('hidden', false)
            $('[value^=Reflector]').prop('disabled', false)
            $('option[value^=Enigma]').prop('disabled', false)
            break
        }

    }
}