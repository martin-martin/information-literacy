import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# --------------------------------------------------------------------
# ------------------- ENTER THE VARIABLES ----------------------------
# --------------------------------------------------------------------
chrome_path = "/Users/martin/Documents/projects/information_literacy/chromedriver"
start_url = "https://scholar.google.com/"
keys = "sustainability concept"
# --------------------------------------------------------------------

# accessing the first page and entering the search query
driver = webdriver.Chrome(executable_path=chrome_path)
driver.get(start_url)
try:
    input_element = driver.find_element_by_xpath('//*[@id="gs_hdr_tsi"]')
    input_element.send_keys(keys)
    input_element.send_keys(Keys.ENTER)

    # finding the nav element that holds results on further pages
    nav_elem = driver.find_element_by_id('gs_n')
    nav_links = nav_elem.find_elements_by_xpath('//a')
    page_links = [li.get_attribute("href") for li in nav_links
                    if li.get_attribute("href").startswith('https://scholar.google')]
except Exception as e:
    print(e)
    time.sleep(10)

#print(page_links)

def get_article_links(driver, url):
    driver.get(url)
    article_links = []
    try:
        # finding all the link containers that hold publication links
        html_links = driver.find_elements_by_class_name('gs_rt')
        for elem in html_links:
            # inside of those elements, get the link out of there
            link = elem.find_element_by_xpath('.//a')
            # adding only the URL of the page to our URL list
            article_links.append(link.get_attribute("href"))
    except NoSuchElementException:
        print('probably sign-in issues')
    except Exception as e:
        print(e)
    return article_links

# collecting all article links into one big list
all_article_links = []
# initial page

all_article_links.extend(get_article_links(driver, start_url))
# all the pagination
for url in page_links:
    # print(url)
    all_article_links.extend(get_article_links(driver, url))

with open(f"{keys.replace(' ', '_')}.json", 'w') as f:
    json.dump(all_article_links, f)
