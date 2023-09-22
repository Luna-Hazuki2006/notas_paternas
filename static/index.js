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
    let actual = document.getElementById('categorias')
    let numero = document.getElementById('puntaje')
    let valor = actual.options[actual.selectedIndex].value
    let texto = actual.options[actual.selectedIndex].text
    let madre = numero.parentElement
    let muchos = madre.getElementsByTagName('div').length
    let div = document.createElement('div')
    let label = document.createElement('label')
    label.innerText = 'Categoría ' + (muchos + 1) + ': '
    div.appendChild(label)
    let input = document.createElement('input')
    input.type = 'text'
    input.id = valor
    input.name = valor
    input.setAttribute('value', texto)
    input.setAttribute('readonly', '')
    div.appendChild(input)
    label = document.createElement('label')
    label.innerText = 'Puntaje ' + (muchos + 1) + ': '
    div.appendChild(label)
    input = document.createElement('input')
    input.type = 'number'
    input.id = 'puntaje' + valor
    input.name = 'puntaje' + valor
    input.setAttribute('value', numero.value)
    input.max = numero.max
    input.min = '1'
    input.setAttribute('readonly', '')
    div.appendChild(input)
    let boton = document.createElement('button')
    boton.setAttribute('type', 'button')
    boton.setAttribute('onclick', 'quitarSeccion(this);')
    boton.innerText = '-'
    div.appendChild(boton)
    div.classList.add('redondeado')
    madre.appendChild(div)
    let lista = actual.getElementsByTagName('option')
    for (let i = 0; i < lista.length; i++) {
        if (lista[i].value == valor) {
            actual.removeChild(lista[i])
            numero.value = 1
            break
        }
    }
    let agregar = document.getElementById('agregar')
    if (lista.length == 0) {
        agregar.setAttribute('disabled', 'disabled')
    } else {
        agregar.removeAttribute('disabled')
    }
    let total = document.getElementById('puntaje_total')
    total.value = Number(total.value) + Number(input.value)
}

function quitarSeccion(esto) {
    let madre = esto.parentElement
    // let madre = document.getElementById('madre')
    let abuela = madre.parentElement
    let inputs = madre.getElementsByTagName('input')
    let option = document.createElement('option')
    option.value = inputs[0].id
    option.text = inputs[0].value
    let actual = document.getElementById('categorias')
    actual.appendChild(option)
    abuela.removeChild(madre)
    let agregar = document.getElementById('agregar')
    let lista = actual.getElementsByTagName('option')
    if (lista.length == 0) {
        agregar.setAttribute('disabled', 'disabled')
    } else {
        agregar.removeAttribute('disabled')
    }
    let total = document.getElementById('puntaje_total')
    total.value = Number(total.value) - Number(inputs[1].value)
}

function verificarExamen() {
    let total = document.getElementById('puntaje_total')
    let boton = document.getElementById('guardar')
    if (total.value != 0) {
        boton.setAttribute('type', 'submit')
        Swal.fire({
            icon: 'info', 
            title: 'Información mandada', 
            text: 'Se ha mandado la información'
        })
    } else {
        boton.setAttribute('type', 'button')
        Swal.fire({
            icon: 'error', 
            title: 'Datos incompletos', 
            text: 'Tiene que haber mínimo una categoría guardada'
        })
    }
}

function modificarPuntaje() {
    let actual = document.getElementById('categorias')
    let numero = document.getElementById('puntaje')
    let valor = actual.options[actual.selectedIndex].value
    for (const este of todos) {
        if (este['id'] == valor) {
            numero.max = este['puntaje']
            numero.value = 1
            break
        }
    }
}