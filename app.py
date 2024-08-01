from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Twitter API credentials
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAGh3vAEAAAAAOW%2BMY4UNM8X8B0OP3J91%2FVIFHYs%3DHJ9sOeUzIFycCcBPy5txv7byRHsycydrcRme0YdAAUoMkVC80L'

# Giphy API credentials
giphy_api_key = '7vrbmQgoOYSa3Dru7kewClrWG8xN08jq'

# Set up the Twitter API object
def create_twitter_api():
    return BearerTokenAuth(bearer_token)

class BearerTokenAuth(requests.auth.AuthBase):
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        return r

# Set up the Giphy API object
headers = {"api_key": giphy_api_key}

def get_random_hug_gif():
    try:
        response = requests.get(f"https://api.giphy.com/v1/gifs/random?tag=bear-hug", headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["data"]["images"]["original"]["url"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Giphy API: {e}")
        return None

@app.route('/api/hug-tweet')
def index():
    return render_template('index.html')

@app.route('/api/hug-tweet', methods=['POST'])
def generate_hug_tweet_endpoint():
    username = request.form['username']
    try:
        hug_gif = get_random_hug_gif()
        message = f"hugs @{username} {hug_gif}"
        api = create_twitter_api()
        response = requests.post(
            f"https://api.twitter.com/2/tweets",
            auth=api,
            json={"text": message}
        )
        response.raise_for_status()
        return jsonify({'message': f'Hug tweet sent to @/{username}!'})

    except requests.exceptions.RequestException as e:
        print(f"Error posting tweet: {e}")
        return jsonify({'error': 'Failed to post tweet'}), 500

if __name__ == '__main__':
    app.run(debug=True)
