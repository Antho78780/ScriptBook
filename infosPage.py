import requests
import csv
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

urlAccueil = "https://books.toscrape.com/"
pageAccueil = requests.get(urlAccueil)
soup = BeautifulSoup(pageAccueil.content, "html.parser")

product_page_url = []
universal_product_code = []
title = []
price_including_max = []
price_excluding_max = []
number_available = []
category = []
review_rating = []
image_url = []
product_description = []
en_tete = ["product_page_url","universal_product_code","title","price_including_max","price_excluding_max","number_available","category","review_rating","image_url", "product_description"]

for li in soup.find("ul", class_="nav-list").ul.find_all("li"):
	a = li.a.get("href")
	urlCategory = "https://books.toscrape.com/" + a
	pageCategory = requests.get(urlCategory)
	soupCategory = BeautifulSoup(pageCategory.content, "html.parser")
	allh3 = soupCategory.find_all("h3")
	
	for h3 in allh3:
		linkBook = h3.a.get("href").strip("../")
		urlBook = "https://books.toscrape.com/catalogue/" + linkBook
		pageBook = requests.get(urlBook)
		soupBook = BeautifulSoup(pageBook.content, "html.parser")

		linkImg = soupBook.img.get("src").strip("../")
		description = soupBook.find("article", class_="product_page").find_all("p")[3].get_text()
		categoryBook = soupBook.find("ul", class_="breadcrumb").find_all("li")[2].a.get_text()
		td = soupBook.find_all("td")

		product_page_url.append(urlBook)
		universal_product_code.append(td[0].get_text())
		title.append(soupBook.find("h1").get_text())
		price_including_max.append(td[2].get_text())
		price_excluding_max.append(td[3].get_text())
		category.append(categoryBook)
		number_available.append(td[5].get_text())
		review_rating.append(td[6].get_text())
		image_url.append("https://books.toscrape.com/" + linkImg)
		product_description.append(description)
		
	
	next = soupCategory.find("li", class_="next")
	if next:
		for i in range(2,9):
			urlPageNext = "https://books.toscrape.com/" + a.strip("index.html") + "page-" + str(i) + ".html"
			pageNext = requests.get(urlPageNext)
			if pageNext: 
				soupPageNext = BeautifulSoup(pageNext.content, "html.parser")
				allh3 = soupPageNext.find_all("h3")
				
				for h3 in allh3:
					urlNextBook = h3.a.get("href").strip("../")
					urlNextBook = "https://books.toscrape.com/catalogue/" + urlNextBook
					pageNextBook = requests.get(urlNextBook)
					soupNextBook = BeautifulSoup(pageNextBook.content, "html.parser")

					linkNextImgBook = soupNextBook.img.get("src").strip("../")
					descriptionNextBook = soupNextBook.find("article", class_="product_page").find_all("p")[3].get_text()
					categoryNextBook = soupNextBook.find("ul", class_="breadcrumb").find_all("li")[2].a.get_text()
					td = soupNextBook.find_all("td")

					product_page_url.append(urlNextBook)
					universal_product_code.append(td[0].get_text())
					title.append(soupNextBook.find("h1").get_text())
					price_including_max.append(td[2].get_text())
					price_excluding_max.append(td[3].get_text())
					category.append(categoryNextBook)
					number_available.append(td[5].get_text())
					review_rating.append(td[6].get_text())
					image_url.append("https://books.toscrape.com/" + linkNextImgBook)
					product_description.append(descriptionNextBook)
	for i in tqdm(product_page_url):
		time.sleep(0.1)		
			
with open("data.csv","w", encoding="utf-8") as csv.file:
	writer = csv.writer(csv.file, delimiter=",")
	writer.writerow(en_tete)
	for product_page_url, universal_product_code, title, price_including_max, price_excluding_max, number_available, category, review_rating, image_url, product_description in zip(product_page_url, universal_product_code, title, price_including_max, price_excluding_max, number_available, category, review_rating, image_url, product_description):
		writer.writerow([product_page_url, universal_product_code, title, price_including_max, price_excluding_max, number_available, category, review_rating, image_url, product_description])

	