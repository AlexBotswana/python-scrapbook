import requests
from bs4 import BeautifulSoup
import csv

#lien du site à scraper
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
reponse = requests.get(url)
page_accueil = reponse.content

# affiche la page HTML
print(page_accueil)

# transforme (parse) le HTML en objet BeautifulSoup
soup_page_accueil = BeautifulSoup(page_accueil, "html.parser")

# récupération des informations suivantes : product_page_url, universal_ product_code (upc), title, price_including_tax, 
# price_excluding_tax, number_available, product_description, category, review_rating, image_url
product_page_url_bs = soup_page_accueil.find_all("article", class_="product_pod")
product_page_url = []
for Product_page in product_page_url_bs:
	product_page_url.append(Product_page.string)


