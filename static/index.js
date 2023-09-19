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
        console.log(event.target.result);
        return event.target.result
    }
}