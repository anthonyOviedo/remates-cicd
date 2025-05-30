from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64
import shutil
import os
import sys
import fitz  # PyMuPDF


# Set Chrome options to enable kiosk printing mode
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--kiosk-printing")  # Automatically print without showing the print dialog
download_dir = os.getcwd()

prefs = {
    "download.default_directory": download_dir,  # Set to working directory
    "download.prompt_for_download": False,       # Disable download prompt
    "download.directory_upgrade": True,          # Auto-upgrade downloads
    "safebrowsing.enabled": True,                # Enable safe browsing
}
chrome_options.add_experimental_option("prefs", prefs)


# Initialize WebDriver with options
driver = webdriver.Chrome(options=chrome_options)


# Configuration
EMAIL = "antony-08@hotmail.com"
PASSWORD = "NyQ7lXJu1"

# Ensure correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python script.py <PROVINCIA> <MATRICULA>")
    sys.exit(1)

# Get the values from command-line arguments
PROVINCIA = sys.argv[1]  # First argument after the script name
MATRICULA = sys.argv[2]  # Second argument

# Print values for verification
print(f"PROVINCIA: {PROVINCIA}")
print(f"MATRICULA: {MATRICULA}")
SCREENSHOT_PATH = "screenshot.png"

def login():
    driver.get("https://www.rnpdigital.com/shopping/login.jspx")
    time.sleep(3)
    
    # Locate the correo electrónico field and input the email
    correo_element = driver.find_element(By.XPATH, "//p[contains(text(), 'Correo electrónico:')]")
    next_element = correo_element.find_element(By.XPATH, "following-sibling::*")
    next_element.send_keys(EMAIL)

    # Locate the contraseña field and input the password
    password_element = driver.find_element(By.XPATH, "//p[contains(text(), 'Contraseña:')]") 
    next_element = password_element.find_element(By.XPATH, "following-sibling::*")
    next_element.send_keys(PASSWORD)

    # Locate the input element with value "Ingresar" and click it
    submit_button = driver.find_element(By.XPATH, "//input[@value='Ingresar']")
    submit_button.click()

    time.sleep(3)  # Wait for the next page to load

def search_finca():


    driver.get("https://www.rnpdigital.com/shopping/consultaDocumentos/paramConsultaFinca.jspx")
    
    # Explicit wait for the select element (params:j_id271)
    select_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name*="params:"]'))
    )
    
    select = Select(select_element)
    select.select_by_value(PROVINCIA)  # Select the province based on the value
    

    # Explicit wait for the finca input element using ID for params:finca
    select_element_finca = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "params:finca"))  # Replace with the actual ID if needed
    )
    time.sleep(3)  # Wait for the next page to load

    select_element_finca.send_keys("")
    select_element_finca.send_keys(MATRICULA)


    time.sleep(2)  # Wait for the next page to load
    print("Finca search completed! will be tried now")

    btnconsulta = driver.find_element(By.ID, "params:argus")
    next_element = btnconsulta.find_element(By.XPATH, "following-sibling::*")
    next_element.click()
    time.sleep(3)  # Wait for the next page to load

    print("PDF de los derechos")  # Wait for user input before proceeding
    try:    
        # Hide everything but the div
        driver.execute_script("""
    document.body.innerHTML = document.getElementById('central').outerHTML
                                      """)

        # Use DevTools Protocol to generate PDF
        result = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True
        })

        # Save PDF to file
        pdf_data = base64.b64decode(result['data'])
        with open(f"{PROVINCIA}-{MATRICULA}-derechos.pdf", "wb") as f:
            f.write(pdf_data)
        print("PDF generated successfully and saved as {PROVINCIA}-{MATRICULA}-derechos.pdf")
        time.sleep(3)  # Wait for modal or action if needed


    except Exception as e:
        print(f"Error generating PDF: {e}")
        driver.save_screenshot(SCREENSHOT_PATH)
        print(f"Screenshot saved to {SCREENSHOT_PATH}")
        return
    
 
    
    
    try:
        # Encuentra todos los <a> dentro de la tabla
        table = driver.find_element(By.ID, "listadoDerechosForm:misDerechos")
        links = table.find_elements(By.XPATH, ".//a[starts-with(@id, 'listadoDerechosForm:misDerechos:') and contains(@id, ':fila')]")
        print(f"Se encontraron {len(links)} enlaces.")

        for index in range(len(links)):
            print(f"[{index}] Clicking link: {links[index].text}")
            links[index].click()
            time.sleep(2)  # Let the page load/render updated content
            
            print("Attempting to  print content...")
            try:
                driver.execute_script("""
                    document.body.innerHTML = document.getElementById('central').outerHTML;
                """)
                # Use DevTools Protocol to generate PDF
                result = driver.execute_cdp_cmd("Page.printToPDF", {
                    "printBackground": True
                })
                print("PDF generation initiated...")
                # Save PDF to file
                pdf_data = base64.b64decode(result['data'])
                with open(f"derecho-.pdf", "wb") as f:
                    f.write(pdf_data)
                print("Print button clicked successfully.")
                time.sleep(3)  # Wait for modal or action if needed
            except Exception as e:
                print(f"Error intentando generar PDF: {e}")


            time.sleep(4)
            driver.get("https://www.rnpdigital.com/shopping/consultaDocumentos/ListingDerechosFinca.jspx")

            table = driver.find_element(By.ID, "listadoDerechosForm:misDerechos")
            links = table.find_elements(By.XPATH, ".//a[starts-with(@id, 'listadoDerechosForm:misDerechos:') and contains(@id, ':fila')]")
            
            old_filename = "derecho-.pdf"
            new_filename = f"{PROVINCIA}-{MATRICULA}-derecho-{links[index].text}.pdf"

            if os.path.exists(old_filename):
                os.rename(old_filename, new_filename)
                print(f"File renamed to {new_filename}")
            else:
                print(f"File {old_filename} not found.")

  
    except Exception as e:
        print(f"Error finding links in the table: {e}")

def search_ubicacion_finca():
    #aqui vamos a buscar la ubicacion de la finca
    print("Searching ubicacion finca...")

    driver.get("https://www.rnpdigital.com/shopping/consultaDocumentos/paramConsultaCatastro.jspx")


    select_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name*="formBusqueda:j_id271"]'))
    )
    
    select = Select(select_element)
    select.select_by_value("F")  # Select the province based on the value
    time.sleep(3)  # Wait for the next page to load
    
    select_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name*="formBusqueda:j_id303"]'))
    )
    
    select = Select(select_element)
    select.select_by_value(PROVINCIA)  # Select the province based on the value
    time.sleep(3)  # Wait for the next page to load
    finca = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, 'formBusqueda:finca'))
    )
    
    finca.send_keys(MATRICULA)  # Select the province based on the value
    time.sleep(3)  # Wait for the next page to load

    btnconsulta = driver.find_element(By.ID, "formBusqueda:j_id357")
    btnconsulta.click()
    time.sleep(3)  # Wait for the next page to load

    #aqui necesitamos capturar el primer a link que nos encontremos.

    try:
        # Wait for the tbody to be present
        tbody = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "formBusqueda:fincaTable:tb"))
        )

        # Find all <a> tags within the tbody
        links = tbody.find_elements(By.TAG_NAME, "a")

        # If at least one link is found, click the first
        if links:
            print(f"Clicking first link: {links[0].text}")
            links[0].click()
            tomar_pdf()  # Call the function to generate the PDF
        else:
            print("No <a> elements found in tbody.")

    except Exception as e:
        print(f"no se encontraron multiples enlaces: {e}")
        tomar_pdf()  # Call the function to generate the PDF
    


    

def get_location_PDF():
    doc = fitz.open("./{PROVINCIA}-{MATRICULA}-location.pdf")
    for page in doc:
        text = page.get_text()
        print(text)
    input("Press Enter to continue...")  # Pause for user inpu

def tomar_pdf():
    print("PDF con el location")  # Wait for user input before proceeding
    try:    
        # Hide everything but the div
        driver.execute_script("""document.body.innerHTML = document.getElementById('central').outerHTML""")

        # Use DevTools Protocol to generate PDF
        result = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True
        })

        # Save PDF to file
        pdf_data = base64.b64decode(result['data'])
        with open(f"{PROVINCIA}-{MATRICULA}-location.pdf", "wb") as f:
            f.write(pdf_data)
        print("PDF generated successfully and saved as {PROVINCIA}-{MATRICULA}-location.pdf")
        time.sleep(3)  # Wait for modal or action if needed

        #analice the PDF and extract the text corresponding to the location.

        #execute the script for the location translation

    except Exception as e:
        print(f"Error generating PDF: {e}")
        driver.save_screenshot(SCREENSHOT_PATH)
        print(f"Screenshot saved to {SCREENSHOT_PATH}")
        return

try:
    login()
except Exception as e:
    print(f"Login failed: {e}")

try:
    search_ubicacion_finca()
except Exception as e:
    print(f"Error searching ubicacion finca: {e}")

try:    
    search_finca()
except Exception as e:
    print(f"Error: {e}")


driver.quit()  # Close the browser

try:
    # Define source and destination directories
    source_dir = os.getcwd()
    dest_dir = os.path.join(".", "data", "pdf", "derechos")
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    # Loop through all PDF files and move them
    for filename in os.listdir(source_dir):
        if filename.endswith(".pdf"):
            src_path = os.path.join(source_dir, filename)
            dest_path = os.path.join(dest_dir, filename)
            shutil.move(src_path, dest_path)
            print(f"Moved: {filename} -> {dest_path}")
except Exception as e:
    print(f"Error moving files: {e}")
