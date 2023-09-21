function mostrar_mensaje(texto) {
    Swal.fire({
        icon: 'question', 
        title: 'Un muy bonito título', 
        text: texto
    })
}

function mostrar_escrito(texto) {
    texto = JSON.parse(texto)
    console.log('Aquí viene texto de prueba');
    console.log(texto);
}

function mostrar_imagen() {
    var input = document.getElementById("imagen");
    var fReader = new FileReader();
    fReader.readAsDataURL(input.files[0]);
    fReader.onloadend = function(event) {
        var img = document.getElementById("vistas");
        img.value = event.target.result;
        img = document.getElementById('externa')
        img.src = event.target.result
        console.log(event.target.result);
        return event.target.result
    }
}

function deimaginar() {
    let imagen = document.getElementById('imagen')
    let externa = document.getElementById('externa')
    let vistas = document.getElementById('vistas')
    imagen.value = ''
    externa.src = ''
    vistas.value = ''
}

function agregarSeccion() {
}

function verificarExamen() {
    let total = document.getElementById('puntaje_total')
    let boton = document.getElementById('guardar')
    if (total.value != 0) {
        boton.setAttribute('type', 'submit')
    } else {
        boton.setAttribute('type', 'button')
    }
}