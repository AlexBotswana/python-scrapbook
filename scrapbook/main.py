import requests
from bs4 import BeautifulSoup
import csv

#lien du site à scraper
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
home_page = response.content

# affiche la page HTML
print(home_page)

# transforme (parse) le HTML en objet BeautifulSoup
soup_home_page = BeautifulSoup(home_page, "html.parser")

# récupération des informations suivantes : product_page_url, universal_ product_code (upc), title, price_including_tax, 
# price_excluding_tax, number_available, product_description, category, review_rating, image_url
product_title_bs = soup_home_page.find_all("title")
product_title_list = []
for Product_title in product_title_bs:
	product_title_list.append(Product_title.string)

product_descript_bs = soup_home_page.find_all("description")
product_descript_list = []
for Product_descript in product_descript_bs:
	product_descript_list.append(Product_descript.string)

#write in csv file
en_tete = ['Titre', 'Description']
with open('data.csv', 'w') as csv_file:
	writer = csv.writer(csv_file, delimiter=',')
	writer.writerow(en_tete)
	for titre, descript in zip(product_title_list, product_descript_list):
		writer.writerow([titre, descript])
