import logging
import openpyxl
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

tipo_estabelecimento = "lojas de roupa"
cidade = "ilhéus"

busca = f"{tipo_estabelecimento} em {cidade}".replace(" ", "+")

# Abrir navegador
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-features=EnableEphemeralGuestProfiles")
chrome_options.add_argument("--disable-features=UnloadBrowserOnReboot")
driver = webdriver.Chrome(options=chrome_options)
# Entrar no site do google maps
driver.get(f"https://www.google.com/search?client=gws-wiz-local&tbm=lcl&q={busca}")
driver.set_window_size(1920, 1080)
sleep(5)

places_list = []

# Coletar info
count = 0
while True:
    try:
        itens = driver.find_elements(By.XPATH, "//div[@class='rllt__details']")
        for item in itens:
            item.click()
            sleep(1.5)
            try:
                name = driver.find_element(
                    By.XPATH, "//div[@class='kp-header']//h2//span"
                ).text
            except:
                name = "Nome não encontrado"

            try:
                address = driver.find_elements(
                    By.XPATH,
                    "//div[@data-attrid='kc:/location/location:address']//div//span",
                )[-1].text
            except:
                address = "Endereço não encontrado"

            try:
                phone = driver.find_element(
                    By.XPATH,
                    "//div[@data-attrid='kc:/collection/knowledge_panels/has_phone:phone']//div//span//span//a//span",
                ).text
            except:
                phone = "Telefone não encontrado"

            places_list.append((name, address, phone))
        driver.find_element(By.XPATH, "//a[@id='pnnext']").click()
        count += 1
        sleep(5)
    except:
        break


print(places_list)
print(len(places_list))
print(count)

# Colocar info no excel
workbook = openpyxl.Workbook()
sheet = workbook.active

sheet["A1"].value = "Nome"
sheet["B1"].value = "Endereço"
sheet["C1"].value = "Telefone"


for row_index, row in enumerate(
    sheet.iter_rows(min_row=2, max_col=3, max_row=len(places_list))
):
    for cell_index, cell in enumerate(row):
        cell.value = places_list[row_index][cell_index]


workbook.save(f"resultado - {tipo_estabelecimento} em {cidade}.xlsx")

driver.quit()
