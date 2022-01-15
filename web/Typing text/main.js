let target = document.querySelector("#dynamic");


function randomSrting(){
    let stringArr = ["Learn to HTML", "Learn to PYTHON", "Hello, HiHI"];
    let selectString = stringArr[Math.floor(Math.random() * stringArr.length)];
    let selStingArr = selectString.split("");

    return selStingArr;
}

function resetTyping(){
    target.textContent = "";
    dynamic(randomSrting());
}

function dynamic(randomArr){
    if(randomArr.length > 0){
        target.textContent += randomArr.shift();
        setTimeout(function(){
            dynamic(randomArr);
        }, 80);
    }else{
        setTimeout(resetTyping, 3000);
    }
}
dynamic(randomSrting());
function blink(){
    target.classList.toggle("active");
}
setInterval(blink, 500)