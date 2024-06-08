from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

import os, time


class Scraper:
    def __init__(self, user, search_item):
        self.user = user
        self.search_item = search_item
        self.path = None
        self.driver = self.get_driver()


    def get_driver(self):
        base = '/mnt/8e469d2a-6fa6-4000-abce-5925d0d4315c/python_project/merimen/'
        path = os.path.join(base, self.user, self.search_item)
        self.path = path
        prefs = {'download.default_directory' : path}
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=options)
        return driver
      
    def login(self):
        user_input = self.driver.find_element(By.ID, "sleUserName")
        pass_input = self.driver.find_element(By.ID, "slePassword")
        if self.user == 'gunsbodyrepair':
            user_input.send_keys("gunsbodyrepair")
            pass_input.send_keys("MERIMEN1234!")
        elif self.user == 'pbs_tio':
            user_input.send_keys("pbs_tio")
            pass_input.send_keys("aditya2162")
        elif '20' in self.user:
            user_input.send_keys("bb_tio")
            pass_input.send_keys("aditya2162")
        pass_input.send_keys(Keys.ENTER)
        # check if login successful
        current_url = self.driver.current_url
        if "https://indonesia.merimen.com/claims/index.cfm?fusebox=MTRroot&fuseaction=dsp_home" not in current_url:
            print('Login failed!')
            self.driver.quit()
        else:
            print('Successfully logged in')

    def search_data(self):
        # search page
        search_input = WebDriverWait(self.driver,timeout=10).until(
            EC.element_to_be_clickable((By.ID, "SRCH")))
        search_input.send_keys(Keys.CONTROL + "a")
        search_input.send_keys(self.search_item)
        search_input.send_keys(Keys.ENTER)

        # list of search result
        print(f'searching {self.search_item}')
        search_result = WebDriverWait(self.driver,timeout=10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, self.search_item)))
        search_result.click()

        # dokumen tab
        dok_tab = WebDriverWait(self.driver,timeout=30).until(
            EC.element_to_be_clickable((By.ID, "ClaimMenu$4")))
        dok_tab.click()

        # dokumen list
        WebDriverWait(self.driver,timeout=10).until(
            EC.presence_of_all_elements_located((By.ID, 'MRMmaintable')))
        print(f'{self.search_item} docs found!')

    def wait_download(self):
        directory_to_watch = self.path

        download_incompleate = True
        while download_incompleate:
            seen_files = os.listdir(directory_to_watch)
            for filename in seen_files:
                if 'crdownload' in filename:
                    time.sleep(3)
                elif 'crdownload' not in filename:
                    download_incompleate = False    

    def rename_files(self, counter):
        directory_to_watch = self.path
        seen_files = os.listdir(directory_to_watch)
        
        for filename in seen_files:
            if '__' not in filename:
                oldfile = os.path.join(directory_to_watch, filename)
                newfile = os.path.join(directory_to_watch, f'{counter+1}__{filename}')
                os.rename(oldfile, newfile)

    def count_files(self):
        table_element = self.driver.find_element(By.ID, 'doclisting')
        element_ids = table_element.find_elements(By.PARTIAL_LINK_TEXT, 'Load')
        print(f'{self.search_item} have {len(element_ids)} docs')
        return element_ids
    
    def download_files(self, element_ids):
        select_element = self.driver.find_element(By.ID, 'SVCDOCVIEW')
        select = Select(select_element)
        select.select_by_value('3')

        for i in range(len(element_ids)):

            element_ids[i].click()
            time.sleep(1)
            self.wait_download()
            self.rename_files(i)

            print(f'Downloading {i+1} of {len(element_ids)}')
        
    def check_previous_download(self):
        if os.path.exists(self.path):
            files = os.listdir(self.path)
            return len(files)
        else:
            os.makedirs(self.path)
            return 0
    
    def delete_downloads(self):
        files = os.listdir(self.path)
        for file in files:
            file_path = os.path.join(self.path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("Old files deleted")
    
    def get_files(self):
        self.driver.get('https://indonesia.merimen.com/claims/index.cfm?skip_browsertest=1')
        self.login()  
        self.search_data()

        element_ids = self.count_files()
        previous_downloaded = self.check_previous_download()
        print(f'Previous downloads: {previous_downloaded}, new downloads: {len(element_ids)}')

        if previous_downloaded < len(element_ids):
            self.delete_downloads()
            self.download_files(element_ids)
        else:
            print('No new files to download')
             
             
if __name__ == "__main__":

    search_values = ["B1677WMM"]

    # with open('plat1.txt', 'r') as f:
    #     data = f.readlines()

    # # # check unfinished search
    # search_values = [item.strip().replace(" ", "") for item in data]
    # unfinished_search = []

    # for i in search_values:
    #     if os.path.exists(f'results/{i}'):
    #         continue
    #     else:
    #         unfinished_search.append(i)
    scraper = Scraper('2024', 'B1677WMM')
    # scraper.get_files(url, 'bb_tio', unfinished_search)
    scraper.get_files()
    # print(unfinished_search)
