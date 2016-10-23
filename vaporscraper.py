from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import mechanize
import csv

browser = webdriver.Chrome()

br = mechanize.Browser()

br.set_handle_robots(False)

br.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")] 

csvwriter = csv.writer(file('final.csv', 'wb'))
csvwriter.writerow(['Product Name', 'Price', 'Rating', 'Product Detail', 'Product Link', 'Category'])

def scrape_individual_product(each_product, product_cat):

    try:
        product_name = each_product.find_element_by_class_name("title").text
        product_name = product_name.encode('utf-8')
        print product_name
    except:
        product_name = ""

    try:
        product_price = each_product.find_element_by_class_name("price").text
        print product_price
    except:
        product_price = ""

    try:
        rating_span = each_product.find_element_by_class_name("spr-badge")
        product_rating = rating_span.get_attribute("data-rating")
        print product_rating
    except:
        product_rating = ""

    try:
        product_link_a = each_product.find_element_by_tag_name('a')
        product_link = product_link_a.get_attribute('href')
        print product_link
        product_page = br.open(product_link)
        soup = BeautifulSoup(product_page)
        product_details_div = soup.find_all('div', attrs={'class':'description'})
        product_detail = product_details_div[0]
        product_detail = product_detail.text
        product_detail = product_detail.encode('utf-8')
        print product_detail
        
    except:
        print "inside except product ingredients"
        product_link = ""
        product_detail = ""
        
    to_write = [product_name, product_price, product_rating, product_detail, product_link, product_cat]
    csvwriter.writerow(to_write)
        
    

def scrape_category(each_url):
    try:
        product_cat = each_url.split('collections/')[-1]
    except:
        product_cat = ""

    browser.get(each_url)
    time.sleep(7)
    try:
        age_verification_button = browser.find_element_by_id("submit_birthdate")
        age_verification_button.click()
    except:
        print "already verified age"
    time.sleep(3)
    all_contents = browser.find_elements_by_class_name("sixteen")[-1]
    all_even_product_divs = all_contents.find_elements_by_class_name("even")
    all_odd_product_divs = all_contents.find_elements_by_class_name("odd")
    for each_even in all_even_product_divs:
        scrape_individual_product(each_even, product_cat)
    for each_odd in all_odd_product_divs:
        scrape_individual_product(each_odd, product_cat)
    
def main(urls):
    for each_url in urls:
        scrape_category(each_url)



if __name__ == '__main__':
    urls = ['http://www.vapo.co.nz/collections/electronic-cigarettes-nz',
'http://www.vapo.co.nz/collections/parts',
'http://www.vapo.co.nz/collections/accessories',
'http://www.vapo.co.nz/collections/advanced-kits',
'http://www.vapo.co.nz/collections/mods',
'http://www.vapo.co.nz/collections/mechanical-mods',
'http://www.vapo.co.nz/collections/tanks',
'http://www.vapo.co.nz/collections/coils',
'http://www.vapo.co.nz/collections/rdas',
'http://www.vapo.co.nz/collections/cotton-coil-and-wire',
'http://www.vapo.co.nz/collections/batteries-and-chargers',
'http://www.vapo.co.nz/collections/advanced-accessories',
'http://www.vapo.co.nz/collections/vapo-e-juice',
'http://www.vapo.co.nz/collections/velvet-cloud-vapor-100-vg',
'http://www.vapo.co.nz/collections/flavour-concentrates-for-vaping',
'http://www.vapo.co.nz/collections/vg-pg',
'http://www.vapo.co.nz/collections/sweetner']
    main(urls)
