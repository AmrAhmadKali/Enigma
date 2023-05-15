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
                    sendRequest('plugboard', 'set', elements[i].outerText)
                    elements[i].remove()
                    return
                }
            }
            return
        }
    }
    if (lastpressed == null) {
        lastpressed = key
        $('.plugboardContainer').append("<p id='lastpressed'></p>")
        $('#lastpressed').append(key)
        return
    }
    if (lastpressed === key) {
        lastpressed = null
        $('#lastpressed').remove()
        return
    }
    letters.push([key, lastpressed])
    awaiting.push('plugboard_set')
    sendRequest('plugboard', 'set', ''+key+lastpressed+'')
    $('.plugboardContainer').append("<p class='tuple' id='"+key+lastpressed+"'>"+lastpressed+key+"</p><p>,&nbsp;</p>")
    lastpressed = null
    $('#lastpressed').remove()
}

function reset_plugboard() {
    lastpressed = null
    letters = []
    awaiting.push('plugboard_reset')
    sendRequest('plugboard', 'reset')
    $('.plugboardContainer').empty()
}
