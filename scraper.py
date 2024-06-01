from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re, os, requests, pdfkit, logging, sys


logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Scraper:
    def __init__(self):
        self.driver = self.get_driver()

    def get_driver(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        return driver
    
    def login(self, user):
        user_input = self.driver.find_element(By.ID, "sleUserName")
        pass_input = self.driver.find_element(By.ID, "slePassword")
        if user == 'gunsbodyrepair':
            user_input.send_keys("gunsbodyrepair")
            pass_input.send_keys("MERIMEN1234!")
        elif user == 'pb_tio':
            user_input.send_keys("pbs_tio")
            pass_input.send_keys("aditya2162")
        elif user == 'tt_tio':
            user_input.send_keys("bb_tio")
            pass_input.send_keys("aditya2162")
        pass_input.send_keys(Keys.ENTER)

    def search_data(self, search_value):
        # search page
        search_input = WebDriverWait(self.driver,timeout=10).until(
            EC.element_to_be_clickable((By.ID, "SRCH")))
        search_input.send_keys(Keys.CONTROL + "a")
        search_input.send_keys(search_value)
        search_input.send_keys(Keys.ENTER)

        # list of search result
        logging.info(f'searching {search_value}')
        print(f'searching {search_value}')
        search_result = WebDriverWait(self.driver,timeout=10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, search_value)))
        search_result.click()

        # dokumen tab
        dok_tab = WebDriverWait(self.driver,timeout=30).until(
            EC.element_to_be_clickable((By.ID, "ClaimMenu$4")))
        dok_tab.click()

        # dokumen list
        WebDriverWait(self.driver,timeout=10).until(
            EC.presence_of_all_elements_located((By.ID, 'MRMmaintable')))
        print(f'{search_value} docs found!')
        logging.info(f'{search_value} docs found!')
    
    def get_files(self, url, user, search_values):
        self.driver.get(url)
        self.login(user)  
        current_url = self.driver.current_url
        if current_url == "https://indonesia.merimen.com/claims/index.cfm?skip_browsertest=1&":
            print('Login failed!')
            logging.info('Login failed!')
            self.driver.quit()
        else:
            print('Successfully logged in')
            logging.info('Successfully logged in')         
        
        for i, search_item in enumerate(search_values):
            print(f'Searching {i+1} of {len(search_values)}')
            try:
                # navigating through pages
                self.search_data(search_item)

                current_url = self.driver.current_url
                token = re.search(r"corole=.*$", current_url).group(0)
                view_url = "https://indonesia.merimen.com/claims/index.cfm?fusebox=SVCdoc&fuseaction=dsp_viewersmart&noimgviewer=1&ftype=2&docid="

                table_element = self.driver.find_element(By.ID, 'doclisting')
                element_names = table_element.find_elements(By.TAG_NAME, 'b')
                element_ids = table_element.find_elements(By.PARTIAL_LINK_TEXT, 'Load')
                # create folder
                folder_name = search_item.replace(" ", "")
                path = os.path.join(user, search_item)
                os.makedirs(path)

                for i in range(len(element_names)):
                    print(f'Downloading {i+1} of {len(element_names)}')
                    # filename start by number+filename
                    filename = str(i+1)+'_'+element_names[i].text.replace('/', '')
                    doc_type = element_ids[i].text
                    docid = element_ids[i].get_attribute('href')
                    docid = re.search(r"SVCDOCAttView\((\d+)", docid).group(1)
                    doc_url = view_url + docid + "&" + token
                    if doc_type == "Load JPG":
                        img = requests.get(doc_url).content
                        with open(f"{path}/{filename}.jpg", 'wb') as f:
                            f.write(img)
                    elif doc_type == "Load PDF":
                        pdf = requests.get(doc_url).content
                        with open(f"{path}/{filename}.pdf", 'wb') as f:
                            f.write(pdf)
                    elif doc_type == "Load HTM":
                        pdfkit.from_url(doc_url, f"{path}/{filename}.pdf")
            except Exception as e:
                print(f'Failed for {search_item}')
                logging.info(f'Failed for {search_item}')
                print(e)
                continue


if __name__ == "__main__":
    url = "https://indonesia.merimen.com/claims/index.cfm?skip_browsertest=1&"
    

    # search_values = ["B 2293 PKW","B 1461 JFA","B 2431 UZS"]

    with open('plat1.txt', 'r') as f:
        data = f.readlines()

    # check unfinished search
    search_values = [item.strip().replace(" ", "") for item in data]    
    unfinished_search = []

    for i in search_values:
        if os.path.exists(f'results/{i}'):
            continue
        else:
            unfinished_search.append(i)
    scraper = Scraper()
    scraper.get_files(url, unfinished_search)
    # print(unfinished_search)
