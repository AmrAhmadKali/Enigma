function showMenu(){
    awaiting.push('getSetting')
    sendRequest('dump')

}

function hideMenu(){
    document.getElementById('menu').close()
}

function currentSet(response){
    let reflector = response[1].toString()
    let rotors = response[0]
    document.getElementById('menu').showModal()

    for(let i= 1; i <= rotors.length; i++ ){
        document.getElementById('reflector').value = reflector
        document.getElementById('r'+i).value = rotors[i-1]
    }

    setvariants(rotors.length)
}

function submitMenu(){
    let reflector = document.getElementById("reflector").value
    let r1 = document.getElementById("r1").value
    let r2 = document.getElementById("r2").value
    let r3 = document.getElementById("r3").value

    let setup

    if(r3 === 'default'){
        setup = ""+reflector+' '+r1+' '+r2+""
    }
    else {
        setup = ""+reflector+' '+r1+' '+r2+' '+r3+""
    }

    awaiting.push("rotors:set")
    sendRequest("rotors", "set", setup)

    document.getElementById('menu').close()
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
            $('label[for=r1]').prop('hidden', false)
            $('label[for=r2]').prop('hidden', false)
            $('label[for=r3]').prop('hidden', true)

            $('[value="Reflector A"]').prop('disabled', true)
            $('[value="Reflector B"]').prop('disabled', false)
            $('[value="Reflector C"]').prop('disabled', true)

            $('option[value^="Enigma B-"]').prop('disabled', false)
            $('option[value^="Enigma I-"]').prop('disabled', true)
            $('option[value^="Enigma M3-"]').prop('disabled', true)
            break
        }

        case "1":{
            $('label[for=r1]').prop('hidden', false)
            $('label[for=r2]').prop('hidden', false)
            $('label[for=r3]').prop('hidden', false)

            $('[value="Reflector A"]').prop('disabled', false)
            $('[value="Reflector B"]').prop('disabled', false)
            $('[value="Reflector C"]').prop('disabled', false)

            $('option[value^="Enigma B-"]').prop('disabled', true)
            $('option[value^="Enigma I-"]').prop('disabled', false)
            $('option[value^="Enigma M3-"]').prop('disabled', true)
            break
        }

        case "M3":{
            $('label[for=r1]').prop('hidden', false)
            $('label[for=r2]').prop('hidden', false)
            $('label[for=r3]').prop('hidden', false)

            $('[value="Reflector A"]').prop('disabled', true)
            $('[value="Reflector B"]').prop('disabled', false)
            $('[value="Reflector C"]').prop('disabled', false)

            $('option[value^="Enigma B-"]').prop('disabled', true)
            $('option[value^="Enigma I-"]').prop('disabled', true)
            $('option[value^="Enigma M3-"]').prop('disabled', false)
            break
        }

        case "All":{
            $('label[for^=r]').prop('hidden', false)
            $('[value^=Reflector]').prop('disabled', false)
            $('option[value^=Enigma]').prop('disabled', false)
            break
        }

    }

    if (rotor_count !== null){
        document.getElementById("variants").value = "default"
        for(let i=1; i <= rotor_count; i++){
            $('label[for="r'+i+'"]').prop('hidden', false)
        }
    }
}