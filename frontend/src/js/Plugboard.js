var letters = []
var lastpressed = null
function plugboard_pressed(key) {
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

    for (let i = 0; i < letters.length; i++) {
        if (letters[i].includes(key)) {
            letters.splice(i, 1)
            const reg = new RegExp(".?"+key+".?")
            // for(element in '.plugboardContainer'){
            //     exec(element)
            //         ...
            // }
            // $('.plugboardContainer').remove("."+...)
            // TODO: remove Abfrage
            return
        }
    }

    letters.push([key, lastpressed])
    //awaiting.push('plugboard_set')
    //sendRequest('plugboard', 'set', [key, lastpressed])
    $('.plugboardContainer').append("<div id='"+key+lastpressed+"'>"+key+lastpressed+"</div><br>")
    lastpressed = null
    $('#lastpressed').remove()
}

function reset_plugboard() {
    lastpressed = null
    letters = null
    //awaiting.push('plugboard_reset')
    //sendRequest('plugboard', 'reset')
    $('.plugboardContainer').empty()
}

