var letters = []
var lastpressed = null
function plugboard_pressed(key) {
       for (let i = 0; i < letters.length; i++) {
        if (letters[i].includes(key)) {
            letters.splice(i, 1)
            const reg = new RegExp(".?" + key + ".?")
            const divs = [...document.getElementsByClassName('tuple')];
            for (let i in divs) {
                if (reg.test(divs[i].outerText)) {
                    awaiting.push('plugboard_set')
                    sendRequest('plugboard', 'set', divs[i].outerText)
                    divs[i].remove()
                    return
                }
            }
            return
        }
    }


    if (lastpressed == null) {
        lastpressed = key
        $('.plugboardContainer').append("<div id='lastpressed'></div><br>")
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
    $('.plugboardContainer').append("<div class='tuple' id='"+key+lastpressed+"'>"+key+lastpressed+"</div><br>")
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

