from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import uvicorn

from middleware.reddit_scraper import scrape_reddit_comments
from middleware.text_cleaner import clean_comments
from middleware.model_predictor import ToxicityPredictor

app = FastAPI()

try:
    predictor = ToxicityPredictor()
except Exception as e:
    predictor = None

@app.post("/analyze_reddit")
async def analyze_reddit(linkReddit: str = Form(...)):
    try:
        if not linkReddit or not linkReddit.strip():
            raise HTTPException(status_code=400, detail="Reddit URL is required")
        
        if "reddit.com" not in linkReddit.lower():
            raise HTTPException(status_code=400, detail="Invalid Reddit URL")
        
        raw_comments = scrape_reddit_comments(linkReddit)
        
        if not raw_comments:
            return JSONResponse(status_code=200, content={ "comments": [], "statistics": { "total_comments": 0, "toxic_count": 0, "non_toxic_count": 0, }})
        
        cleaned_comments = clean_comments(raw_comments)
        
        if predictor is None:
            raise HTTPException(status_code=500, detail="Model not available")
        
        predictions = predictor.predict_toxicity(cleaned_comments)
        
        comments_response = []
        for i, raw_comment in enumerate(raw_comments):
            if i < len(predictions):
                prediction = predictions[i]
                comments_response.append({ "comment": raw_comment, "status": prediction.get("status", "error"), "percentage": prediction.get("confidence", 0)
                })
            else:
                comments_response.append({ "comment": raw_comment, "status": "error", "percentage": 0})
        
        statistics = predictor.get_overall_statistics(predictions)
        
        response_data = {"comments": comments_response, "statistics": statistics}
        
        return JSONResponse(status_code=200, content=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
