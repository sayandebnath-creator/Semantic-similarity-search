import requests

def load_company_data():
    url = "http://130.211.212.39:8080/list-companies"  # replace with real endpoint
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching company data")
        return []

    data = response.json()

    companies = []
    for item in data:
        companies.append({
            "id": item.get("id"),
            "name": item.get("companyName", "Unknown"),
            "symbol": item.get("symbol"),
            "sector": item.get("sector"),
            "ceo": item.get("ceo"),
            "city": item.get("city"),
            "state": item.get("state"),
            "zip": item.get("zip"),
            "description": item.get("description", ""),
            "website": item.get("website"),
            "image": item.get("image"),
        })
    return companies
