function mostrar_mensaje(texto) {
    Swal.fire({
        icon: 'error', 
        title: 'Un muy bonito título', 
        text: texto
    })
}

function mostrar_escrito(texto) {
    console.log('Aquí viene texto de prueba');
    console.log(texto);
}