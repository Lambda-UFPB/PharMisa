from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


class PharmitControl:

    def __init__(self):
        options = Options()
        options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=options)

    def _upload_files(self):
        # Get page
        self.driver.get("https://pharmit.csb.pitt.edu/search.html")
        self.driver.implicitly_wait(3)
        # Upload ligand
        ligand = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[3]/div[2]/input')
        ligand.send_keys("/home/kdunorat/Documentos/LambdaPipe/files/7KR1-pocket3-remdesivir-cid76325302.pdbqt")
        # Upload receptor
        time.sleep(3)
        receptor = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[3]/div[1]/input')
        receptor.send_keys("/home/kdunorat/Documentos/LambdaPipe/files/7KR1.pdbqt")

    def _get_json(self):
        # Download first json
        time.sleep(3)
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[5]/div/button').click()

    def _upload_json(self):
        # Upload modified json
        load_session = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[5]/div/div/input')
        load_session.send_keys("/home/kdunorat/Documentos/LambdaPipe/files/pharmit.json")

    def _search(self):
        # Modificar o value (banco de dados) dps
        # Search
        search = self.driver.find_element(By.XPATH, '//*[@id="pharmitsearchbutton"]')
        search.click()

    def _download(self):
        # Minimize
        self.driver.find_element(By.XPATH, '//*[@id="pharmit"]/div[1]/div[4]/div[3]/div/button[1]').click()
        # Saving
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//*[@id="pharmit"]/div[1]/div[4]/div[3]/div/button[2]').click()

    def run(self):
        #self._upload_files()
        #self._get_json()
        self._upload_json()
        #self._search()
        #self._download()
