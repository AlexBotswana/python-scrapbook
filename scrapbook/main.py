#from inspect import classify_class_attrs
import requests
from bs4 import BeautifulSoup
import csv

#lien du site à scraper
product_url = "http://books.toscrape.com/catalogue/the-black-maria_991/index.html"
response = requests.get(product_url)
home_product_page = response.content

# affiche la page HTML
#print(home_page)

# transforme (parse) le HTML en objet BeautifulSoup
soup_home_product_page = BeautifulSoup(home_product_page, "html.parser")

# récupération des informations suivantes : product_page_url (product_url) ,  , , image_url

# Data in <td> : universal_ product_code (upc), price_including_tax, price_excluding_tax, number_available, 
product_data_td_bs = soup_home_product_page.find_all("td")

# title
product_title_bs = soup_home_product_page.find_all("h1")

# product_description
product_descpt_bs = soup_home_product_page.find_all("p")

# category
product_category_bs = soup_home_product_page.find_all("a", href="../category/books/poetry_23/index.html")

#review_rating
#product_review_rating_bs = soup_home_product_page.find_all("p", class_="star-rating Three")

# image url
product_url_img_bs = soup_home_product_page.find_all("img")

product_title_list = []
for product_title in product_title_bs:
	product_title_list.append(product_title.string)

product_data_td_list = []
for product_data_td in product_data_td_bs:
	product_data_td_list.append(product_data_td)

product_descpt_list = []
for product_descpt in product_descpt_bs:
	product_descpt_list.append(product_descpt)

product_category_list = []
for product_category in product_category_bs:
	product_category_list.append(product_category)

#product_review_rating_list = []
#for product_review_rating in product_review_rating_bs:
#	product_review_rating_list.append(product_review_rating)

product_url_img_list = []
for product_url_img in product_url_img_bs:
	product_url_img_list.append(product_url_img)

print(product_data_td_list)

print(product_title_list[0])
print(product_descpt_list[3])

print(product_category_list[0])
#print(product_review_rating_list)
print(product_url_img_list[0])



#write in csv file
# universal_ product_code (upc) = product_data_td_list[0], 
# price_including_tax = product_data_td_list[3], 
# price_excluding_tax = product_data_td_list [2], 
# number_available = product_data_td_list[5], 
# review_rating = product_data_td_list [6] 

en_tete = ['product_page_url','universal_ product_code (upc)','title','price_including_tax','price_excluding_tax', 'number_available', 'product description', 'category', 'review_rating', 'image_url']
with open('../scrapbook/data.csv', 'w') as csv_file:
	writer = csv.writer(csv_file, delimiter=',')
	writer.writerow(en_tete)
	writer.writerow([product_url, product_data_td_list[0], product_title_list[0], product_data_td_list[3], product_data_td_list[2], product_data_td_list[5], product_descpt_list[3], product_category_list, product_data_td_list[6], product_url_img_list])
