from flask import Flask, request, render_template, redirect, url_for
import random
import string

app = Flask(__name__)

# Dictionary to store short URL mapping
urlDict = {"ghdeqs": "https://mail.google.com/mail/u/0/#inbox"}

def generate_alphanumeric_code(length=6):
    # Define characters for the code (letters and digits)
    characters = string.ascii_letters + string.digits
    # Randomly select characters to create the code
    code = ''.join(random.choices(characters, k=length))
    return code

def addurl(url):
    # Generate a short URL code and add it to the dictionary
    var = generate_alphanumeric_code()
    urlDict[var] = url
    return var  # Return the short URL code

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
    if var in urlDict:
        # Redirect to the original URL associated with the short URL
        return redirect(urlDict.get(var), code=302)
    else:
        return "No TinyURL Found", 404

if __name__ == "__main__":
    app.run(debug=True)