import requests
import csv
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")


products = soup.find("ul", class_="nav-list")

product_page_url = []
universal_product_code = []
title = []
price_including_max = []
price_excluding_max = []
number_available = []
category = []
review_rating = []
image_url = []

en_tete = ["product_page_url","universal_product_code","title","price_including_max","price_excluding_max","number_available","category","review_rating","image_url"]

h3 = soup.find_all("h3")
for h in h3:
	url = "https://books.toscrape.com/" + h.a["href"]
	product_page_url.append(url)
	page = requests.get(url)
	soup = BeautifulSoup(page.text, "html.parser")
	infos_product = soup.find_all("td")

	universal_product_code.append(infos_product[0].text)
	title.append(soup.find("h1").text)
	price_including_max.append(infos_product[2].text)
	price_excluding_max.append(infos_product[3].text)
	number_available.append(infos_product[5].text)
	category.append(infos_product[1].text)
	review_rating.append(infos_product[6].text)
	image_url.append("https://books.toscrape.com/" + soup.find("img")["src"].strip("../"))

with open("data.csv", "w") as csv.file:
	writer = csv.writer(csv.file, delimiter=",")
	writer.writerow(en_tete)
	for product_page_url, universal_product_code,title, price_including_max, price_excluding_max,number_available, category,review_rating, image_url in zip(product_page_url, universal_product_code,title, price_including_max, price_excluding_max,number_available, category,review_rating, image_url):
		writer.writerow([product_page_url, universal_product_code,title, price_including_max, price_excluding_max,number_available, category,review_rating, image_url])
	



	





	