import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os.path
from os import path
import sqlite3


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


meLink = driver.current_url

### product dictionary
# product[0] = name
# product[1] = price
# product[2] = website
# product[3] = link

productA = {}
productCC = {}
productME = {}

############################################################# Amazon Canada #############################################################

print("\nAmazon Prices")
numberA = 0
page = requests.get(amazonLink, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
for elem in soup.find_all("div", {"class" : "s-include-content-margin s-border-bottom"}):
	link = elem.find("a" , {"class" : "a-link-normal a-text-normal"})
	link = link.get('href')
	link = "https://www.amazon.ca" + link
	product = elem.find("a" , {"class" :  "a-link-normal a-text-normal"})
	productName = product.find("span" , {"class" : "a-size-medium a-color-base a-text-normal"})
	Name = productName.get_text().strip()
	priceWhole = elem.find("span" , {"class" : "a-offscreen"})
	price = priceWhole.get_text().strip()
	print(str(numberA) + ": " + Name)
	print(price)
	print(link)
	print()
	productA[numberA] = [Name,price,"AmazonCanada",link]
	numberA += 1
print()

############################################################# Canada Computers #############################################################

print("Canada Computers Prices")

page = requests.get(ccLink, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

numberCC = numberA
for elem in soup.find_all("div" , {"class" : "px-0 col-12 productInfoSearch pt-2"}):
	link = elem.find("a" , {"class" : "text-dark text-truncate_3"})
	link = link.get('href')
	productName = elem.find("span" , {"class" : "text-dark d-block productTemplate_title"}).get_text().strip()
	price = elem.find("span" , {"class" : "d-block mb-0 pq-hdr-product_price line-height"})
	if (price == None):
		price = elem.find("span" , {"class" : "text-danger d-block mb-0 pq-hdr-product_price line-height"})
	realPrice = price.get_text().strip()
	print(str(numberCC) + ": " + productName)
	print(realPrice)
	print(link)
	print()
	productCC[numberCC] = [productName, realPrice, "CanadaComputers",link]
	numberCC += 1
print()
############################################################# Memory Express #############################################################

print("Memory Express Prices")

page = requests.get(meLink,headers=headers)
soup = BeautifulSoup(page.content,'html.parser')

numberME = numberCC
for elem in soup.find_all("div" , {"class" : "c-shca-icon-item"}):
	link = elem.find("a")
	link = link.get('href')
	link = "https://www.memoryexpress.com" + link
	productElem = elem.find("div" , {"class" : "c-shca-icon-item__body-name"})
	productName = productElem.find('a').get_text().strip()
	priceElem = elem.find("div" , {"class" : "c-shca-icon-item__summary"})
	priceVal = priceElem.find("div", {"class": "c-shca-icon-item__summary-list"})
	price = priceVal.find("span").get_text().strip()
	print(str(numberME) + ": " + productName)
	print(price)
	print(link)
	print()
	productME[numberME] = [productName,price,"MemoryExpress",link]
	numberME += 1

driver.quit()

selectedProductNum = input("Which product would you like?(Please enter the number of the product): ")
selectedProductNum = int(selectedProductNum)

### insert values into database

if(path.exists("ProductPrices.db")):
	conn = sqlite3.connect('ProductPrices.db')
	c = conn.cursor()
else:
	createTable = """CREATE TABLE IF NOT EXISTS Products (
                                    ProductName text,
                                    price integer,
                                    website text,
                                    link text
                                );"""
	conn = sqlite3.connect('ProductPrices.db')
	c = conn.cursor()
	c.execute(createTable)


if (selectedProductNum <= numberA):
	c.execute("INSERT INTO Products (ProductName, price, website, link) VALUES(?,?,?,?)",(productA[selectedProductNum][0],productA[selectedProductNum][1],productA[selectedProductNum][2],productA[selectedProductNum][3]))

elif (selectedProductNum <= numberCC and selectedProductNum > numberA):
	c.execute("INSERT INTO Products (ProductName, price, website, link) VALUES(?,?,?,?)",(productCC[selectedProductNum][0],productCC[selectedProductNum][1],productCC[selectedProductNum][2],productCC[selectedProductNum][3]))

elif (selectedProductNum <= numberME and selectedProductNum > numberCC):
	c.execute("INSERT INTO Products (ProductName, price, website, link) VALUES(?,?,?,?)",(productME[selectedProductNum][0],productME[selectedProductNum][1],productME[selectedProductNum][2],productME[selectedProductNum][3]))

conn.commit()
conn.close()
