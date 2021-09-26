import requests
import json


def get_inn_data(inn_number):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Token 3350474eeccef34236a18c1508848b0703de281d",
    }
    response = requests.get(f"https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party?query={inn_number}",
                            headers=headers)
    data_json = response.json()
    suggestions = list(filter(lambda item: str(item.get("data", {}).get("inn", {})) == str(inn_number),
                              data_json.get("suggestions", [])))
    if not suggestions:
        return None
    return suggestions[0]


def get_auction_id_data(auction_id):
    with open("api/database/auctions.json", encoding="utf8") as f:
        auctions = json.load(f)
    for item in auctions.get("data", []):
        if str(item["id"]) == str(auction_id):
            return item
    return None
