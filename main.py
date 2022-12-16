import requests
import secrets
from prettytable import PrettyTable

print("Введите id  аккаунта в доте: ")
account_id = input()
if account_id == "master":
    account_id = secrets.account_id

params = {
    "api_key": secrets.api_token
}

wl_response = requests.get(f"https://api.opendota.com/api/players/{account_id}/wl", params=params)
normal_wins = wl_response.json()["win"]
normal_lose = wl_response.json()["lose"]

name_response = requests.get(f"https://api.opendota.com/api/players/{account_id}", params=params)
player_name = name_response.json()["profile"]["personaname"]

print(f"Имя: {player_name}")

turbo_params = {
    "api_key": secrets.api_token,
    "significant": 0,
    "game_mode": 23
}

turbo_wl_response = requests.get(
    f"https://api.opendota.com/api/players/{account_id}/wl", params=turbo_params)
turbo_wins = turbo_wl_response.json()["win"]
turbo_lose = turbo_wl_response.json()["lose"]

user_stats = PrettyTable()
user_stats.field_names = ["Тип игры", "Побед", "Поражений", "Процент побед"]
user_stats.add_rows(
    [
        ["Турбо", turbo_wins, turbo_lose, round(turbo_wins / (turbo_lose + turbo_wins) * 100, 2)],
        ["Обычная", normal_wins, normal_lose, round(normal_wins / (normal_wins + normal_lose) * 100, 2)]
    ]
)
print(user_stats)

all_heroes_response = requests.get("https://api.opendota.com/api/heroes", params=params)
id_name_heroes_data = {}

for hero in all_heroes_response.json():
    id_name_heroes_data[str(hero["id"])] = hero["localized_name"]

response_heroes = requests.get(f"https://api.opendota.com/api/players/{account_id}/heroes", params=params)
best_twenty_heroes = response_heroes.json()[:20]

hero_stats = PrettyTable()
hero_stats.field_names = ["Название героя", "Матчей", "Количество побед", "Количество поражений", "Процент побед"]
for hero in best_twenty_heroes:
    hero_stats.add_row([id_name_heroes_data[hero["hero_id"]], hero["games"], hero["win"],
                        hero["games"] - hero["win"], round(hero["win"] / hero["games"] * 100, 2)])

print("Лучшие 20 героев \n", hero_stats)
