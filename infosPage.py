import requests
import csv
from bs4 import BeautifulSoup
import time

url = "https://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

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

for a in soup.find("ul", class_="nav-list").find("ul").find_all("a"):
	urlAccueil = "https://books.toscrape.com/" + a["href"]
	pageAccueil = requests.get(urlAccueil)
	soup = BeautifulSoup(pageAccueil.content, "html.parser")
	h3All = soup.find_all("h3")
	next = soup.find("li", class_="next")
	print(next)

	for h3 in h3All:
		urlBook = "https://books.toscrape.com/catalogue/" + h3.find("a")["href"].strip("../")
		pageBook = requests.get(urlBook)
		soup = BeautifulSoup(pageBook.content, "html.parser")
		print(urlBook)

		td = soup.find_all("td")
		product_page_url.append(urlBook)
		universal_product_code.append(td[0].text)
		title.append(soup.find("h1").text)
		price_including_max.append(td[2].text)
		price_excluding_max.append(td[3].text)
		category.append(soup.find("ul", class_="breadcrumb").find_all("a")[2].text)
		number_available.append(td[5].text)
		review_rating.append(td[6].text)
		image_url.append("https://books.toscrape.com/" + soup.find("img")["src"].strip("../"))
	"""
	while next:
		urlNextPage = "https://books.toscrape.com/" + a["href"].strip("index.html") +  next.find("a")["href"]
		pageNext = requests.get(urlNextPage)
		soup = BeautifulSoup(pageNext.content, "html.parser")
		
		for h3 in h3All:
			urlBookNext = "https://books.toscrape.com/catalogue/" + h3.find("a")["href"].strip("../")
			pageBookNext = requests.get(urlBookNext)
			soup = BeautifulSoup(pageBookNext.content, "html.parser")
		
			td = soup.find_all("td")
			product_page_url.append(urlBookNext)
			universal_product_code.append(td[0].text)
			title.append(soup.find("h1").text)
			price_including_max.append(td[2].text)
			price_excluding_max.append(td[3].text)
			category.append(soup.find("ul", class_="breadcrumb").find_all("a")[2].text)
			number_available.append(td[5].text)
			review_rating.append(td[6].text)
			image_url.append("https://books.toscrape.com/" + soup.find("img")["src"].strip("../"))
		"""
"""
with open("data.csv","w") as csv.file:
	writer = csv.writer(csv.file, delimiter=",")
	writer.writerow(en_tete)
	for product_page_url, universal_product_code, title, price_including_max, price_excluding_max, number_available, category, review_rating, image_url in zip(product_page_url, universal_product_code, title, price_including_max, price_excluding_max, number_available, category, review_rating, image_url):
		writer.writerow([product_page_url, universal_product_code, title, price_including_max, price_excluding_max, number_available, category, review_rating, image_url])
"""

	