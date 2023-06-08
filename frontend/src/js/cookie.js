function deleteCookie(){
    document.cookie = "uuid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

function setCookie(uuid) {
    const d = new Date()
    d.setTime(d.getTime() + (7 * 24 * 60 * 60 * 1000))

    document.cookie = "uuid="+ uuid + ";" + "expires=" + d.toUTCString() + "; path=/;"
}

function getCookie() {
    let cookieName = "uuid="
    let cookie = decodeURIComponent(document.cookie)
    return cookie.split(';')[0].slice(cookieName.length, cookie.length)
}

function isCookieSaved(){
    return decodeURIComponent(document.cookie).length > 0
}


