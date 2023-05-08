from googlesearch import search
from tkinter import simpledialog
import time
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Use google search engine and get urls based on specified query
def get_websites_urls(query):
    websites = [url for url in search(query,  num_results=80)]
    return websites

def search_url_for_content(url) -> dict:
    page_url = url
    web_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:       
        page_data = requests.get(page_url, headers=web_headers)
        page_html = str(page_data.content)    
        phones = ' ,'.join(str(item) for item in get_phones(page_html))
        mails = ' ,'.join(str(item) for item in get_emails(page_html))
        head_name = get_website_title(page_html)
        return {"company name" : head_name, "website" : url, "phones" : [phones], "mails" : [mails]}
    except:
        return {"company name" : "unable to access webstie", "website" : url, "phones" : [], "mails" : []}
def get_phones(html_page_content) -> list:

    phone_regex = re.compile(r'''(
                        (\d{3}|\(\d{3}\))? 
                        (\s|-|\.)?
                        (\d{3})
                        (\s|-|\.)
                        (\d{4})
                        (\s*(ext|x|ext.)\s*(\d{2,5}))?)''', re.VERBOSE)

    phones_content_list = [element for tup in phone_regex.findall(html_page_content) for element in tup]
    phone_content_list_unique = list(set(item for item in phones_content_list if len(item) >= 7)) 
    return phone_content_list_unique

def get_emails(html_page_content) -> list:
    email_regex = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+' )
    emails_content_list = email_regex.findall(html_page_content)
    return emails_content_list

# Below function is used to extract title which is usualy company name
def get_website_title(site_content) -> str:
    soup = BeautifulSoup(site_content, 'html.parser')
    try:
        title = soup.find_all('title')[0].get_text()
    except IndexError:
        title = "not found"
    return title

def main():
    query = simpledialog.askstring("New Item", "Enter name of item:")
    urls = get_websites_urls(query)
    report_df = pd.DataFrame(columns=["company name", "website", "phones", "mails"])
    for url in urls:
        df_row = search_url_for_content(url)
        report_df = pd.concat([report_df, pd.DataFrame(df_row)])
    
    #print(report_df)
    report_df.to_excel("Report.xlsx")


if __name__ == "__main__":
    main()    