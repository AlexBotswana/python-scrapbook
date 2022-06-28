from re import split
from jmespath import search
import requests
from bs4 import BeautifulSoup
import csv


mapping_number = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four" :4, "Five": 5}


	

def extract_book_data(book_url):

	response = requests.get(book_url)
	html_book_page = response.content

	# transforme (parse) le HTML en objet BeautifulSoup
	soup_book_page = BeautifulSoup(html_book_page, "html.parser")

	# récupération des informations suivantes : product_page_url (product_url) ,  , , image_url
	# title
	title = soup_book_page.find("h1").get_text()
	
	# Data in table-striped : universal_ product_code (upc), price_including_tax, price_excluding_tax, number_available, 
	table = soup_book_page.find("table", {"class": "table table-striped"})
	for row in table.find_all("tr"):
		th = row.find("th").get_text()
		td = row.find("td").get_text()
        # UPC
		if "UPC" in th:
			upc = td
        # price without tax
		if "Price (excl. tax)" in th:
			price_excluding_tax = td
        # price with tax
		if "Price (incl. tax)" in th:
			price_including_tax = td
        # stock
		if "Availability" in th:
			stock = td
	
	# product_description
	product_descpt_bs = soup_book_page.find_all("p")
	product_descpt_list = []
	for product_descpt in product_descpt_bs:
		product_descpt_list.append(product_descpt.text)
	
	#review_rating
	rating_bs = soup_book_page.find("p", {"class": "star-rating"})
	rating = str(rating_bs).split("\n")[0]
	rating = rating.replace('<p class="star-rating ', "").replace('">', "")
	rating = mapping_number[rating]
	
	# category
	product_category_bs = soup_book_page.find_all("a", href="../category/books/poetry_23/index.html")
	product_category_list = []
	for product_category in product_category_bs:
		product_category_list.append(product_category.text)
	
	# image url
	url_img_bs = soup_book_page.img["src"]
	url_site_root = "http://books.toscrap.com/"
	url_img = url_site_root + url_img_bs.replace("../", "")
	
	print(book_url)
	print(upc)
	print(price_excluding_tax)
	print(price_including_tax)
	print(stock)
	print(title)
	print(product_descpt_list[3])
	print(product_category_list[0])
	print(rating)
	print(url_img)



	#write in csv file
	# universal_ product_code (upc) = product_data_td_list[0], 
	# price_including_tax = product_data_td_list[3], 
	# price_excluding_tax = product_data_td_list [2], 
	# number_available = product_data_td_list[5], 

	en_tete = ['product_page_url','universal_ product_code (upc)','title','price_including_tax','price_excluding_tax', 'number_available', 'product description', 'category', 'review_rating', 'image_url']
	with open('../scrapbook/data.csv', 'w') as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow(en_tete)
		writer.writerow([book_url, upc, title, price_including_tax, price_excluding_tax, stock, product_descpt_list[3], product_category_list[0], rating, url_img])



#lien du site à scraper
responde_category = requests.get("http://books.toscrape.com/catalogue/category/books_1/index.html")
home_category_page = responde_category.content
soup_home_category_page = BeautifulSoup(home_category_page, "html.parser")

#product_url = "http://books.toscrape.com/catalogue/the-black-maria_991/index.html"
book_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
extract_book_data(book_url)