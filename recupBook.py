import requests
import csv
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

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
product_description = []
en_tete = [
    "product_page_url", "universal_product_code", "title", "price_including_max", "price_excluding_max",
    "number_available", "category", "review_rating", "image_url", "product_description"
]


def urlSoup(u):
    pageUrl = requests.get(u)
    soupPage = BeautifulSoup(pageUrl.content, "html.parser")
    urlImg = soupPage.img.get("src").strip("../")
    descriptionBook = soupPage.find("article", class_="product_page").find_all("p")[3].get_text()
    categoryBook = soupPage.find("ul", class_="breadcrumb").find_all("li")[2].a.get_text()
    td = soupPage.find_all("td")

    product_page_url.append(u)
    universal_product_code.append(td[0].get_text())
    title.append(soupPage.find("h1").get_text())
    price_including_max.append(td[2].get_text())
    price_excluding_max.append(td[3].get_text())
    category.append(categoryBook)
    number_available.append(td[5].get_text())
    review_rating.append(td[6].get_text())
    image_url.append("https://books.toscrape.com/" + urlImg)
    product_description.append(descriptionBook)


for li in soup.find("ul", class_="nav-list").ul.find_all("li"):
    a = li.a.get("href")
    url = "https://books.toscrape.com/" + a
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    allh3 = soup.find_all("h3")
    for h3 in allh3:
        urlBook = h3.a.get("href").strip("../")
        url = "https://books.toscrape.com/catalogue/" + urlBook
        urlSoup(url)
    next = soup.find("li", class_="next")
    if next:
        for i in range(2, 9):
            url = "https://books.toscrape.com/" + a.strip("index.html") + "page-" + str(i) + ".html"
            page = requests.get(url)
            if page:
                soup = BeautifulSoup(page.content, "html.parser")
                allh3 = soup.find_all("h3")

                for h3 in allh3:
                    urlNextBook = h3.a.get("href").strip("../")
                    url = "https://books.toscrape.com/catalogue/" + urlNextBook
                    urlSoup(url)

for i in tqdm(product_page_url):
    time.sleep(0.1)

with open("data.csv", "w", encoding="utf-8") as fileCsv:
    writer = csv.writer(fileCsv, delimiter=",")
    writer.writerow(en_tete)

    for ppu, upc, t, pim, pxm, na, c, rr, iu, pd, in zip(
            product_page_url, universal_product_code, title, price_including_max, price_excluding_max, number_available,
            category, review_rating, image_url, product_description
    ):
        writer.writerow([ppu, upc, t, pim, pxm, na, c, rr, iu, pd])



