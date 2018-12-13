var messages_size = 0;
var path = 'http://';
// var adress = null;
// browser adress
var adress = path + '172.16.79.8';
// smartphone adress
// var adress = path + '192.168.43.48';
var user_name = "anonymous";

function set_path (str) {
    adress = path + str;
    document.getElementById('send_btn').disabled = false;
    setInterval(get_messages, 1000);
}

function start () {
    var adress = document.getElementById("adress").value,
    name = document.getElementById("user_name").value,
    status = document.getElementById('status');
    
    if (name != null && name.length > 0) {
        if (adress != null && adress.length > 0) {
            user_name = name;
            set_path(adress);
            status.innerHTML = "conectado(a)";
            status.style.color = "#26fb26";
        }
        else {
            status.innerHTML = "Escreva um endereço válido.";
            status.style.color = "red";
        }
    }
    else {
        status.innerHTML = "Escreva um nome válido.";
        status.style.color = "red";
    }
}

var teste = function () {
	$.ajax({
        type: "GET",
        url: adress + ':8000/teste',
        crossDomain: true,
        dataType: 'text',
        async: false,
        success: function (data) {
        	console.log(data);
        },
        error: function (err) {
        	alert('deu erro');
            console.log(err);
        }
    });
}

// To send message
var send_message = function () {
    var text = document.getElementById('type_area').value;

    if (text != null && text.length >= 1) {
        text = user_name + " falou: " + text;
        document.getElementById('type_area').value = "";

        console.log("TEXTOOOOO: ", text);
        $.ajax({
            type: "GET",
            url: adress + ':8000/send_message',
            crossDomain: true,
            dataType: 'json',
            // async: false,
            data: {message: text},
            success: function (data) {
                console.log(data);
                console.log("AQUIIIIII: ", text);
                document.getElementById('type_area').innerHTML = '';
            },
            error: function (err) {
                console.log(err);
                console.log("AQUIIIIII: ", text);
                document.getElementById('type_area').innerHTML = '';
            }
        });
    }
}

// Get messages
var get_messages = function () {

    $.ajax({
        type: "GET",
        url: adress + ':8000/get_messages',
        crossDomain: true,
        dataType: 'json',
        // async: false,
        success: function (data) {
            if (data.length > messages_size) {
                messages_size = data.length
                show_messsages(data);
            }
        },
        error: function (err) {
            console.log('nothing');
        }
    });  
}

var show_messsages = function (str_arr) {
    var div = document.getElementById('show_messages');
    var label = document.createElement('label');
    var notif = document.getElementById('notif');

    for (x in str_arr) {
        console.log(str_arr[x]);
        label.innerHTML = str_arr[x];
        label.style.width = "100%";

        div.appendChild(label);
    }
    
    var name = str_arr[messages_size - 1];
    name = name.split(' ')[0];

    console.log(name);
    if(name != user_name) {
        notif.play();
    }
}


