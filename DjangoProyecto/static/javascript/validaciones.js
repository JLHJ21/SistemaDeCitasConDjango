// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})()

//PERMITE GUION (-) Y PISO (_)
function SoloLetrasYNumerosYGuiones(e) {
    var key = e.keyCode || e.which;
    var teclado = String.fromCharCode(key).toLowerCase();
    //Expresion Regular Letras con Espacio
    //var ExpRegLetrasEspacio = "^[ a-zA-ZñÑáéíóúÁÉÍÓÚ]+$";
    //var ExpRegNomUsuario1 = /^[a-z0-9_-]{1,30}$/;

    var ExpRegNomUsuario = "^[ a-z0-9_-zA-ZÀ-ÿ-\u00f1\u00d1]+$";

    //Evaluación de Cadena Valida de Letras con Espacio 
    if (teclado.match(ExpRegNomUsuario) != null) {
        console.log("Letras con Espacio Válido");
    } else {
        alert("Sin carácteres especiales");
        return false;
    }
}

function SoloLetras(e) {
    var key = e.keyCode || e.which;
    var teclado = String.fromCharCode(key).toLowerCase();
    //Expresion Regular Letras con Espacio
    var ExpRegNomUsuario = "^[ a-zA-ZÀ-ÿ\u00f1\u00d1]+$";

    //Evaluación de Cadena Valida de Letras con Espacio 
    if (teclado.match(ExpRegNomUsuario) != null) {
        console.log("Letra");
    } else {
        alert("Solo letras");
        return false;
    }
}

function SoloNumeros(e) {
    var key = e.keyCode || e.which;
    var teclado = String.fromCharCode(key).toLowerCase();
    //Expresion Regular Letras con Espacio
    var ExpRegNomUsuario = "^[0-9,.]+$";

    //Evaluación de Cadena Valida de Letras con Espacio 
    if (teclado.match(ExpRegNomUsuario) != null) {
        console.log("Número");
    } else {
        alert("Solo números");
        return false;
    }
}



function SoloLetrasYNumeros(e) {
    var key = e.keyCode || e.which;
    var teclado = String.fromCharCode(key).toLowerCase();
    //Expresion Regular Letras con Espacio
    var ExpRegNomUsuario = "^[ a-z0-9zA-ZÀ-ÿ\u00f1\u00d1]+$";

    //Evaluación de Cadena Valida de Letras con Espacio 
    if (teclado.match(ExpRegNomUsuario) != null) {
        console.log("Número o letra");
    } else {
        alert("Solo números y letras");
        return false;
    }
}

//PERMITE EL ARROBA EL PISO, GUION, PUNTOS Y COMAS
function SoloCorreo(e) {
    var key = e.keyCode || e.which;
    var teclado = String.fromCharCode(key).toLowerCase();

    //Expresión Regular Email
    var ExpRegNomUsuario = "^[ a-z0-9_-zA-ZÀ-ÿ-@.,\u00f1\u00d1]+$";

    //Evaluación de Cadena Valida de Email 
    if (teclado.match(ExpRegNomUsuario) != null) {
        console.log("good");
    } else {
        alert("Solo (@), (.) como carácteres especiales");
        return false;
    }
}


//no funciona
function Texto(e) {
    var key = e.keyCode || e.which;
    var teclado = String.fromCharCode(key).toLowerCase();

    //Expresión Regular Email
    var ExpRegNomUsuario = /^[^$%&|<>#]*$/;

    //Evaluación de Cadena Valida de Email 
    if (ExpRegNomUsuario.test(e.target.value)) {
        console.log("good");
    } else {
        alert("No se permiten carácteres especiales");
        return false;
    }
}