from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re, os, requests, pdfkit



class Scraper:
    def __init__(self):
        self.driver = self.get_driver()

    def get_driver(self):
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        return driver
    
    def login(self):
        user_input = self.driver.find_element(By.ID, "sleUserName")
        pass_input = self.driver.find_element(By.ID, "slePassword")
        user_input.send_keys("gunsbodyrepair")
        pass_input.send_keys("MERIMEN1234!")
        pass_input.send_keys(Keys.ENTER)
        print('Successfully logged in')

    def search_data(self, search_value):
        # search page
        search_input = WebDriverWait(self.driver,timeout=30).until(
            EC.element_to_be_clickable((By.ID, "SRCH")))
        search_input.send_keys(search_value)
        search_input.send_keys(Keys.ENTER)

        # list of search result
        search_result = WebDriverWait(self.driver,timeout=30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="MRMR1"]/td[3]/a')))
        search_result.click()

        # dokumen tab
        dok_tab = WebDriverWait(self.driver,timeout=30).until(
            EC.element_to_be_clickable((By.ID, "ClaimMenu$4")))
        dok_tab.click()

        # dokumen list
        WebDriverWait(self.driver,timeout=30).until(
            EC.presence_of_all_elements_located((By.ID, 'MRMmaintable')))
        print(f'{search_value} docs found!')
    
    def get_files(self, url, search_values):
        self.driver.get(url)
        self.login()
        for search_item in search_values:
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
                os.makedirs(folder_name)

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
                        with open(f"{folder_name}/{filename}.jpg", 'wb') as f:
                            f.write(img)
                    elif doc_type == "Load PDF":
                        pdf = requests.get(doc_url).content
                        with open(f"{folder_name}/{filename}.pdf", 'wb') as f:
                            f.write(pdf)
                    elif doc_type == "Load HTM":
                        pdfkit.from_url(doc_url, f"{folder_name}/{filename}.pdf")
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    url = "https://indonesia.merimen.com/claims/index.cfm?skip_browsertest=1&"
    # search_values = ["B 2293 PKW","B 1461 JFA","B 2431 UZS","B 1236 KZW","B 2291 UZR","B 1236 JFF","B 805 FBI","B 1994 WZE"]

    search_values = ["B 2293 PKW","B 1461 JFA","B 2431 UZS"]

    scraper = Scraper()
    scraper.get_files(url, search_values)
    
