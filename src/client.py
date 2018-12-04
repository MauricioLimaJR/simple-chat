import socket
import threading
import pickle
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import winsound
from random import randint


class Cliente():


    def __init__(self):

        # Interface

        # inicializando o objeto da tela
        root = Tk()
        # passando as medidas e configuração da tela
        root.geometry("640x480+325+100")
        root.title('Chat')
        #root.iconbitmap('C:/Users/User/Pictures/icone/favicon.ico')
        root.resizable(False, False)
        # root.setFixedSize(640, 480);
        root.configure(background='#707070')

        # criando o frame do topo
        Bot = Frame(root, width=640, height=98)
        Bot.pack(side=BOTTOM)
        Bot.configure(background='grey')

        # criando a frame esquerda
        Left = Frame(root, width=380, height=380)
        Left.pack(side=LEFT)
        Left.configure(background='#DCDCDC')

        # criando a frame direita

        Right = Frame(root, width=258, height=380)
        Right.pack(side=RIGHT)
        Right.configure(background='#3CB371')

        # inserindo label para titulo
        lblTitulo = Label(Right, font=('arial', 10, 'bold'), text='Inicie sua conexão')
        lblTitulo.place(x=62, y=0)
        lblIP = Label(Right, font=('arial', 10, 'bold'), text='Digite o IP do servidor:')
        lblIP.place(x=50, y=150)
        lblNome = Label(Right, font=('arial', 12, 'bold'), text='Digite seu nome:')
        lblNome.place(x=55, y=70)
        lblConexao = Label(Right, width=20, height=2, font=('arial', 8, 'bold'), text='Desconectado  :(')
        lblConexao.place(x=55, y=260)

        # inserindo campo Entry
        self.entrada_ip = Entry(Right, width=20)
        self.entrada_ip.place(x=60, y=180)
        self.entrada_nome = Entry(Right, width=20)
        self.entrada_nome.place(x=60, y=100)

        # inserindo botão
        btEnviar = Button(Bot, height=3, width=12, text='Enviar', command=self.bt_click_enviar,
                          font=('arial', 10, 'bold'))
        btEnviar.place(x=520, y=16)
        btConectar = Button(Right, height=1, width=7, text='Conectar', command=self.bt_click_conectar,
                            font=('arial', 10, 'bold'))
        btConectar.place(x=90, y=210)

        # inserindo campo de texto(Bot)
        self.text = Text(Bot, font=('arial', 10, 'bold'), height=4, width=65)
        self.text.place(x=30, y=10)

        # insetindo campo de texto com rolagem (Left)
        self.areaMensagens = ScrolledText(Left, height=21, width=40)
        self.areaMensagens.place(x=2, y=2)
        self.areaMensagens['font'] = ('arial', 12)

        # Interface


        # Conexão

        self.host = ' '
        self.user = ' '
        port = 3250
        while True:
            if self.host == ' ':
                root.update()
            else:
                break

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(self.host), int(port)))
        print('Conectado ao servidor: {} , Porta: {}'.format(self.host, str(port)))
        self.conexao = True
        lblConexao['text'] = 'Conectado :)'
        msg_recv = threading.Thread(target=self.msg_recv)
        msg_recv.daemon = True
        msg_recv.start()

        #Conexão

        # finalização da tela do sistema
        root.mainloop()




    def msg_recv(self):

        while True:
            try:

                data = self.sock.recv(1024)
                data = pickle.loads(data)
                if data:
                    msg = self.decode(data[0], data[1])
                    self.areaMensagens.insert(END, msg)
                    winsound.PlaySound('C:/music/notif.wav', winsound.SND_FILENAME)
            except Exception:
                pass




    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))

    def bt_click_enviar(self):
        msg = self.text.get(1.0, END)
        msgUser = self.user+" falou: "+msg
        self.areaMensagens.insert(END, "Você falou: "+msg)
        self.send_msg(self.encode(msgUser))
        self.text.delete(1.0, END)

    def bt_click_conectar(self):
        self.host = self.entrada_ip.get()
        self.entrada_ip.delete(0, 'end')
        self.user = self.entrada_nome.get()
        self.entrada_nome.delete(0, 'end')


    def encode(self,text):
        seed = randint(3, 5)
        keys = [randint(1, 9) * 1 for x in range(seed)]

        for key in keys:
            text = [chr(ord(l) + key) for l in text]

        return [text, keys]

    def decode(self, text, keys):
        decrypt_str = ''
        keys.reverse()

        for key in keys:
            for l in text:
                decrypt_str += chr(ord(l) - key)
            text = decrypt_str
            decrypt_str = ''

        return text



c = Cliente()
