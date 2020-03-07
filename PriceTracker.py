import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import sqlite3

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

# CAN websites

## For Amazon website
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.amazon.ca/")

productName = input("what item: ")

title = productName

text = driver.find_element_by_id("twotabsearchtextbox")
text.send_keys(productName)
text.send_keys(Keys.RETURN)

button = driver.find_element_by_xpath("//a[@class='a-link-normal a-text-normal']")
button.click()

amazonLink = driver.current_url

## For Canada Computers website
driver.get("https://www.canadacomputers.com/index.php")
text = driver.find_element_by_id("cc_quick_search")
text.send_keys(productName)
text.send_keys(Keys.RETURN)

button = driver.find_element_by_xpath("//a[@class='text-dark text-truncate_3']")
button.click()

ccLink = driver.current_url

## For Memory Express website

driver.get("https://www.memoryexpress.com/")
text = driver.find_element_by_name("Search")
text.send_keys(productName)
text.send_keys(Keys.RETURN)

button = driver.find_element_by_xpath("//div[@class='c-shca-icon-item__body-name']")
button.click()

meLink = driver.current_url
## Amazon link

### amazon links
#amazon = ['https://www.amazon.ca/dp/B07B41WS48?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B07XPZMKQ6?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B0143UM4TC?tag=pcp0f-20&linkCode=ogi&th=1&psc=1',
#         'https://www.amazon.ca/dp/B0786QNS9B?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B075QJTBVT?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B07RJGK1PW?tag=pcp0f-20&linkCode=ogi&th=1&psc=1',
#         'https://www.amazon.ca/dp/B071G4KDKG?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B00IUQRPQS?tag=pcp0f-20&linkCode=ogi&th=1&psc=1','https://www.amazon.ca/dp/B00H3T1KBE?tag=pcp0f-20&linkCode=ogi&th=1&psc=1']


print("Amazon price")

page = requests.get(amazonLink, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
priceString = soup.find(id="priceblock_ourprice").get_text()
priceVal = float(priceString[5:])

print(title)
print(priceVal)
print()

print("Canada Computers Prices")

page = requests.get(ccLink, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
priceString = soup.find("span", {"class" : "h2-big"}).get_text()
priceString = priceString[2:-1]

print(title)
print(priceString)
print()

print("Memory Express Prices")

page = requests.get(meLink,headers=headers)
soup = BeautifulSoup(page.content,'html.parser')
price = soup.find("div", {"class" : "GrandTotal c-capr-pricing__grand-total"}).get_text()
price = price[6:]
print(title)
print(price)
print()


# for url in amazon:
#     page = requests.get(url, headers=headers)

#     soup = BeautifulSoup(page.content, 'html.parser')
#     title = soup.find(id="productTitle").get_text()
#     priceString = soup.find(id="priceblock_ourprice").get_text()
#     priceVal = float(priceString[5:])

#     amazonPrices[title.strip()] = priceVal
#     print(title.strip())
#     print(priceString[5:])
# print("END OF AMAZON PRICES\n")

# print("CANADA COMPUTERS PRICES\n")
# ### canada computers
# CC = ['https://www.canadacomputers.com/product_info.php?cPath=4_64&item_id=120458','https://www.canadacomputers.com/product_info.php?cPath=26_1832_1833&item_id=140922','https://www.canadacomputers.com/product_info.php?cPath=24_311_1326&item_id=096846'
#       'https://www.canadacomputers.com/product_info.php?cPath=179_1927_1928&item_id=120759','https://www.canadacomputers.com/product_info.php?cPath=15_1086_210&item_id=132494','https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=137857',
#       'https://www.canadacomputers.com/product_info.php?cPath=6_112&item_id=108444']

# for url in CC:
#     page = requests.get(url, headers=headers)
#     soup = BeautifulSoup(page.content,'html.parser')
#     title = soup.find("h1", {"class" : "h3 product-title mb-2"}).get_text()
#     price = soup.find("span", {"class" : "h2-big"}).get_text()

#     canadaComputersPrices[title.strip()] = float(price[2:-1])
#     print(title.strip())
#     print(price)
# print("END OF CANADA COMPUTER PRICES\n")

# ### memory express
# ME = ['https://www.memoryexpress.com/Products/MX78787','https://www.memoryexpress.com/Products/MX61227','https://www.memoryexpress.com/Products/MX76126','https://www.memoryexpress.com/Products/MX77286','https://www.memoryexpress.com/Products/MX70610',
#       'https://ca.pcpartpicker.com/mr/memoryexpress/cXg323']

# print("MEMORY EXPRESS PRICES\n")
# for url in ME:
#     page = requests.get(url,headers=headers)
#     soup = BeautifulSoup(page.content,'html.parser')
#     title = soup.find("h1").get_text()
#     price = soup.find("div", {"class" : "GrandTotal c-capr-pricing__grand-total"}).get_text()

#     memoryExpressPrices[title.strip()] = price[7:-15]
#     print(title.strip())
#     print(price[6:])
# print("END OF MEMORY EXPRESS PRICES\n")

# print(amazonPrices)
# print('\n')
# print(canadaComputersPrices)
# print('\n')
# print(memoryExpressPrices)


### insert values into database
# conn = sqlite3.connect('ProductPrices.db')

# c = conn.cursor()

