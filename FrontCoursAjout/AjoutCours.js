'use strict';


const droparea = document.querySelector('.droparea');
const instruText = document.getElementById('instruct');
const button = document.getElementById('chercheur');
const input = document.getElementById('formfile');


button.addEventListener("click", ()=>{
    input.click();
})

droparea.addEventListener('dragover', (evnt) => {
    evnt.preventDefault();
    console.log("y'a un fichier qui flotte chef");
    droparea.classList.add('active');
    instruText.innerText = "relâcher pour télécharger";
})

droparea.addEventListener('dragover', (evnt) => {
    evnt.preventDefault();
    console.log("y'a plus rien chef");
    droparea.classList.remove('active');
    instruText.innerText = "Glissez et lâchez votre fichier";
})

droparea.addEventListener('drop', (evnt)=>{
    evnt.preventDefault();
    console.log("CA A ETE DROPP2 CHEF !")
    let file = evnt.dataTransfer.files[0];

    FileisInputed(file);
})

input.addEventListener('change', function(){
    console.log("l'event marche chef !");
    let file = this.files[0];
    console.log(file);

    if(file){
        FileisInputed(file);
    }
    else{
        console.log("Erreur ! Y'a pas de fichier chef !");
    }
    
})

function FileisInputed(file){
    let fileType = file.type;
    let accepted = ['application/pdf'];

    if(accepted.includes(fileType)){
        let fileReader = new FileReader();
        fileReader.readAsDataURL(file);

        fileReader.onload = () => {
            document.getElementById('icone').src = "./pdfLogo.png";
            instruText.innerText = file.name;
        }
    } else {
        alert("Ceci n'est pas un PDF");
    }
}



