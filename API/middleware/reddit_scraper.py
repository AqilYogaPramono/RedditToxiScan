import requests
import re
from typing import List

def fetch_comments(data, out_list: List[str]):
    for item in data:
        if item.get('kind') != 't1':
            continue
        d = item['data']
        body = d.get('body', '').strip()
        if body:
            one_line = ' '.join(body.splitlines())
            one_line = re.sub(r'\s+', ' ', one_line)
            out_list.append(one_line)
        replies = d.get('replies')
        if replies and isinstance(replies, dict):
            children = replies.get('data', {}).get('children', [])
            fetch_comments(children, out_list)

def scrape_reddit_comments(reddit_url: str) -> List[str]:
    base = reddit_url.rstrip('/')
    json_url = base + '.json'
    headers = {'User-Agent': 'RedditCommentScraper/1.0'}

    try:
        resp = requests.get(json_url, headers=headers)
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}")
        
        data = resp.json()
        top_comments = data[1]['data']['children']
        
        flat_comments = []
        fetch_comments(top_comments, flat_comments)
        
        return flat_comments
    except Exception as e:
        raise Exception(f"Error scraping Reddit comments: {str(e)}") 