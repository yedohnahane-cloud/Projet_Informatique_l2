'use strict'

document.addEventListener('DOMContentLoaded', DCL_callback);

function DCL_callback (event){
    let ToSigninBtn = document.getElementById("ToSigninBtn");
    let ToLoginBtn = document.getElementById("ToLoginBtn");
    let Image = document.getElementById("décor");
    let Login = document.getElementById("Login");
    let Signin = document.getElementById("Signin");
    let Perso = document.getElementById("Perso");

    function hide(element) {
        element.style.display = 'none';
    }

    function show(element) {
        element.style.display = '';
    }

    function PageLoginSignin(){

    hide(Signin);
    hide(Perso);

    ToLoginBtn.addEventListener('click', () => {
        hide(Signin);
        hide(Perso);
        show(Image);
        show(Login);
    });

    ToSigninBtn.addEventListener('click', () => {
        hide(Image);
        hide(Login);
        show(Signin);
        show(Perso);
    });

    }
        PageLoginSignin();
    }

    



