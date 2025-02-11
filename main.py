from flask import Flask, request, render_template, redirect, url_for
import random
import string
from mongoDB import createURL,getURL
import hashlib
app = Flask(__name__)


# def generate_alphanumeric_code(length=6):
#     # Define characters for the code (letters and digits)
#     characters = string.ascii_letters + string.digits
#     # Randomly select characters to create the code
#     code = ''.join(random.choices(characters, k=length))
#     return code

def hash_url(url):
    # Encoding string and generating MD5 hash
    result = hashlib.md5(url.encode())

    # Getting the hexadecimal equivalent of the hash
    hex_hash = result.hexdigest()

    # Extracting the first 6 alphanumeric characters
    short_hash = hex_hash[:6]
    return short_hash


def addurl(url):

    # Generate a short URL code using hash_url
    short_hash = hash_url(url)

    # Check if the short URL already exists in the database
    if getURL(short_hash) is None:
        # Create a new entry for the short URL
        data = {"var": short_hash, "URL": url}
        createURL(data)
        return short_hash

    # Retrieve the existing short URL record
    response = getURL(short_hash)
    if response is None:
        raise ValueError(f"No record found for hash: {short_hash}")

    # Extract and return the short URL code from the response
    return response.get("var")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            # Generate and add the URL, get the short code
            short_url_code = addurl(url)
            # Pass the short URL code and full URL to the template
            return render_template('index.html', short_url=short_url_code, full_url=url)
        else:
            return render_template('index.html', error="Please enter a valid URL.")

    return render_template('index.html')

@app.route('/url/<var>')
def redirect_url(var):
        # Redirect to the original URL associated with the short URL
    result = getURL(var)
    print(result["URL"])
    redURL=result["URL"]
    return redirect(redURL, code=302)

if __name__ == "__main__":
    app.run(debug=True)
