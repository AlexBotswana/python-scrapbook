from dataclasses import replace
import requests
from bs4 import BeautifulSoup
import csv
import urllib.request
import unicodedata


mapping_number = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four" :4, "Five": 5}

def get_url_categories(url: str) -> list:
    """Return a list of the categories's urls."""
    urls = []
    request = requests.get(url)
    html = request.content
    soup = BeautifulSoup(html, features="html.parser")
    soup_category = soup.find("ul", "nav nav-list").ul
    soup_category = soup_category.find_all("li")
    for url_category in soup_category:
        urls.append(url_category.a["href"])
    return urls

def get_url_books(url):
    """Return a list of the books's urls of 1 category."""
    urls_books = []
    request = requests.get(url)
    html = request.content
    soup = BeautifulSoup(html, features="html.parser")
    soup_books = soup.find_all("article", "product_pod")

    category = soup.find("h1").get_text()

    for book_href in soup_books:
        url_book = book_href.a["href"].replace("../", "")
        urls_books.append(url_book)

    next_page = soup.find("li", "next")
    url = url.replace("index.html", "")
    while next_page:
        url_next_page = url + next_page.a["href"]
        request = requests.get(url_next_page)
        html = request.content
        soup = BeautifulSoup(html, features="html.parser")
        soup_books = soup.find_all("article", "product_pod")
        for book_href in soup_books:
            url_book = book_href.a["href"].replace("../", "")
            urls_books.append(url_book)
        next_page = soup.find("li", "next")
    return urls_books, category	

def extract_book_data(book_url):

    # to register book's datas for csv file
    booking = {
    "title": 0,
    "url": 1,
    "upc": 2,
    "price_including_tax": 3,
    "price_excluding_tax": 4,
    "description": 5,
    "category": 6,
    "stock": 7,
    "review_rating": 8,
    "image_url": 9
    }

    response = requests.get(book_url)
    html_book_page = response.content
    
    
	# transforme (parse) le HTML en objet BeautifulSoup
    soup_book_page = BeautifulSoup(html_book_page, "html.parser")

	# title
    title_book = soup_book_page.find("h1").get_text()
    booking["title"] = unicodedata.normalize('NFC', title_book).encode("ascii", "ignore").decode()
    
    # Data in table-striped : universal_ product_code (upc), price_including_tax, price_excluding_tax, number_available, 
    table = soup_book_page.find("table", {"class": "table table-striped"})
    for row in table.find_all("tr"):
        th = row.find("th").get_text()
        td = row.find("td").get_text()
        # UPC
        if "UPC" in th:
            booking["upc"] = td
        # price without tax
        if "Price (excl. tax)" in th:
            booking["price_excluding_tax"] = td
        # price with tax
        if "Price (incl. tax)" in th:
            booking["price_including_tax"] = td
        # stock
        if "Availability" in th:
            booking["stock"] = td
    
	# product_description
    descpt_bs = soup_book_page.find_all("p")
    descpt_list = []
    for descpt in descpt_bs:
        descpt_list.append(descpt.text)
	
    if descpt_list[3]:
        booking["description"] = unicodedata.normalize('NFC', str(descpt_list[3])).encode("ascii", "ignore").decode()
    else:
        booking["description"] = "Sans description"
	
    booking["category"] = category
    booking["url"] = url_book

	#review_rating
    rating_bs = soup_book_page.find("p", {"class": "star-rating"})
    rating = str(rating_bs).split("\n")[0].replace('<p class="star-rating ', "").replace('">', "")
    booking["review_rating"] = mapping_number[rating]

    # image url
    url_img_bs = soup_book_page.img["src"]
    url_site_root = "http://books.toscrape.com/"
    url_img = url_site_root + url_img_bs.replace("../", "")
    booking["image_url"] = url_img
    # load and save img 
    img_title = title_book.replace("'", "_").replace(" ", "_").replace(":", "").replace("#", "").replace(".", "").replace(",", "").replace("/", "_").replace('"', "").replace("&", "").replace("*", "").replace("?", "")
    urllib.request.urlretrieve(url_img, f"../scrapbook/image/{img_title}.jpg")   
    return booking


#write in csv file
def export_csv(books, category):
    #Export data in csv file
    with open(f"csv/{category}.csv", "w", newline="") as csvfile:  
        writer = csv.DictWriter(csvfile, fieldnames=['title', 'url', 'upc', 'price_including_tax', 'price_excluding_tax', 'description', 'category', 'stock', 'review_rating', 'image_url'])
        writer.writeheader() 
        for book in books:
            writer.writerow(book)

#Main function
url = "http://books.toscrape.com"
urls_category = get_url_categories(url)
for url_category in urls_category:
    books = []
    url = f"http://books.toscrape.com/{url_category}"
    print(url)
    urls_book, category = get_url_books(url)
    for url_book in urls_book:
        url_book = f"http://books.toscrape.com/catalogue/{url_book}"
        book = extract_book_data(url_book)
        books.append(book)
    export_csv(books, category)