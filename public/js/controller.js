var teste = function () {
	$.ajax({
        type: "GET",
        // url: '../../src/test',
        url: 'src/test.py',
        // async: false,
        data: {data: 'mauricio'},
        success: function (data) {
        	alert(data);
        },
        error: function (err) {
        	alert(err);
        }
    });
}