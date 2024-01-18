from flask import Flask, render_template, request, redirect, url_for
import random
import string

app = Flask(__name__)

# Dictionary to store shortened URLs
url_store = {}

def generate_alias():
    alias_length = 6
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(alias_length))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form.get('url')
    custom_alias = request.form.get('custom_alias')

    # Check if the alias is already in use
    if custom_alias and custom_alias in url_store:
        return render_template('error.html', message='Alias already in use. Please choose another.')

    # Generate a unique alias or use the custom one
    alias = custom_alias if custom_alias else generate_alias()

    # Store the shortened URL
    url_store[alias] = original_url

    # Construct the shortened URL
    shortened_url = request.host_url + alias

    return render_template('index.html', original_url=original_url, shortened_url=shortened_url)

@app.route('/<alias>')
def redirect_to_original(alias):
    # Redirect to the original URL if the alias exists
    if alias in url_store:
        return redirect(url_store[alias])
    else:
        return render_template('error.html', message='URL not found.')

@app.route('/history')
def history():
    return render_template('history.html', url_history=url_store)

if __name__ == '__main__':
    app.run(debug=True)