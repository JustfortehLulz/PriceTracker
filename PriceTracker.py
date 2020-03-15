import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#import sqlite3

# skip sponsored products 

ok = []

productName = input("what item: ")

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

driver = webdriver.Chrome()
driver.maximize_window()

title = productName

# CAN websites

## For Amazon website

driver.get("https://www.amazon.ca/")

text = driver.find_element_by_id("twotabsearchtextbox")
text.send_keys(productName)
text.send_keys(Keys.RETURN)

amazonLink = driver.current_url

## For Canada Computers website
driver.get("https://www.canadacomputers.com/index.php")
text = driver.find_element_by_id("cc_quick_search")
text.send_keys(productName)
text.send_keys(Keys.RETURN)

ccLink = driver.current_url

## For Memory Express website

driver.get("https://www.memoryexpress.com/")
text = driver.find_element_by_name("Search")
text.send_keys(productName)
text.send_keys(Keys.RETURN)

#button = driver.find_element_by_xpath("//div[@class='c-shca-icon-item__body-name']")
#button.click()

meLink = driver.current_url
## Amazon link

### amazon links
#amazon = ['https://www.amazon.ca/dp/B07B41WS48?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B07XPZMKQ6?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B0143UM4TC?tag=pcp0f-20&linkCode=ogi&th=1&psc=1',
#         'https://www.amazon.ca/dp/B0786QNS9B?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B075QJTBVT?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B07RJGK1PW?tag=pcp0f-20&linkCode=ogi&th=1&psc=1',
#         'https://www.amazon.ca/dp/B071G4KDKG?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B00IUQRPQS?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B00H3T1KBE?tag=pcp0f-20&linkCode=ogi&th=1&psc=1']


print("Amazon price")

page = requests.get(amazonLink, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
for elem in soup.find_all("div", {"class" : "s-include-content-margin s-border-bottom"}):
	product = elem.find("a" , {"class" :  "a-link-normal a-text-normal"})
	productName = product.find("span" , {"class" : "a-size-medium a-color-base a-text-normal"})
	priceWhole = elem.find("span" , {"class" : "a-offscreen"}).get_text().strip()
	# priceFraction = elem.find("span" , {"class" : "a-price-fraction"}).get_text().strip()
	print(productName.get_text().strip())
	print(priceWhole)

print()


print("Canada Computers Prices")

page = requests.get(ccLink, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

number = 1
for elem in soup.find_all("div" , {"class" : "px-0 col-12 productInfoSearch pt-2"}):
	productName = elem.find("span" , {"class" : "text-dark d-block productTemplate_title"}).get_text().strip()
	price = elem.find("span" , {"class" : "d-block mb-0 pq-hdr-product_price line-height"})
	if (price == None):
		price = elem.find("span" , {"class" : "text-danger d-block mb-0 pq-hdr-product_price line-height"})
	print(productName)
	print(price.get_text().strip())
	# productName = elem.find("span" , {"class" : "text-dark d-block productTemplate_title"}).get_text().strip()
	# price = elem.find("span" , {"class" : "d-block mb-0 pq-hdr-product_price line-height"}).get_text().strip()
	# print(productName)
	# print(price)
# titleCC = soup.find("h1", {"class" : "h3 product-title mb-2"}).get_text().strip()
# priceString = soup.find("span", {"class" : "h2-big"}).get_text()
# priceString = priceString[2:-1]

#print(titleCC)
#print(priceString)
print()
############################################################# Memory Express

productsME = []
pricesME = []

print("Memory Express Prices")

page = requests.get(meLink,headers=headers)
soup = BeautifulSoup(page.content,'html.parser')

### grabs the entire list of products with similar name
### selects a number 
# for elem in soup.find_all("div",{"class" : "c-shca-icon-item__body-name"}):
# 	print(elem.find('a')['href'])
# 	print(str(number) + ": " + elem.find('a').get_text().strip())

# for elem in soup.find_all("div", {"class": "c-shca-icon-item__summary-list"}):
# 	print(elem.find("span").get_text().strip())
number = 1
for elem in soup.find_all("div" , {"class" : "c-shca-icon-item"}):
	#print(elem.find("span").get_text().strip())
	productName = elem.find("div" , {"class" : "c-shca-icon-item__body-name"})
	
	priceElem = elem.find("div" , {"class" : "c-shca-icon-item__summary"})
	price = priceElem.find("div", {"class": "c-shca-icon-item__summary-list"})
	print(str(number) + ": " + productName.find('a').get_text().strip() + " " + price.find("span").get_text().strip())
	print()
	number += 1

driver.quit()


### insert values into database
# conn = sqlite3.connect('ProductPrices.db')

# c = conn.cursor()

