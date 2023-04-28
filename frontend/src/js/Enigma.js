
let textContainer = document.querySelector(".textContainer");
let allKey = document.querySelectorAll(".key");
/**
deleteKey.addEventListener("click",function(){
    let textContainerContent = textContainer.innerText;
    if(textContainerContent.length == 0){
        return;
    }
    console.log(textContainerContent);
    let newContent = textContainerContent.slice(0,textContainerContent.length-1);
    textContainer.innerText = newContent;
})

enterKey.addEventListener("click",function(){
    let content = textContainer.innerText;
    let newContent = content+"\n";
    textContainer.innerText = newContent;
})

spaceKey.addEventListener("click",function(){
    let content = textContainer.innerText;
    let newContent = content+ '\u00A0';
    textContainer.innerText = newContent;
})
**/
for(let key of allKey){
    key.addEventListener("click",function(){
        textContainer.innerText += key.innerText;
    })
}

function keypressed(){
    let key = event.key;
    document.getElementById("key").innerHTML = key
    if (key == "W"){
        console.log("W")
    }
    if(key == "Q"){
        console.log("Q")

    }
}


function openwindow(){
    const newwindow = window.open("Konfiguration.html", "Konfiguration");
    newwindow.focus()
}