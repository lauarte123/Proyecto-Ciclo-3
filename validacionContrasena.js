function validar_formulario(){
    var usuario = document.formulario.usuario;
    var correo = document.formulario.correo;
    var clave = document.formulario.password;
    
    var usuario_len=usuario.value.length;

    //if(usuario_len == 0 || usuario_len<8){
        //alert("Debes ingresar un usuario con mínimo 8 caracteres");
        //return false;
    //}

    var clave_len = clave.value.length;

    if(clave_len == 0 || clave_len<8){
        alert("Debes ingresar una clave con más de 8 caracteres");
        return false;
    }
    formato de correo electrónico
    var formatoCorreo = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    si no es verdadero !correo.
    if(!correo.value.match(formatoCorreo)){
        alert("Debes ingresar un correo electrónico válido");
        return false;
    }


}