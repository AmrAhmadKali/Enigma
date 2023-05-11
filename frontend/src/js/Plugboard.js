var letters = []
var lastpressed = null
function plugboard_pressed(key) {

    if (lastpressed == null) {
        lastpressed = key
        return

    }
    if (lastpressed == key) {
        lastpressed = null
        return
    }

    for (let i = 0; i < letters.length; i++) {
        if (letters[i].includes(key)) {
            letters.splice(i, 1)
            return
        }

    }

    letters.push([key, lastpressed])
    //awaiting.push('plugboard_set')
    //sendRequest('plugboard', 'set', [key, lastpressed])
    lastpressed = null
    console.log("Plugboardeinstellung"+ letters)
}

function reset_plugboard() {
    lastpressed = null
    letters = null
    //awaiting.push('plugboard_reset')
    //sendRequest('plugboard', 'reset')

}

