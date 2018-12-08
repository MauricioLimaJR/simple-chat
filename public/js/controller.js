var teste = function () {
	$.ajax({
        type: "GET",
        url: 'http://localhost:8000/teste',
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