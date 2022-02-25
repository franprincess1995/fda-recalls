from bs4 import BeautifulSoup
import requests 
import os
import re


data_dir = os.environ['DATA_DIR']

def main():
    download_recall_pages()



def download_recall_pages():
    url = "https://www.fda.gov/medical-devices/medical-device-recalls/2022-medical-device-recalls"
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    page_links = gather_links(soup)
    scrape_recall_pages(page_links)



def gather_links(soup):
    all_links=[]
    for link in soup.find_all('a', href=re.compile('^/medical-devices/medical-device-recalls/'), attrs ={'data-entity-substitution' :'canonical'}):
        all_links.append("https://www.fda.gov" + link.get('href'))
    return all_links 



def scrape_recall_pages(page_links):
    for page_link in page_links:
        response = requests.get(page_link).text
        file_name = page_link.split('/')[-1] + '.html'
        raw_DIR = data_dir + '/raw/'
        with open(raw_DIR + file_name, 'w') as f:
            f.write(response)



if __name__ == '__main__':
    main()


    #for link in soup.find('a', href=re.compile('^/medical-devices/medical-device-recalls/'), attrs ={'data-entity-substitution' :'canonical'}):
