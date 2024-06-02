import os

from scraper import Scraper


def check_list(filename, user):
    with open(filename, 'r') as f:
        data = f.readlines()

    # check unfinished search
    search_values = [item.strip().replace(" ", "") for item in data]    
    unfinished_search = []

    for i in search_values:
        if os.path.exists(f'{user}/{i}'):
            continue
        else:
            unfinished_search.append(i)
    return unfinished_search


if __name__ == "__main__":
    url = "https://indonesia.merimen.com/claims/index.cfm?skip_browsertest=1&"

    user = 'pbs_tio'
    filename = 'pb_tio.txt'

    # user = 'results'
    # filename = 'plat1.txt'

    scraper = Scraper()
    unfinished_search = check_list(filename, user)
    # print(unfinished_search)
    scraper.get_files(url, user, unfinished_search)

