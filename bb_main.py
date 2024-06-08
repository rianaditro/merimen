from bb_scraper import Scraper

import os


def check_list(folder):
    with open(f'{folder}.txt', 'r') as f:
        data = f.readlines()

    # check unfinished search
    search_values = [item.strip().replace(" ", "") for item in data]
    print(f"{len(search_values)} items in list")
    unfinished_search = []

    for i in search_values:
        if i in unfinished_search:
            print(f"Duplicate found: {i}")
        else:
            unfinished_search.append(i)
       
    return unfinished_search

def download_files(folder):
    search_list = check_list(folder)
    for i, item in enumerate(search_list):
        print(f'{i+1}/{len(search_list)}: {item}')
        try:
            scraper = Scraper(folder, item)
            scraper.get_files()
            scraper.driver.quit()
            del scraper
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    """
    This app loop through every item with its own driver.
    So, if this item download a file, it will download file to the its own folder.
    But this kinda slow.
    For checking or validate the content, kindly re-use the driver and
    save the list so you can download it with the new driver each instance.

    """
    folder = '2023'

    download_files(folder)

