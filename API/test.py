import requests
import sys
import re

def fetch_comments(data, out_list):
    """
    Recursively traverse comments & replies, append body text (flattened to one line).
    """
    for item in data:
        if item.get('kind') != 't1':
            continue
        d = item['data']
        body = d.get('body', '').strip()
        if body:
            # flatten multiline into single line
            one_line = ' '.join(body.splitlines())
            # (opsional) hapus extra-whitespace
            one_line = re.sub(r'\s+', ' ', one_line)
            out_list.append(one_line)
        # process replies
        replies = d.get('replies')
        if replies and isinstance(replies, dict):
            children = replies.get('data', {}).get('children', [])
            fetch_comments(children, out_list)

def test_scrape_json(reddit_url: str):
    """
    Fetch all comments via JSON API and print only the comment text, one per line.
    """
    base = reddit_url.rstrip('/')
    json_url = base + '.json'
    headers = {
        'User-Agent': 'RedditCommentScraper/1.0 (+https://github.com/yourname)'
    }

    print(f"Mengambil JSON: {json_url}")
    resp = requests.get(json_url, headers=headers)
    if resp.status_code != 200:
        print(f"ERROR: HTTP {resp.status_code}")
        return

    data = resp.json()
    try:
        top_comments = data[1]['data']['children']
    except (IndexError, KeyError):
        print("Format JSON tidak sesuai atau tidak ada komentar.")
        return

    flat_comments = []
    fetch_comments(top_comments, flat_comments)

    if not flat_comments:
        print("Tidak ada komentar ditemukan.")
        return

    for comment in flat_comments:
        print(comment)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python test.py <reddit_submission_url>")
        sys.exit(1)
    test_scrape_json(sys.argv[1])
