function initLocalStorage() {
    if(localStorage.length === 0 || !isCookieSaved()){
        localStorage.clear()
        localStorage.setItem("current", "1")
        localStorage.setItem("plugboard", "true")
        localStorage.setItem("1", "name,Enigma 1,reflectors,Reflector A,Reflector B,Reflector C,rotors,Enigma I-R1,Enigma I-R2,Enigma I-R3,Enigma I-R4,Enigma I-R5,plugboard,true")
        localStorage.setItem("2", "name,Enigma B,reflectors,Reflector UKW,rotors,Enigma B-R1,Enigma B-R2,Enigma B-R3,plugboard,false")
        localStorage.setItem("3", "name,Enigma M3,reflectors,Reflector B,Reflector C,rotors,Enigma M3-R1,Enigma M3-R2,Enigma M3-R3,Enigma M3-R4,Enigma M3-R5,Enigma M3-R6,Enigma M3-R7,Enigma M3-R8,plugboard,true")
    } else {
        // hide or show plugboard according to localStorage
        if(localStorage.getItem("plugboard")==="true"){
            document.getElementById('plugboard-row').hidden = false
            $('input[id="deactivate_plugboard"]').prop('disabled', true)
        } else {
            document.getElementById('plugboard-row').hidden = true
            $('input[id="deactivate_plugboard"]').prop('disabled', true)
        }
    }
}


function getCurrentVariant(){
    let variantNbr =  localStorage.getItem("current")
    let variant = localStorage.getItem(variantNbr).split(',')
    return variant[1]
}


function showVariantMenu() {
    remove_keydown_listener()
    document.getElementById('variantMenu').showModal()
    $('#variantReflectors option').prop('disabled', false)
    $('#variantRotors option').prop('disabled', false)
}

function hideVariantMenu(){
    document.getElementById('variantMenu').close()
    document.addEventListener("keydown", key_event)
}

function submitVariantMenu(){
    let name = document.getElementById("variantName").value
    let plugboard = document.getElementById("variantPlugboard").checked
    let reflectors = $("#variantReflectors").val().toLocaleString()
    let rotors = $("#variantRotors").val().toLocaleString()

    let variant = "name,"+name+",reflectors," +reflectors+",rotors,"+rotors+",plugboard,"+plugboard

    appendToLocalStorage(variant)
    hideVariantMenu()
}

function appendToLocalStorage(variant){
    let savedVariants = localStorage.length - 2
    let VariantNbr = savedVariants + 1

    localStorage.setItem(String(VariantNbr), String(variant))
}

function loadVariantsToMenu(){
    // delete all
    document.getElementById('variants').options.length = 0

    // add saved
    let i = 1
    while(localStorage.getItem(String(i))){
        let variant = localStorage.getItem(String(i)).split(',')
        let name = variant[1]

        let opt = document.createElement('option')
        opt.value = name
        opt.innerHTML = opt.value
        document.getElementById('variants').add(opt)
        i++
    }
}