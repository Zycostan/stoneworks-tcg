import os
import time
import requests
from bs4 import BeautifulSoup

# Directory to save skins
os.makedirs("skins", exist_ok=True)

# Base URL for bans
base_url = "https://stoneworks.gg/bans/bans.php"
all_bans = {}

page = 102

while True:
    print(f"Fetching page {page}...")
    try:
        response = requests.get(f"{base_url}?page={page}", timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"Timeout while fetching page {page}. Retrying...")
        time.sleep(2)  # Wait and retry
        continue
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page}: {e}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")  # Adjust selector based on actual table structure

    if not rows:  # Break if no rows
        print("No more data found. Stopping.")
        break

    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 2:
            player = columns[0].text.strip()
            banned_by = columns[1].text.strip()

            if player not in all_bans:
                all_bans[player] = banned_by

            try:
                uuid_url = f"https://api.mojang.com/users/profiles/minecraft/{player}"
                uuid_response = requests.get(uuid_url, timeout=10)
                if uuid_response.status_code == 200:
                    uuid = uuid_response.json().get("id")

                    skin_preview_url = f"https://crafatar.com/renders/body/{uuid}?overlay"
                    img_response = requests.get(skin_preview_url, timeout=10)

                    if img_response.status_code == 200:
                        file_path = f"skins/{player}.png".replace(" ", "_")
                        with open(file_path, "wb") as file:
                            file.write(img_response.content)
                        print(f"Downloaded skin for {player}")
                    else:
                        print(f"Failed to download skin for {player}")
                else:
                    print(f"Failed to fetch UUID for {player}")
            except Exception as e:
                print(f"Error processing {player}: {e}")

    page += 1
    time.sleep(2)  # Rate limiting
