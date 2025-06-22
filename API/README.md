# Reddit Toxicity Scanner API

A FastAPI-based application that analyzes toxicity in Reddit comments using machine learning.

## Features

- Scrapes comments from Reddit submissions using JSON API
- Cleans and preprocesses comment text
- Predicts toxicity using trained machine learning model
- Returns detailed analysis results with confidence scores

## Installation

1. Install the required dependencies:
```bash
pip install -r requirement.txt
```

2. Make sure the model files are available in the `../model/` directory:
   - `toxic_detection.pkl` (combined model and vectorizer)
   - OR separate files: `model_logistic_regression.pkl` and `tfidf_vectorizer.pkl`

## Running the API

1. Start the FastAPI server:
```bash
python app.py
```

2. The API will be available at:
   - Main API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## API Endpoints

### POST /analyze_reddit

Analyzes toxicity in Reddit comments from a given URL.

**Request:**
- Method: POST
- Content-Type: application/x-www-form-urlencoded
- Body: `linkReddit=<reddit_url>`

**Response:**
```json
{
  "message": "Analysis completed successfully",
  "reddit_url": "https://reddit.com/r/...",
  "raw_comments": ["original comment 1", "original comment 2"],
  "cleaned_comments": ["cleaned comment 1", "cleaned comment 2"],
  "predictions": [
    {
      "comment": "cleaned comment text",
      "status": "toxic|non-toxic",
      "confidence": 85.5,
      "raw_prediction": 1,
      "probabilities": {
        "non-toxic": 14.5,
        "toxic": 85.5
      }
    }
  ],
  "statistics": {
    "total_comments": 10,
    "toxic_count": 3,
    "non_toxic_count": 7,
    "average_confidence": 82.3,
    "toxicity_percentage": 30.0
  }
}
```

## Using with Postman

1. Open Postman
2. Create a new POST request
3. Set URL to: `http://localhost:8000/analyze_reddit`
4. Go to Body tab
5. Select "x-www-form-urlencoded"
6. Add key: `linkReddit` with value: your Reddit URL
7. Send the request

## Project Structure

```
API/
├── app.py                 # Main FastAPI application
├── requirement.txt        # Python dependencies
├── README.md             # This file
├── test.py               # Original test script
└── middleware/           # Modular functions
    ├── __init__.py
    ├── reddit_scraper.py # Reddit comment scraping
    ├── text_cleaner.py   # Text preprocessing
    └── model_predictor.py # ML model prediction
```

## Text Cleaning Process

The API automatically cleans scraped comments using:
- Convert to lowercase
- Remove URLs
- Remove mentions (@username)
- Remove hashtags (keep words)
- Remove special characters
- Remove numbers
- Remove single characters
- Normalize whitespace

## Error Handling

The API includes comprehensive error handling for:
- Invalid Reddit URLs
- Network errors during scraping
- Model loading issues
- Empty comment sections
- Malformed requests

## Health Check

Use `GET /health` to check if the API and model are working correctly. 