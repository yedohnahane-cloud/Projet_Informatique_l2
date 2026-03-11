'use strict'

document.addEventListener('DOMContentLoaded', DCL_callback);

function DCL_callback (event){
    let SigninBtn = document.querySelector("SignIn");
    let mail;
    let password;
    let title = document.getElementById("titre");

SigninBtn.addEventListener("click", () => {
    window.location.href = "SignIn.html";
})

mail.addEventListener("submit", () => {
    mail  = document.getElementById("mail").value;
    title.innerText = mail;
})

password.addEventListener("submit", () => {
    password  = document.getElementById("password").value;
    title.innerText = password;
})

}