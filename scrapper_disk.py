import random
import time
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class Browser: 
    browser: webdriver.Chrome

    def __init__(self):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def open_page(self, url: str):
        self.browser.get(url)

    def close_browser(self):
        self.browser.quit()  

    def scroll_until_end(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        
        while True:
            # Desplazar hacia abajo
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Espera para que cargue el contenido adicional

            # Calcular la nueva altura de la página
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break  # Se ha llegado al final, no hay más contenido cargado
            last_height = new_height
  
    def select_song(self):
        # Obtener todos los elementos
        disks = self.browser.find_elements(By.XPATH, "//*[starts-with(@href, 'browse/')]")

        # Crear un diccionario clave-valor (nombre de la canción, href)
        disk_dict = {song.text: song.get_attribute('href') for song in disks}

        # Obtener una canción aleatoria
        chosen_disk = random.choice(list(disk_dict.items()))

        # Mostrar el nombre de la canción y su enlace
        print(f"El disco seleccionado es {chosen_disk[0]} y lo podes escuchar en {chosen_disk[1]}")

        return chosen_disk

    def random_disk(self, url: str):
        # Abrir la página
        self.open_page(url)

        # Realizar el scroll hasta el final para cargar todo el contenido
        self.scroll_until_end()

        # Esperar un poco para que cargue todo
        time.sleep(2)

        # Seleccionar un disco aleatorio
        return self.select_song()

