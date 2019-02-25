# the script uses requests library to access URLs by default, which only gets static HTML and often gets poor results
# to render the URL with Selenium, run the script with '-js' from the command line
# (requires selenium and the Chrome webdriver, links at https://seleniumhq.github.io/selenium/docs/api/py/index.html#drivers)
# input file for the URL is url.txt, output is emails.csv
try:
    from selenium import webdriver
    NO_SELENIUM = False                 
except ImportError:
    NO_SELENIUM = True
from requests import get                  
from bs4 import BeautifulSoup
import sys
import re

def read_url(file_name):
    with open(file_name) as url_file:
        return url_file.readline()

def get_html_from_url(url, render_js=False):
    response = ''
    if render_js:
        if NO_SELENIUM:
            print('Selenium module not installed!')
        else:
            with webdriver.Chrome() as browser:
                browser.get(url)
                response = browser.page_source
    else: 
        response = get(url).text 
    return response

def find_emails(html):
    parser = 'html.parser'
    soup = BeautifulSoup(html, parser)
    email_list = set()
    email_regex = re.compile(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+")
    tags_with_email = soup.find_all(string=email_regex)
    links_with_email = [link for link in map(str, soup.find_all(href=email_regex))]
    text_with_email = tags_with_email + links_with_email
    for item in text_with_email:
        for email in email_regex.findall(item):
            email_list.add(email)
    return email_list

def write_emails_csv(email_list):
    with open('emails.csv', 'w+') as csvfile:
        for email in email_list:
            csvfile.write(email + '\n')

if __name__ == "__main__":
    args = sys.argv
    url = read_url('url.txt')
    print('URL: {}'.format(url))
    if '-js' in args:
        render_js = True
        print('Rendering with Selenium...')
    else:
        render_js = False
        print('Getting static HTML...')
    html = get_html_from_url(url, render_js=render_js)
    print('Building email address list...')
    email_list = find_emails(html)
    print('Writing email addresses to file...')
    write_emails_csv(email_list)
    print('Done!')