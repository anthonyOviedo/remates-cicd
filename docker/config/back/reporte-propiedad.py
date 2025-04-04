from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys 
import os



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

     #Locate the contraseña field and input the password
    btnconsulta = driver.find_element(By.ID, "params:argus")
    next_element = btnconsulta.find_element(By.XPATH, "following-sibling::*")
    next_element.click()
    time.sleep(3)  # Wait for the next page to load


    # download the document
    print("Trying to print the document")
    # Using contains() to locate part of the onclick text
    link = driver.find_element(By.XPATH, "//a[contains(@onclick, 'printdiv')]")
    # Click the link to trigger the print window
     
    time.sleep(3)  # Wait for the next page to load
    

    driver.get("https://www.rnpdigital.com/shopping/consultaDocumentos/paramConsultaCatastro.jspx")

    select_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name*="formBusqueda:j_id272"]'))
    )
    select = Select(select_element)
    select.select_by_value("F")  # Select the province based on the value
    time.sleep(3)  # Wait for the next page to load
    
    select_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name*="formBusqueda:j_id304"]'))
    )
    select = Select(select_element)
    select.select_by_value(PROVINCIA)  # Select the province based on the value
    time.sleep(3)  # Wait for the next page to load

    finca = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, 'formBusqueda:finca'))
    )
    finca.send_keys(MATRICULA)  # Select the province based on the value
    time.sleep(3)  # Wait for the next page to load
    input("Press Enter to continue...")
  
    btnconsulta = driver.find_element(By.ID, "formBusqueda:j_id358")
    btnconsulta.click()
    time.sleep(3)  # Wait for the next page to load

    
try:
    login()
    search_finca()

    
    print("Process completed successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    input("Press Enter to continue...")
    driver.quit()  # Close the browser
