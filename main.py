import sys
import getpass
from script import *
from pdfManipulation import *

def fileLogin(f):
    lines = f.readlines()
    user = lines[0][:-1]
    pwd = lines[1][:-1]
    
    return user, pwd
   
def typedLogin():
    user = input(" Usuário: ")
    pwd = getpass.getpass(" Senha: ")

    return user, pwd

print("-- Sistema de Acesso --\n")

try:
    f = open('login.txt')
    user, pwd = fileLogin(f)
    f.close()
except FileNotFoundError:
    user, pwd = typedLogin()
    
get_pdf(user, pwd)
pdf_print()

