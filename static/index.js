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