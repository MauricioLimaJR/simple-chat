var teste = function () {
	$.ajax({
        type: "GET",
        // url: '../../src/test',
        url: '../../TcpServerNew.py',
        // async: false,
        data: null, 
        success: function (data) {
        	console.log(data);
        },
        error: function (err) {
        	alert('deu erro');
        }
    });
}