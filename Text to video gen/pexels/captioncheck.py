import requests

# Your Pexels API key
PEXELS_API_KEY = 'DfFwCzubOYn49jfG9x1LMjlupVjeoqVUaXm7mZSazVyT4IlwbNegIA2x'

def search_pexels_videos(query, per_page=1):
    url = f'https://api.pexels.com/videos/search?query={query}&per_page={per_page}'
    headers = {
        'Authorization': PEXELS_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
query = "nature"
videos = search_pexels_videos(query)
if videos:
    for video in videos['videos']:
        print(video['url'])
