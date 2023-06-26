/**
 * a global array of the currently set plugs.
 * @type {string[]}
 */
let plugs = [];
/**
 * a global variable containing the key on the plugboard that has been pressed the last.
 * @type {any}
 * @default null
 */
let lastpressed = null;

/**
 * Handles the plugboard pressed event by sending the commands to the backend,
 *  coloring the plugboard
 *  and filling or deleting the chars in the plugboard container.
 * @param key - The key that has been pressed on the plugboard
 */
function plugboard_pressed(key) {
    for (let i = 0; i < plugs.length; i++) {
        if (plugs[i].includes(key)) {
            plugs.splice(i, 1)
            const RE = RegExp
            const reg = new RE(`.?${key}.?`)
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
    plugs.push([key, lastpressed])
    awaiting.push('plugboard_set')
    sendRequest('plugboard', 'set', ''+key+lastpressed+'')
    $('.plugboardContainer').append("<p class='tuple' id='"+key+lastpressed+"'>"+lastpressed+key+',&nbsp;'+"</p>")
    $('#lastpressed').remove()
    $('[name="p_'+key+'"]').css('background-color', 'LightBlue')
    $('[name="p_'+lastpressed+'"]').css('background-color', 'LightBlue')
    lastpressed = null
}

/**
 * Resets the plugboard by clearing the plugs and lastpressed variables, sending a reset command to the server and
 * emptying the Plugboard and Container.
 */
function reset_plugboard() {
    lastpressed = null
    plugs = []
    awaiting.push('plugboard_reset')
    sendRequest('plugboard', 'reset')
    $('.plugboardContainer').empty()
    $("[name^=p_]").css('background-color', 'white')
}

/**
 * Counts the currently set plugs and returns true if it is 10. Otherwise, returns false.
 * @returns {boolean}
 */
function checkPlugLimitReached(){
    let plugboardContainer = document.querySelector(".plugboardContainer");
    let contentLength = plugboardContainer.textContent.length

    if (contentLength%4 === 0) {
        let plug_count = contentLength / 4
        if (plug_count === 10){
            return true
        }
    }
    return false
}

/**
 * Sets the plug board according to the saved data in the backend.
 * Only to be called by the getSaveData response Handler.
 * @param setting - Dictionary with the plug mapping
 */
function setPlugboard(setting){
    let tmp = null
    for(let i in setting){
        if(tmp){
            $('[name="p_'+i+'"]').css('background-color', 'LightBlue')
            $('[name="p_'+tmp+'"]').css('background-color', 'LightBlue')
            $('.plugboardContainer').append("<p class='tuple' id='"+i+tmp+"'>"+i+tmp+',&nbsp;'+"</p>")
            plugs.push(i+tmp)
            tmp = null
        } else {
            tmp = i
        }
    }
}
