import sys
import getpass
from script import *
from pdfManipulation import *

print("-- Sistema de Acesso --\n")
user = input(" Usuário: ")
pwd = getpass.getpass(" Senha: ")

get_pdf(user, pwd)
pdf_print()

