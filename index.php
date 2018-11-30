<!DOCTYPE html>
<html lang="pt-br">
<head>
	<meta charset="UTF-8">
	<link rel="stylesheet" type="text/css" href="public/bootstrap/css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="public/css/style.css">

	<title>Chat</title>
</head>
<body>
	<!-- Container -->
	<div class="jumbotron">
		<!-- Header -->
		<div class="title-div">
			CHAT
		</div>
		<!-- Chat and Configs -->
		<div class="middle-div">
			<div class="chat-field">
				<!-- <textarea name="chat-area"></textarea> -->
			</div>
			<div class="config-field">
				<div>
					<label>Inicie sua conexão</label>
				</div>
				<div>
					<label>Digite seu nome:</label>
					<input type="text" name="user-name">
				</div>
				<div>
					<label>Digite o IP do servidor:</label>
					<input type="number" name="server-ip">
				</div>
				<div>
					<button>Conectar</button>
				</div>
				<div>
					<label>Status</label>
				</div>
			</div>
		</div>
		<!-- Bottom -->
		<div class="bottom-div container-fluid">
			<br>
			<textarea name="message"></textarea>
			<button type="button" class="btn btn-default">Enviar</button>
		</div>
	</div>
</body>
</html>