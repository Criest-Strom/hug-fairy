from flask import Flask, request, jsonify, render_template
import tweepy
import requests

app = Flask(__name__)
CORS(app)

# Twitter API credentials
consumer_key = 'ufZ9AntSrk9cLZYOssEXwxL9Z'
consumer_secret = 'Sm7OXU7MTqRrmfoDif0CR16mGKLvRZgqzMTVB4jRLsin3P6F6J'
access_token ='1818374940883927042-SRD7qaTGPkuVFUAajCkLosWPOyPvKb'
access_token_secret = 'cGbOo7wxRPQ6TMD00lWFMOMnbCaDGXkYeo1sQgF7Ba0uhT'

# Giphy API credentials
giphy_api_key = '7vrbmQgoOYSa3Dru7kewClrWG8xN08jq'

# Set up the Twitter API object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hug-tweet', methods=['POST'])
def generate_hug_tweet_endpoint():
    username = request.form['username']
    try:
        hug_gif = get_random_hug_gif()
        message = f"hugs @/{username} {hug_gif}"
        api.update_status(message)
        return jsonify({'message': f'Hug tweet sent to @/{username}!'})

    response = make_response(jsonify({'tweet': hug_tweet}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

    except tweepy.TweepError as e:
        print(f"Error posting tweet: {e}")
        return jsonify({'error': 'Failed to post tweet'}), 500

if __name__ == '__main__':
    app.run(debug=True)
