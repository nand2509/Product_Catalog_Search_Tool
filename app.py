# from flask import Flask, render_template,request,send_file
# from bs4 import BeautifulSoup
# import requests
# import re
# import io
# import pandas as pd
#
# app = Flask(__name__)
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#   url = 'https://www.webscraper.io/test-sites/e-commerce/allinone/computers/tablets'
#   page = requests.get(url)
#   soup = BeautifulSoup(page.text, "lxml")
#
#   # Column1 = Product_name
#   names = soup.find_all("a",class_ = "title")
#   product_name = []
#   for i in names:
#     name = i.text
#     product_name.append(name)
#
#   # Column2 = product_prices
#   prices = soup.find_all("h4" , class_ = "price float-end card-title pull-right")
#   product_price = []
#   for i in prices:
#     price = i.text
#     product_price.append(price)
#
#   # Column3 = Product_Description
#   desc = soup.find_all("p" , class_ = "description card-text")
#   product_description = []
#   for i in desc:
#     desce = i.text
#     product_description.append(desce)
#
#   # product_reveiws
#   review = soup.find_all("p" , class_ = "review-count float-end")
#   product_reviews=[]
#   for i in review:
#     rev = i.text
#     product_reviews.append(rev)
#
#
#   # Convert into dataframe using Pandas
#
#   df = pd.DataFrame({"Product_Name" : product_name , "Product_Price" : product_price , "Product_Description" : product_description , "Product_Reviews" : product_reviews})
#
#   search_query = request.form.get('search')
#   action = request.form.get('action')
#
#   if search_query:
#     df = df[df['Product_Name'].str.contains(search_query, case=False, na=False)]
#
#     if request.form.get('download') == 'Download CSV':
#         return download_csv(df)
#
#   return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
#
#
# def download_csv(df):
#   buffer = io.StringIO()
#   df.to_csv(buffer, index=False)
#   buffer.seek(0)
#   return send_file(buffer, mimetype='text/csv', as_attachment=True, download_name='products.csv')
#
# if __name__ == '__main__':
#   app.run(debug=True)


from flask import Flask, render_template, request, send_file
from bs4 import BeautifulSoup
import requests
import pandas as pd
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the selected product type
        product_type = request.form.get('product_type')

        if product_type == 'tablets':
            url = 'https://www.webscraper.io/test-sites/e-commerce/allinone/computers/tablets'
        elif product_type == 'laptops':
            url = 'https://www.webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
        elif product_type == 'phones':
            url = 'https://www.webscraper.io/test-sites/e-commerce/allinone/phones/touch'
        else:
            return render_template('index.html', message="Please select either Tablets, Laptops, or Phones.")

        # Function to scrape data from a given URL
        def scrape_data(url):
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            product_name = [name.text.strip() for name in soup.find_all("a", class_="title")]
            product_price = [price.text.strip() for price in soup.find_all("h4", class_="price float-end card-title pull-right")]
            product_description = [desc.text.strip() for desc in soup.find_all("p", class_="description card-text")]
            product_reviews = [review.text.strip() for review in soup.find_all("p", class_="review-count float-end")]

            return pd.DataFrame({
                'Product Name': product_name,
                'Price': product_price,
                'Description': product_description,
                'Reviews': product_reviews
            })

        # Scrape data based on the selected product type
        df = scrape_data(url)

        # Filter data based on search query
        search_query = request.form.get('search')
        if search_query:
            df = df[df['Product Name'].str.contains(search_query, case=False, na=False)]

        # Handle CSV download request
        if request.form.get('action') == 'download':
            return download_csv(df)

        return render_template('index.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values, search_query=search_query)

    # If GET request or no product type selected, render the initial form
    return render_template('index.html', message="Please select either Tablets, Laptops, or Phones.")

def download_csv(df):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(buffer, mimetype='text/csv', as_attachment=True, attachment_filename='products.csv')

if __name__ == '__main__':
    app.run(debug=True,port=9000)