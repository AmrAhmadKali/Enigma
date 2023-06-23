/**
 * Deletes the cookie with the name 'CC_uuid' if it exists.
 */
function deleteCookie(){
    document.cookie = "CC_uuid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

/**
 * Sets a cookie with the name 'CC_uuid' and the specified UUID.
 * This UUID should be the identifier for a saved Enigma State at the backend.
 * @param uuid - The value of the cookie
 */
function setCookie(uuid) {
    const d = new Date()
    d.setTime(d.getTime() + (7 * 24 * 60 * 60 * 1000))

    document.cookie = "CC_uuid="+ uuid + ";" + "expires=" + d.toUTCString() + "; path=/;"
}

/**
 * Returns the value of the cookie named 'CC_uuid' as a string.
 * This value is the UUID for a saved Enigma State at the backend.
 * @returns {string}
 */
function getCookie() {
    let cookieName = "CC_uuid="
    let cookie = decodeURIComponent(document.cookie)
    return cookie.split(';')[0].slice(cookieName.length, cookie.length)
}

/**
 * Determines whether cookie with the name 'CC_uuid' is set.
 * @returns {boolean}
 */
function isCookieSaved(){
    return decodeURIComponent(document.cookie).includes("CC_uuid=")
}


