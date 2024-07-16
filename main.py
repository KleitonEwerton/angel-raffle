import smtplib
import random
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

FILE = 'pessoas.csv'
REMETENTE = 'remetente.emailc.com'
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
    formulario_url = "https://docs.google.com/forms/d/e/1FAIpQLSeA0I3Iq-hZmQdWIyx2sSL99W3CDX-nRBepuzFpcnnrlReUSQ/viewform?usp=sf_link"

    mensagem_base = """
    <p>Olá {nome},</p>

    <p>Sou o <strong>guardião do anjo</strong> dessa gestão e você, meu pequeno garfanhoto, foi o sorteado para ser <strong>anjo de {anjo}</strong>. Cuide para que essa pessoa se sinta <strong>muuuuuito bem</strong> essa gestão.</p>

    <p>E atenção, <strong>guarde essa informação apenas para você</strong>! Tudo bem?</p>

    <p>Neste formulário ({url}), você pode encontrar os <strong>mimos favoritos de seu protegido</strong>. Além disso, garanta que você também coloque suas preferências.</p>

    <p>Qualquer coisa, pode contar comigo!</p>

    <p><strong>Boa Gestão!</strong></p>
    """

    for pessoa in pessoas:
        nome = pessoa['nome']
        anjo = anjos[nome]
        mensagem = mensagem_base.format(
            nome=nome, anjo=anjo, url=formulario_url)
        mensagens[pessoa['email']] = mensagem

    return mensagens


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

        msg.attach(MIMEText(mensagem, 'html'))
        
        try:
            server.send_message(msg)
            print(f'E-mail enviado para {destinatario}')
        except Exception as e:
            print(f'Erro ao enviar e-mail para {destinatario}, mensagem: {mensagem}')
            print(e)
            
    server.quit()


mensagens = criar_mensagens(pessoas, anjos)

enviar_emails(mensagens)
