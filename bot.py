import requests
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

import numpy as np
from scipy.interpolate import make_interp_spline

# The bot class is used to send messages from groupme and get weather data
class bot:

    def __init__(self, groupme_key, groupme_bot_id, open_weather_key):
        self.groupme_key = groupme_key
        self.groupme_bot_id = groupme_bot_id
        self.open_weather_key = open_weather_key
        self.groupme_base_url = "https://api.groupme.com/v3"
        self.open_weather_base_url = "https://api.openweathermap.org/data/2.5/forecast"

    def send_message(self, messageString, image_url=None):
        messageURL = self.groupme_base_url + "/bots/post"
        params = {"bot_id": self.groupme_bot_id, "text": messageString}
        if image_url is not None:
            params["picture_url"] = image_url
        r = requests.post(messageURL, params=params)
        print(r.text)
        return r.status_code

    def get_group_id(self, groupName):
        messageURL = self.groupme_base_url + "/groups"
        params = {"omit": "memberships", "token": self.groupme_key}
        r = requests.get(messageURL, params).json()["response"]
        for item in r:
            if groupName in item["name"]:
                return item["id"]
        return -1

    def get_weather(self):
        messageURL = self.open_weather_base_url
        params = {
            "lat": 34.681814,
            "lon": -82.862603,
            "appid": self.open_weather_key,
            "units": "imperial",
            "exclude": ["current", "minutely"],
        }
        r = requests.get(messageURL, params).json()
        x = list(range(0, 24, 3))
        windData = []
        gustData = []
        for i, data in enumerate(r["list"][:8]):
            windData.append(data["wind"]["speed"])
            gustData.append(data["wind"]["gust"])
        plt.plot(x, windData)
        plt.plot(x, gustData)
        spl = make_interp_spline(x, windData, k=3)
        y_smooth = spl(x)f

        plt.title("Wind data over the next 24 hours in Clemson, SC")
        plt.ylabel("Wind speed (MPH)")
        plt.xlabel("Hours from now")
        plt.legend(["Wind Speed", "Wind Gust"], )
        plt.savefig("windplot.png")
        return self.upload_image("windplot.png")

    def upload_image(self, image_path):
        url = "https://image.groupme.com/pictures"
        headers = {
            "X-Access-Token": self.groupme_key,
            "Content-Type": "image/png",  # Adjust for PNG, etc.
        }
        with open(image_path, "rb") as image_file:
            response = requests.post(url, headers=headers, data=image_file)
        if response.status_code == 200:
            return response.json()["payload"]["picture_url"]
        else:
            return "Error: {response.text}"


if __name__ == "__main__":
    # load the API keys from the .env file
    load_dotenv()
    GROUPME_KEY = os.getenv("GROUPME_KEY")
    OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")
    GROUPME_BOT_ID = os.getenv("GROUPME_BOT_ID")

    # create the instance of the bot and send a message
    myBot = bot(GROUPME_KEY, GROUPME_BOT_ID, OPEN_WEATHER_KEY)
    image_url = myBot.get_weather()
    print(f"Image URL: {image_url}")
    status = myBot.send_message("This is the wind forcast for the docks over the next 24 hours", image_url)
    print(f"status code of message code: {status}")
