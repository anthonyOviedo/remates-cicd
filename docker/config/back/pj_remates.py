import re
from datetime import datetime
import requests
import json

class Remate:
    def __init__(self, exp=None, precio=None, medidas=None, ubicacion=None, uso=None, 
                 primera_fecha=None, segunda_fecha=None, tercera_fecha=None, candidato=None, 
                 raw=None, plano=None, url=None, matricula=None, id=None, favorito=None, juzgado=None):
        # Inicializar los atributos, si no se pasa ningún valor se usan valores predeterminados (None)
        self.id = id 
        self.exp = exp
        self.precio = precio
        self.medidas = medidas
        self.ubicacion = ubicacion
        self.uso = uso
        self.primera_fecha = primera_fecha
        self.segunda_fecha = segunda_fecha
        self.tercera_fecha = tercera_fecha
        self.candidato = candidato
        self.plano = plano
        self.raw = raw
        self.url = url
        self.matricula = matricula
        self.favorito = False
        self.juzgado = juzgado
        self.comments = [] 
    
    def __str__(self):
        precio_ = precioFormatter(self.precio)
        return (f"*******************************************Remate:\n"
                f"Precio: {self.id}\n"
                f"Precio: {precio_}\n"
                f"Medidas: {self.medidas} mts2 \n"
                f"Ubicación: {self.ubicacion}\n"
                f"Uso: {self.uso}\n"
                f"Plano: {self.plano}\n"
                f"Matricula: {self.matricula}\n"
                f"Primera Fecha: {self.primera_fecha}\n"
                f"Segunda Fecha: {self.segunda_fecha}\n"
                f"Tercera Fecha: {self.tercera_fecha}\n"
                f"URL: {self.url}\n")
    
def to_dict(remate):
        # Convert the instance to a dictionary
        return {
            'id': remate.id,
            'exp': remate.exp,
            'precio': remate.precio,
            'medidas': remate.medidas,
            'ubicacion': remate.ubicacion,
            'uso': remate.uso,
            'matricula': remate.matricula,
            'primera_fecha': str(remate.primera_fecha),
            'segunda_fecha': str(remate.segunda_fecha),
            'tercera_fecha': str(remate.tercera_fecha),
            'candidato': remate.candidato,
            'plano': remate.plano,
            'raw': remate.raw,
            'url': remate.url,
            'favorito': remate.favorito,
            'juzgado': remate.juzgado
            
        }

def precioFormatter(precio):
    # El método __str__ para representar la instancia como una cadena
    try:
        precio_ = "{:,}".format(precio).replace(",", " ")
        return precio_
    except Exception as e:
        print(f"Error: {e}")
    return precio
    
def precioBase(text):
    # Expresión regular corregida
    pattern = r"[A-ZÁÉÍÓÚÑ\s]+(?=,)"

    # Buscar coincidencia
    match = re.search(pattern, text)
    
    return match.group(0) if match else None

def tipoRemate(text):
    type_pattern = r"la cual es terreno\s([^.]+)\."
    type_match = re.search(type_pattern, text)
    if type_match:
        return type_match.group(1)

def isFinca(text):
    categ_pattern = r"sáquese a remate (la finca)"
    match = re.findall(categ_pattern, text)

    terreno = False
    if match:
        terreno = True

    return terreno

def remate_raw_list(text,id):
    
    try:
        # Regex to match paragraphs starting with "En este Despacho"
        pattern = r"(?<=En este Despacho,)(.*?)(?=de 2)"

        # Find all matches
        matches = re.findall(pattern, text)

        remates = [] 

        for match in matches:
            remates.append(Remate(raw=match,exp=id))
    except Exception as e:
        print (f"Error: {e}")



    return remates

def medidas_(text):
    pattern = r"(?<=\bMIDE\b)(.*?)(?=\bMETROS\b)"

    n_match = re.search(pattern, text)
    return  palabras_a_medidas(n_match.group(0)) if n_match else "not found "

def ubicacion_(text):
    # Regex to match location details with a comma as the limit
    distrito_pattern = r"Situada en el DISTRITO\s([^\n,]+)"
    canton_pattern = r"CANTÓN\s([^\n,]+)"
    provincia_pattern = r"de la provincia de\s([^\n.]+)"

    # Find matches
    distrito = re.search(distrito_pattern, text)
    canton = re.search(canton_pattern, text)
    provincia = re.search(provincia_pattern, text)

    # Print and return the location information
    if distrito and canton and provincia:
       return f"{provincia.group(1)} - {canton.group(1)}"
    else:
        cities = ["SAN JOSÉ", "SAN JOSE", "PUNTARENAS", "ALAJUELA", "CARTAGO", "LIMÓN", "HEREDIA", "GUANACASTE"]
        for city in cities:
            if city in text:
                found_city = city
                break  # Stop once the first city is found
        return found_city
    
def palabras_a_numero(text):
    try:
        # Diccionarios base
        unidades = {
            "cero": 0, "un":1 ,"uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
            "seis": 6, "siete": 7, "ocho": 8, "nueve": 9
        }
        especiales = {
            "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14,
            "quince": 15, "dieciséis": 16, "diecisiete": 17, "dieciocho": 18, "diecinueve": 19,
            "veinte": 20, "veintiún": 21, "veintidós": 22, "veintitrés": 23, "veinticuatro": 24,
            "veinticinco": 25, "veintiseis": 26, "veintsiete": 17, "veintiocho": 18, "veintinueve": 19,
        }
        decenas = {
            "veinte": 20, "treinta": 30, "cuarenta": 40, "cincuenta": 50,
            "sesenta": 60, "setenta": 70, "ochenta": 80, "noventa": 90
        }
        centenas = {
            "ciento": 100,"cien": 100, "doscientos": 200, "trescientos": 300, "cuatrocientos": 400,
            "quinientos": 500, "seiscientos": 600, "setecientos": 700,
            "ochocientos": 800, "novecientos": 900
        }
        multiplicadores = {
            "mil": 1000, "millón": 1000000, "millones": 1000000
        }


        
        # Regex pattern to match until 'colones' or 'dólares' (non-greedy)
        pattern = r"(.*?)(COLONES|DÓLARES)"
        # Iterate through each text and apply regex
        match = re.search(pattern, text)
        if match:
            # Capture the values before the currency and the currency type
            amount = match.group(1).strip()
            currency = match.group(2)
        

            # Procesar el texto
            palabras = amount.lower().replace("y", "").split()
            resultado = 0
            parcial = 0

            for palabra in palabras:
                if palabra in unidades:
                    parcial += unidades[palabra]
                elif palabra in especiales:
                    parcial += especiales[palabra]
                elif palabra in decenas:
                    parcial += decenas[palabra]
                elif palabra in centenas:
                    parcial += centenas[palabra]
                elif palabra in multiplicadores:
                    parcial = parcial or 1  # Si es solo "mil" o "millón", asumir 1
                    parcial *= multiplicadores[palabra]
                    resultado += parcial
                    parcial = 0
                

            resultado += parcial
            if currency == "DÓLARES":
                resultado = resultado*500
            return resultado
    except Exception as e:
        print(f"Error: {e}")
    return text

def palabras_a_medidas(text):
    unidades = {
        "cero": 0, "un":1 ,"uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
        "seis": 6, "siete": 7, "ocho": 8, "nueve": 9
    }
    especiales = {
        "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14,
        "quince": 15, "dieciséis": 16, "diecisiete": 17, "dieciocho": 18, "diecinueve": 19,
        "veinte": 20, "veintiún": 21, "veintidos": 22, "veintitrés": 23, "veinticuatro": 24,
        "veinticinco": 25, "veintiseis": 26, "veintsiete": 27, "veintiocho": 28, "veintinueve": 29,
    }
    decenas = {
        "veinte": 20, "treinta": 30, "cuarenta": 40, "cincuenta": 50,
        "sesenta": 60, "setenta": 70, "ochenta": 80, "noventa": 90
    }
    centenas = {
        "ciento": 100,"cien": 100, "doscientos": 200, "trescientos": 300, "cuatrocientos": 400,
        "quinientos": 500, "seiscientos": 600, "setecientos": 700,
        "ochocientos": 800, "novecientos": 900
    }
    multiplicadores = {
        "mil": 1000, "millón": 1000000, "millones": 1000000
    }
    resultado = 0
    parcial = 0

    palabras = text.lower().replace("y", "").split()

    for palabra in palabras:
        if palabra in unidades:
            parcial += unidades[palabra]
        elif palabra in especiales:
            parcial += especiales[palabra]
        elif palabra in decenas:
            parcial += decenas[palabra]
        elif palabra in centenas:
            parcial += centenas[palabra]
        elif palabra in multiplicadores:
            parcial = parcial or 1  # Si es solo "mil" o "millón", asumir 1
            parcial *= multiplicadores[palabra]
            resultado += parcial
            parcial = 0
        
    resultado += parcial

    return resultado
        
def get_fechas(text):
    pattern = r'Para tal efecto(?:,? se señalan las)\s(.*?)(?=\.)'
    match = re.search(pattern, text)
    primera="" 
    segunda="" 
    tercera = ""

    if match:
        primera = match.group(1)

    pattern = r'el segundo remate.*?se efectuará a las\s(.*?)\scon la base de'
    match = re.search(pattern, text)
    if match:
        segunda = match.group(1)


    pattern_third = r'para el tercer remate se señalan las\s(.*?)\scon la base'    
    match = re.search(pattern_third, text)
    if match:
        tercera = match.group(1)

    return   parse_datetime(primera), parse_datetime(segunda), parse_datetime(tercera)

def parse_datetime(text):
    number_mapping = {
        'cero': 0, 'uno': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 
        'cinco': 5, 'seis': 6, 'siete': 7, 'ocho': 8, 'nueve': 9,
        'diez': 10, 'once': 11, 'doce': 12, 'trece': 13, 'catorce': 14, 
        'quince': 15, 'dieciséis': 16, 'diecisiete': 17, 'dieciocho': 18, 
        'diecinueve': 19, 'veinte': 20, 'veintiuno': 21, 'veintidós': 22,
        'veintitrés': 23, 'veinticuatro': 24, 'veinticinco': 25, 
        'veintiséis': 26, 'veintisiete': 27, 'veintiocho': 28, 
        'veintinueve': 29, 'treinta': 30, 'treinta y uno': 31, 
        'treinta y dos': 32, 'treinta y tres': 33, 'treinta y cuatro': 34, 
        'treinta y cinco': 35, 'treinta y seis': 36, 'treinta y siete': 37, 
        'treinta y ocho': 38, 'treinta y nueve': 39, 'cuarenta': 40, 
        'cuarenta y uno': 41, 'cuarenta y dos': 42, 'cuarenta y tres': 43, 
        'cuarenta y cuatro': 44, 'cuarenta y cinco': 45, 'cuarenta y seis': 46, 
        'cuarenta y siete': 47, 'cuarenta y ocho': 48, 'cuarenta y nueve': 49, 
        'cincuenta': 50, 'cincuenta y uno': 51, 'cincuenta y dos': 52, 
        'cincuenta y tres': 53, 'cincuenta y cuatro': 54, 'cincuenta y cinco': 55, 
        'cincuenta y seis': 56, 'cincuenta y siete': 57, 'cincuenta y ocho': 58, 
        'cincuenta y nueve': 59, 'sesenta': 60, 'sesenta y uno': 61, 
        'sesenta y dos': 62, 'sesenta y tres': 63, 'sesenta y cuatro': 64, 
        'sesenta y cinco': 65, 'sesenta y seis': 66, 'sesenta y siete': 67, 
        'sesenta y ocho': 68, 'sesenta y nueve': 69, 'setenta': 70, 
        'setenta y uno': 71, 'setenta y dos': 72, 'setenta y tres': 73, 
        'setenta y cuatro': 74, 'setenta y cinco': 75, 'setenta y seis': 76, 
        'setenta y siete': 77, 'setenta y ocho': 78, 'setenta y nueve': 79, 
        'ochenta': 80, 'ochenta y uno': 81, 'ochenta y dos': 82, 
        'ochenta y tres': 83, 'ochenta y cuatro': 84, 'ochenta y cinco': 85, 
        'ochenta y seis': 86, 'ochenta y siete': 87, 'ochenta y ocho': 88, 
        'ochenta y nueve': 89, 'noventa': 90, 'noventa y uno': 91, 
        'noventa y dos': 92, 'noventa y tres': 93, 'noventa y cuatro': 94, 
        'noventa y cinco': 95, 'noventa y seis': 96, 'noventa y siete': 97, 
        'noventa y ocho': 98, 'noventa y nueve': 99, 'cien': 100,
        'dos mil veinticinco':2025,'dos mil veinticuatro':2024,
        'dos mil  veintiseis':2026, 'dos mil veintitrés':2023
    }
    month_mapping = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12,
    }

    try:

        # Regular expression to match the text format
        regex = r"del ([\w\s]+) de (\w+) del año (dos mil \w+)"
        # Find all matches
        match = re.findall(regex,text)
        if match:
            day_text, month_text, year_text = match[0]
        else:
            regex = r"del ([\w\s]+) de (\w+) de (dos mil \w+)"
            # Find all matches
            match = re.findall(regex,text)
            if match:
                day_text, month_text, year_text = match[0]

        hregex = r"(\w+) horas"
        hm = re.findall(hregex,text)
        mregex = r"(\w+) minutos"
        mm = re.findall(mregex,text)

        # Convert the Spanish words to numbers
        hour = number_mapping[hm[0]]
        if mm:
            minute = number_mapping[mm[0]] 
        else :
            minute = 0
        day = number_mapping[day_text]
        month = month_mapping[month_text]
        year = number_mapping[year_text]
        #int(''.join(number_mapping.get(word, word) for word in year_text.split()))
        
        # Create and return the datetime object
        return datetime(year, month, day, hour, minute)
    except Exception as e:
        print(f"Error: {e}")

    
    return text

def refresh_remates(page): 
    # URL endpoint
    url = "https://nexuspj.poder-judicial.go.cr/api/search"
    # Payload
    payload = {
        "q": "tipoInformacion:(Boletín AND Judicial) remate ",
        "advanced": False,
        "facets": [
            "Año:2025"
        ],
        "size": 10,
        "page": 1,
        "sort": {
            "field": "numeroDocumento",
            "order": "desc"
        },
        "exp": ""
    }
    # Headers (optional, if needed for the API)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer <your_api_token>"  # Replace with an actual token if required
    }
    # Make the POST request
    try:
        response = requests.post(url, json=payload, headers=headers)
        # Check if the request was successful

        if response.status_code == 200:
            remates = response.text
            return remates
        else:
            print(f"Error: {response.status_code}")
            print(response.text)  # Print the error response for debugging
    except Exception as e:
        print(f"An error occurred: {e}")

def saveNewPage(page, remates):
    try:
        file = f"page-{page}.json"
        # Open the file in write mode, since JSON data should replace the previous contents
        with open(file, "w") as f:
            json.dump(remates, f)  # Write JSON object to file
    except Exception as e:
        print(f"Error: {e}")

def proccesRematesJson(remates_json):
    remates_list = []
    try:  

        for i in range(10):
            exp = { "remates" : remates_json[i]['content'] , "id" : remates_json[i]['idDocument'] }
            remates_list.append(exp)

        rfl = []
        for remate in remates_list:
            some_remates = remate_raw_list(remate['remates'],remate['id'])
            rfl = rfl + some_remates
        
        remates = []
        for remate in rfl:
            remates.append(createRemate(remate))     
        return remates  

    except Exception as e:
       print("Errorwq : {e}")


def createRemate(remate):
    try:
        if isFinca(remate.raw):
            remate.id = getId(remate.raw)
            remate.precio = palabras_a_numero( precioBase(remate.raw))
            remate.uso = tipoRemate(remate.raw)
            remate.medidas = medidas_(remate.raw) 
            remate.ubicacion = ubicacion_(remate.raw)
            remate.candidato = True
            remate.primera_fecha,remate.segunda_fecha,remate.tercera_fecha =  get_fechas(remate.raw)
            remate.plano = getPlano(remate.raw)
            remate.matricula = getMatricula(remate.raw)
            remate.url = f"https://nexuspj.poder-judicial.go.cr/document/{remate.exp}"
            remate.favorito = False
            remate.juzgado = getJuzgado(remate.raw)
            
        else :
            remate.candidato = False        

        return remate
    except Exception as e:
        print(f"Error: {e}")

def getJuzgado(text):
    # Regex to match the "Juzgado" line
    pattern = r"(JUZGADO\s.*?)(?=\.)"
    match = re.search(pattern, text)
    if match:
        return match.group(0).strip()
    else:
        return 'not found'
    
def getId(text):
    match = re.search(r"Referencia N°:\s*(\d+)", text)

    if match:
        return match.group(1)
    else:
        return 'not found'
        
def getPlano(text):
    pattern = r"PLANO:\s*(\S+)"
    # Search for the pattern in the text
    match = re.search(pattern, text)
    if match:
        return match.group(1)

    pattern = r"plano\s*(\S+)"
    # Search for the pattern in the text
    match = re.search(pattern, text)
    if match:
        return match.group(1)

    pattern = r"catastrado número\s*(\S+)"
    match = re.search(pattern, text)
    if match: 
        return match.group(1)
    
    pattern = r"finca número:\s*(\S+)"
    match = re.search(pattern, text)
    if match: 
        return match.group(1)
    
    return 'not found'

def getMatricula(text):
    pattern = r"matrícula número\s*(\S+),"
    match = re.search(pattern, text)
    if match: 
        return match.group(1)

    pattern = r"matrícula\s*(\S+),"
    match = re.search(pattern, text)
    if match: 
        return match.group(1)

    pattern = r"matricula numero\s*(\S+),"
    match = re.search(pattern, text)
    if match: 
        return match.group(1)
    
    pattern = r"matr\u00edcula n\u00famero\s*(\S+),"
    match = re.search(pattern, text)
    if match: 
        return match.group(1)
    
    return 'not found'

def getloadpage(page):
    file = f"page-{page}.json"
    # Retrieve JSON data from the file
    with open(file, "r") as file:
        data = json.load(file)
    
    return data

def get_updated_remates(page):
    remate_ouput = refresh_remates(page)
    remates_json = json.loads(remate_ouput)
    try:
        file = f"page-{page}.json"
        # Open the file in write mode, since JSON data should replace the previous contents
        with open(file, "w") as f:
            json.dump(remates_json, f)  # Write JSON object to file
    except Exception as e:
        print(f"Error: {e}")

def jsonGetLoadPage(page):
    try:
        with open(f"page-{page}.json", 'r') as f:
            data = json.load(f)  # Read and parse JSON object from file
        return data
    except Exception as e:
        return None


def update_all(page):
    old = sync_data()
    new = load_new_data(page)

    print("new: ", len(new))
    print("old: ", len(old))

    # Convert old list into a set for quick lookup
    existing_ids = {item['id'] for item in old}  

    for i in new:
        item_dict = to_dict(i)
        if item_dict['id'] not in existing_ids:
            old.append(item_dict)  # Add new item if not found
            existing_ids.add(item_dict['id'])  # Update set

    print("final: ", len(old))

    with open('data/remates.json', 'w') as f:
        f.write(json.dumps(old))

    

def sync_data():
    # loads current data/remates.json 
    with open('data/remates.json', 'r') as f:
        data = json.load(f)  # Read and parse JSON object from file
    return data

def load_new_data(page):
    remates_raw_list_page = jsonGetLoadPage(page)
    remates = proccesRematesJson(remates_raw_list_page["hits"])
    candidatos = []
    for item in remates:
        if item is not None and item.candidato:
            candidatos.append(item)
    return candidatos

def main():
    #--Correr siempre, este es el que me los trae y guarda despues en json sin procesar
    remate_ouput = get_updated_remates(1)
    print(remate_ouput)
    #--Esta funcion actualiza las veces publicado o agrega el nuevo Bien 
    update_all(1)
    

    #--data rationalizer
    # data = sync_data()    
    # for item in data:
    #     item['comments'] = []
    # with open('data/remates.json', 'w') as f:   
    #     f.write(json.dumps(data))
    # print("file run successfully")

 
if __name__ == '__main__':
    main()

# Now you can serialize the list of dictionaries to JSON


