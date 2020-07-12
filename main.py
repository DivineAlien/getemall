from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import re
import requests
from tqdm import tqdm



###########################################
#   definging the functions and variables
###########################################



# first we need to serach the links in webpage
# so here is the scrapper part of the program

def get_links(page_url: str, pattern: str):

    links = []

    http = httplib2.Http()

    status, page = http.request(page_url)

    body = BeautifulSoup(page, features="html.parser", parse_only=SoupStrainer('body'))
    
    for link_element in body.findChildren():

        download_link = None

        if link_element.has_attr('href'):
            download_link = link_element.get('href')
        elif link_element.has_attr('src'):
            download_link = link_element.get('src')
        else:
            pass

        if download_link is not None and re.match(pattern, download_link):
            links.append(download_link)
    
    for l in links:
        yield l



# after generating the links for download we need to download them
# so here is the program for download files and write them in out filesystem

DOWNLOAD_PATH = './downloads/'

def get_file_info(file_url: str):

    description = file_url.split('/')[-1]
    file_with_path = '{}{}'.format(DOWNLOAD_PATH, description)
    return (file_url, file_with_path, description)


def download(file_url: str, file: str, description: str):

    try:
        response = requests.get(file_url, stream=True)
        with tqdm.wrapattr(open(file, "wb"), "write",
                        miniters=1, desc=description[:20],
                        total=int(response.headers.get('content-length', 0))) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)

    except Exception as identifier:
        print(identifier)
        print("downlad failed")
    
    else:
        print('{}... successfully downloaded'.format(description[:20]))



# so here we assemble the functions and get the links of files then downloading them
def start():

    # sample_url = 'http://wallpaperswide.com/'
    # sample_pattern = '.*jpg'
    files_url = input('please enter your webpage url: \n')
    files_pattern = input('please enter regex match: \n')

    generated_links = get_links(files_url, files_pattern)

    for link in generated_links:
        download(*get_file_info(link))





########################################################
#               starting the app
########################################################

start()