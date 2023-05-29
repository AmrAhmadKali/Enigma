var cookie = {

    generateUUID: function() {
        let chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let uuid = '';
        for(let i = 0; i < 20; i++) {
            uuid += chars[Math.floor(Math.random() * chars.length)];
        }
        return uuid;
    },

    changeCookie: function(){
        let settings = this.getCookie();
        if (settings.length !== 0) {
            this.deleteCookie();
            this.setCookie(settings[0]);
        }else{
            awaiting.push('uuid');
            sendRequest('uuid')
            //let uuid = this.generateUUID();
            //this.setCookie(uuid);
        }
    },

    deleteCookie: function(){
        document.cookie = "enigma_settings=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    },

    setCookie: function(uuid) {
        let input = document.querySelector(".inputContainer");
        let cypher = document.querySelector(".outputContainer");
        const d = new Date();
        d.setTime(d.getTime() + (7 * 24 * 60 * 60 * 1000));
        let expires = "expires="+d.toUTCString();
        let replaced_uuid = uuid.replace("=", "!");
        console.log(replaced_uuid);
        console.log("test");
        let cookie_value = "UUID=" + replaced_uuid + ":input=" + input.innerHTML + ":cypher=" + cypher.innerHTML;
        document.cookie = "enigma_settings"+ "=" + cookie_value + ";" + expires + ";path=/";
    },

    getCookie: function() {
        let settings = "enigma_settings=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(';');
        for(let i = 0; i <ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(settings) === 0) {
                let value_list = c.substring(settings.length, c.length).split(":").map(function (x){return x.slice(x.indexOf("=") + 1)});
                value_list[0] = value_list[0].replace("!", "=");
                return value_list
            }
        }
        return [];
    },

    loadCookie: function(){
        let settings = this.getCookie();
        if (settings.length !== 0){
            let inputContainer = document.querySelector(".inputContainer");
            let outputContainer = document.querySelector(".outputContainer");

            inputContainer.innerHTML = settings[1];
            outputContainer.innerHTML = settings[2];
        }
    }
}

