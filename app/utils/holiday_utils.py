import requests

def get_holidays(api_url):
    try:
        response = requests.get(api_url)
        holidays = response.json()
        return holidays
    except Exception as e:
        print(f"Error fetching holidays: {e}")
        return {}
