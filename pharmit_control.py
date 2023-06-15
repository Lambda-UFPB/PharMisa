from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from json_handler import JsonHandler
import time
import utils


class PharmitControl:

    def __init__(self):
        options = Options()
        options.add_experimental_option('detach', True)
        self.db_tuple = ()
        self.proceed = False
        self.driver = webdriver.Chrome(options=options)

    def _open_tabs(self):

        # Get tabs
        for db in self.db_tuple:
            self.driver.execute_script(f"window.open('about:blank','{db}');")
            self.driver.switch_to.window(f"{db}")
            self.driver.get("https://pharmit.csb.pitt.edu/search.html")
            time.sleep(3)

    def _upload_complex(self):
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

    def _change_db(self):
        time.sleep(3)
        database = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[1]/button[1]')
        for db in self.db_tuple:
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1]);", database, db)

    def _upload_json(self):
        # Create second json
        jsh = JsonHandler()
        jsh.create_json()

        # Upload session
        load_session = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[5]/div/div/input')
        load_session.send_keys("/home/kdunorat/Documentos/LambdaPipe/files/file_1.json")
        for db in self.db_tuple:
            self.driver.switch_to.window(f"{db}")
            load_session = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[5]/div/div/input')
            load_session.send_keys("/home/kdunorat/Documentos/LambdaPipe/files/file_1.json")
            time.sleep(3)

    def _search(self):
        # Modificar o value (banco de dados) dps
        # Search
        search = self.driver.find_element(By.XPATH, '//*[@id="pharmitsearchbutton"]')
        time.sleep(2)
        search.click()
        self._search_loop()
        for db in self.db_tuple:
            self.driver.switch_to.window(f"{db}")
            search = self.driver.find_element(By.XPATH, '//*[@id="pharmitsearchbutton"]')
            time.sleep(2)
            search.click()
            self._search_loop()

    def _search_loop(self):
        while True:
            minimize_button = self.driver.find_element(By.XPATH, '//*[@id="pharmit"]/div[1]/div[4]/div[3]/div/button[1]')
            try:
                no_results = self.driver.find_element(By.CLASS_NAME, "dataTables_empty")
                if no_results.text == 'No results found':
                    print(no_results.text)
                    break
            except NoSuchElementException:
                pass

            if minimize_button.is_enabled():
                self.proceed = True
                break
            else:
                time.sleep(1)
        if self.proceed:
            pass
            #self._download(minimize_button)

    def _download(self, minimize_button):
        # Minimize
        time.sleep(3)
        minimize_button.click()
        try:
            self.driver.switch_to.alert.dismiss()
        except NoAlertPresentException:
            pass
        # Saving
        while True:
            save_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[3]/div[2]/button')
            if save_button.is_enabled():
                time.sleep(1)
                save_button.click()
                break
            time.sleep(1)

    def run(self):
        full_tuple = ('molport', 'chembl', 'chemdiv', 'chemspace', 'mcule', 'ultimate', 'nsc', 'pubchem', 'wuxi-lab', 'zinc')
        self._upload_complex()
        self._get_json()
        for i in range(2):
            if i == 0:
                self.db_tuple = full_tuple[:4]
            else:
                self.db_tuple = full_tuple[4:]
            self._open_tabs()
            self._upload_json()
            self._change_db()
            self._search()
            break
            #self.driver.close()
