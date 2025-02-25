import requests

url = "https://image.groupme.com/pictures"
access_token = "SEwIm3nN1jdd4WDp5jT5loSvHPk9cfbAi8RwpRXM"
image_path = "avatar.jpg"

headers = {
    "X-Access-Token": access_token,
    "Content-Type": "image/jpeg"  # Adjust for PNG, etc.
}

with open(image_path, "rb") as image_file:
    response = requests.post(url, headers=headers, data=image_file)

if response.status_code == 200:
    image_url = response.json()["payload"]["picture_url"]
    print(f"Image URL: {image_url}")
else:
    print(f"Error: {response.text}")