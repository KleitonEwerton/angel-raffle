import smtplib

import csv

def ler_arquivo_csv(nome_arquivo):
    with open(nome_arquivo, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        pessoas = [row for row in csv_reader]
    return pessoas


