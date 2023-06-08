var letters = []
var lastpressed = null

function plugboard_pressed(key) {
    for (let i = 0; i < letters.length; i++) {
        if (letters[i].includes(key)) {
            letters.splice(i, 1)
            const reg = new RegExp(".?" + key + ".?")
            const elements = [...document.getElementsByClassName('tuple')];
            for (let i in elements) {
                if (reg.test(elements[i].outerText)) {
                    awaiting.push('plugboard_set')
                    sendRequest('plugboard', 'set', elements[i].outerText.split(',')[0])
                    elements[i].remove()
                    $('[name="p_'+elements[i].outerText[0]+'"]').css('background-color', 'white')
                    $('[name="p_'+elements[i].outerText[1]+'"]').css('background-color', 'white')
                    return
                }
            }
            return
        }
    }
    if (checkPlugLimitReached()){
        alert("Only 10 Plugs are allowed")
        return
    }
    if (lastpressed == null) {
        lastpressed = key
        $('.plugboardContainer').append("<p id='lastpressed'></p>")
        $('#lastpressed').append(key)
        $('[name="p_'+key+'"]').css('background-color', 'LightCoral')
        return
    }
    if (lastpressed === key) {
        $('#lastpressed').remove()
        $('[name="p_'+key+'"]').css('background-color', 'white')
        lastpressed = null
        return
    }
    letters.push([key, lastpressed])
    awaiting.push('plugboard_set')
    sendRequest('plugboard', 'set', ''+key+lastpressed+'')
    $('.plugboardContainer').append("<p class='tuple' id='"+key+lastpressed+"'>"+lastpressed+key+',&nbsp;'+"</p>")
    $('#lastpressed').remove()
    $('[name="p_'+key+'"]').css('background-color', 'LightBlue')
    $('[name="p_'+lastpressed+'"]').css('background-color', 'LightBlue')
    lastpressed = null
}

function reset_plugboard() {
    lastpressed = null
    letters = []
    awaiting.push('plugboard_reset')
    sendRequest('plugboard', 'reset')
    $('.plugboardContainer').empty()
    $("[name^=p_]").css('background-color', 'white')
}

function checkPlugLimitReached(){
    let plugboardContainer = document.querySelector(".plugboardContainer");
    let contentLength = plugboardContainer.textContent.length

    if (contentLength%4 === 0) {
        let plugs = contentLength / 4
        if (plugs === 10){
            return true
        }
    }
    return false
}

function setPlugboard(){
 // TODO
}
