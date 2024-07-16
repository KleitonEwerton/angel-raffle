import smtplib
import random
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

FILE = 'pessoas.csv'
REMETENTE = 'remetente@email.com'
SENHA = 'senha'


def ler_arquivo_csv(nome_arquivo):
    with open(nome_arquivo, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        pessoas = [row for row in csv_reader]
    return pessoas


def sortear_anjos(pessoas):
    nomes = [p['nome'] for p in pessoas]
    random.shuffle(nomes)
    anjos = {}

    for i, nome in enumerate(nomes):
        anjo = nomes[(i + 1) % len(nomes)]
        anjos[nome] = anjo

    return anjos


pessoas = ler_arquivo_csv(FILE)

anjos = sortear_anjos(pessoas)


def criar_mensagens(pessoas, anjos):
    mensagens = {}
    formulario_url = "www.formulario.com"


    mensagem_base = """
        Olá {nome},

        Sou o **guardião do anjo** dessa gestão e você, meu pequeno garfanhoto, foi o sorteado para ser o **anjo de {anjo}**. Cuide para que essa pessoa se sinta **muuuuuito bem** essa gestão.

        E atenção, **guarde essa informação apenas para você**! Tudo bem?

        Neste formulário ({url}), você pode indicar os **mimos favoritos de seu protegido**. Além disso, garanta que você também coloque suas preferências.

        Qualquer coisa, pode contar comigo!

        **Boa Gestão!**
        """

    for pessoa in pessoas:
        nome = pessoa['nome']
        anjo = anjos[nome]
        mensagem = mensagem_base.format(
            nome=nome, anjo=anjo, url=formulario_url)
        mensagens[pessoa['email']] = mensagem

    return mensagens

mensagens = criar_mensagens(pessoas, anjos)

def enviar_emails(mensagens):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(REMETENTE, SENHA)

    for destinatario, mensagem in mensagens.items():
        msg = MIMEMultipart()
        msg['From'] = REMETENTE
        msg['To'] = destinatario
        msg['Subject'] = "Sorteio de Anjos"

        msg.attach(MIMEText(mensagem, 'plain'))

        server.send_message(msg)

    server.quit()

enviar_emails(mensagens)

