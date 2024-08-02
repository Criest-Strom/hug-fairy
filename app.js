// Import required modules
const express = require('express');
const cors = require('cors');
const axios = require('axios');

// Create an Express app
const app = express();

// Enable CORS
app.use(cors({
  origin: '*',
  methods: 'POST',
  allowedHeaders: 'Content-Type'
}));

// Twitter API credentials
const bearerToken = process.env.BEARER_TOKEN;

// Set up the Twitter API object
const client = axios.create({
  baseURL: 'https://api.twitter.com/2/',
  headers: {
    Authorization: `Bearer ${AAAAAAAAAAAAAAAAAAAAAGh3vAEAAAAAOW%2BMY4UNM8X8B0OP3J91%2FVIFHYs%3DHJ9sOeUzIFycCcBPy5txv7byRHsycydrcRme0YdAAUoMkVC80L}`,
    'Content-Type': 'application/json'
  }
});

// Healthcheck endpoint
app.get('/healthcheck', (req, res) => {
  res.send('Express app is running on Vercel!');
});

// Hug tweet endpoint
app.post('/api/hug-tweet', (req, res) => {
  const eventData = req.body;
  try {
    // Extract the username from the event data
    const status = eventData.data.text;
    const usernameMention = eventData.entities.user_mentions.map(entity => entity.username);
    if (usernameMention.length > 0) {
      const username = usernameMention[0];
      const message = `hugs @${username} 🤗`;
      client.post('tweets', { text: message })
        .then(response => {
          res.json({ message: `Hug tweet sent to @${username}!` });
        })
        .catch(error => {
          console.error(`Error posting tweet: ${error}`);
          res.status(500).json({ error: `Error posting tweet: ${error}` });
        });
    } else {
      res.status(400).json({ error: 'No username found in the tweet.' });
    }
  } catch (error) {
    console.error(`Error processing request: ${error}`);
    res.status(500).json({ error: `Error processing request: ${error}` });
  }
});

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
