import PyPDF2 # type: ignore
import re
import requests
import sys
import os 
from bs4 import BeautifulSoup
from pj_remates import *

def downloadTodaysNews():
    # URL de la Gaceta Oficial
    url = "https://www.imprentanacional.go.cr/gaceta/"

    # Realizar la solicitud HTTP
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar elementos específicos (por ejemplo, enlaces a las Gacetas)
        gacetas = soup.find_all('a', href=True)  # Busca todos los enlaces

        # Filtrar y mostrar enlaces que contengan "gaceta"
        for gaceta in gacetas:
            if "/pub/2025/" in gaceta['href'].lower():
                pdf_url = gaceta['href']
                regex = r"/(?:[^/]*/){2}(.*)"
                match = re.search(regex, pdf_url)
                fullurl = "https://www.imprentanacional.go.cr/pub/" + match.group(1)
                response = requests.get(fullurl)
                if response.status_code == 200:
                    script_dir = os.path.dirname(__file__)
                    rel_path = "../data/todays.pdf"
                    abs_file_path = os.path.join(script_dir, rel_path)
                    with open(abs_file_path, "wb") as file:
                        file.write(response.content)
                    print("PDF descargado correctamente.")
                    break
                else:
                    print(f"Error al descargar el PDF: {response.status_code}")
                break    
    else:
        print(f"Error al acceder al sitio: {response.status_code}")

def readstodaysPDF():
    # Abrir el archivo PDF
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/todays.pdf"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'rb') as file:
        # Crear un objeto PDF reader
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Número de páginas en el PDF
        num_pages = len(pdf_reader.pages)
        
        # Leer todas las páginas
        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        storePDFtext(text)

def storePDFtext(text):
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/todays.pdf"
    abs_file_path = os.path.join(script_dir, rel_path)
    f = open(abs_file_path, "a")
    f.write(text)
    f.close()

def getRemates():
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/todays.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    #open and read the file after the appending:
    f = open( abs_file_path , "r")
    text = f.read()
    print(len(text))
    
    pattern = r"(?s)REMATES\s*AVISOS\s*(.*?)(?=\nINSTITUCIONES)"
    matches = re.search(pattern, text)

    posibleRematesRaw = matches.group(1)

    pattern = r"(?s)con una base\s*.*?(?=25% de la base original)"
    remates = re.findall(pattern, posibleRematesRaw)

    return remates

def split_in_half(text):
    mid = len(text) // 2
    return text[:mid], text[mid:]

def createRematesGaceta(remates_raw):
    remates = []

    for remate in remates_raw:
        remates.append(Remate(raw=remate))

    return remates

def main():
    #downloadTodaysNews()
    readstodaysPDF()
    remates = getRemates()
    print(createRematesGaceta(remates)[0])
    

if __name__ == '__main__':
    main()