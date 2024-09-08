import requests
import json
import re

# API endpoint
url = "https://67adf88317.yunchenshop.store/apimanager/api/product/collection/create"

# Headers
headers = {
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,fr;q=0.5",
    "access-token": "r3IRJt0zzJtLU1CrU9ZUpzCq2MCfoKVC",
    "client-type": "10",
    "Content-Type": "application/json"
}

# Function to generate a handle from the title
def generate_handle(title):
    return re.sub(r'\W+', '-', title.lower()).strip('-')

# User input: Accept multiline input for song titles (paste into the console)
print("Please paste the song titles, one per line. When done, press Enter twice:")
songs_input = []
while True:
    song = input()
    if song == "":
        break
    songs_input.append(song)

# Process each song title from the input
for song in songs_input:
    # Create payload for each song
    payload = {
        "meta_is_edit": "1",
        "meta_title": song,  # Song title for meta_title
        "meta_keywords": "",
        "meta_description": "",
        "handle": generate_handle(song),  # Generated handle from the song title
        "translate_type": "",
        "body_html": "",
        "title": song,  # Song title for the collection title
        "image": "",
        "collectionInfo": []
    }

    # Send the POST request for each song
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check response for each request
    if response.status_code == 200:
        print(f"Collection created successfully for '{song}'!")
    else:
        print(f"Failed to create collection for '{song}'. Status code: {response.status_code}")
        print("Error:", response.text)
