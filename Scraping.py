from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import wget
import time
import shutil


# j'ai choisi de scrapper avec Selenium vu qu'il prend en charge le javascript
# mais aussi vu qu'on va pas scrapper beaucoup de page (du coup j'ai pas utilisé scrapy)
class scraping(object):
    name=''
    def execute(self):
        #On regle les parametres du webdriver
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920,1080')
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)  
        chrome_options.add_argument("--no-sandbox")
        
        driver = webdriver.Remote(
                command_executor='http://chrome:4444/wd/hub',options=chrome_options
                                )

        
        driver.get("http://www.facebook.com")

        # par la suite on se connecte au site facebook

        username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='inputtext _55r1 _6luy']")))
        password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='inputtext _55r1 _6luy _9npi']")))

        
        username.clear()
        username.send_keys("miissawi.ramzi@yahoo.com")
        password.clear()
        password.send_keys("Elyadata")

        
        button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='_42ft _4jy0 _6lth _4jy6 _4jy1 selected _51sy']"))).click()
    # maintenant on va commencer à scrapper la page de rafael nadal
    # on va scrapper les photos de ce dernier et son nom
    # j'ai insérer plusieurs sleep() car selenium avec docker ne trouve pas parfois certaines balises du coup je lui offre plus de temps pour les charger
        images = []
        time.sleep(10)
        driver.get("https://www.facebook.com/Nadal/photos/")
        time.sleep(10)
        for j in range(0,1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
        
        
        time.sleep(5)
        
        elements = driver.find_elements(By.XPATH,"//a[@class='qi72231t nu7423ey n3hqoq4p r86q59rh b3qcqh3k fq87ekyn bdao358l fsf7x5fv s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk srn514ro oxkhqvkx rl78xhln nch0832m cr00lzj9 rn8ck1ys s3jn8y49 icdlwmnq jxuftiz4 cxfqmxzd b6ax4al1 pytsy3co om3e55n1 mfclru0v']")
        hrefs = [element.get_attribute('href') for element in elements]
        # aprés avoir prix les url de chaques images
        # on entre dans chaque liens et on scrappe l'image
        for href in hrefs:
            driver.get(href)
            time.sleep(5)
            name_balise= driver.find_elements(By.XPATH,"//a[contains(text(),'Rafa Nadal')]")
            self.name=name_balise[0].get_attribute('textContent')
            img = driver.find_elements(By.XPATH,"//img[@data-visualcompletion='media-vc-image']")
            images.append(img[0].get_attribute("src"))       

                    




        # on crée par la suite un dossier FB_SCRAPED pour stocker les images
        path = os.getcwd()
        path = os.path.join(path, "FB_SCRAPED")
        if os.path.exists(path):
            shutil.rmtree(path)


        
        os.mkdir(path)
        counter = 0
        
        for image in images:
            save_as = os.path.join(path, str(counter) + '.jpg')
            wget.download(image, save_as)
            counter += 1      
      
    
        