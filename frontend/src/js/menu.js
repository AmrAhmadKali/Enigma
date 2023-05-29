const menu = document.getElementById('menu');


// TODO: alles

function submitMenu(){
    return
}

function cancelMenu() {
    return
}
function setvariants(variant){
    var variant = document.getElementById("variants").value
    $('[value^=R]').prop('disabled', true)
    $('label[for=r]').prop('hidden', true)
    $('label[for=reflector]').prop('hidden', false)
    var selectedRotors = []
    switch(variant){
        case "B":{
            
            $('label[for=r1]').prop('hidden', false)
            $('label[for=r2]').prop('hidden', false)
            $('[value^=Reflector-B').prop('disabled', false)
            $('[value^=R-B-]').prop('disabled', false)
           
            break}
            
          

        case "1":{
            $('label[for=r1]').prop('hidden', false)
            $('label[for=r2]').prop('hidden', false)
            $('label[for=r3]').prop('hidden', false)
             $('[value^=UKW').prop('disabled', false)
             $('[value^=R-I-]').prop('disabled', false)
            break}

        case "M3":{
            $('label[for=r1]').prop('hidden', false)
            $('label[for=r2]').prop('hidden', false)
            $('label[for=r3]').prop('hidden', false)
            $('label[for=r4]').prop('hidden', false)
            $('label[for=r5]').prop('hidden', false)
            $('[value^=UKW-B]').prop('disabled', false)
            $('[value^=UKW-C]').prop('disabled', false)
            $('[value^=R-M3-]').prop('disabled', false)
            break}

        case "All":{
            $('label[for=r1]').prop('hidden', false)
            $('label[for=r2]').prop('hidden', false)
            $('label[for=r3]').prop('hidden', false)
            $('label[for=r4]').prop('hidden', false)
            $('label[for=r5]').prop('hidden', false)
            $('[value^=UKW').prop('disabled', false)
            $('[value^=Reflector-B').prop('disabled', false)
            $('[value^=R]').prop('disabled', false)
            break}


    }
}