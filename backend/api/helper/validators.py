import requests

def url_accessible(url):
    headers = {
        'User-Agent': (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        return response.ok and response.status_code == 200
    except requests.RequestException as e:
        print(f"Error: {e}")
        return False
    

def isStringEmpty(string):
    return not bool(string)