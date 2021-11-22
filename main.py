import requests
from datetime import datetime
import os


APP_ID = os.environ["APP_ID"]
API_KEY = os.environ.get("API_KEY")
SHEETY_USERNAME = os.environ.get("SHEETY_USERNAME")
SHEETY_PASSWORD = os.environ.get("SHEETY_PASSWORD")

GENDER = "male"
WEIGHT_KG = 77
HEIGHT_CM = 183
AGE = 27

nutritionix_exercise_url = "https://trackapi.nutritionix.com/v2/natural/exercise"


##### Get data from Nutritionix #####

user_exercise = input("Tell me which exercise you did? ")

nutritionix_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

nutritionix_params = {
    "query": user_exercise,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(url=nutritionix_exercise_url, json=nutritionix_params, headers=nutritionix_headers)
result = response.json()
activity = result["exercises"][0]["name"].title()
duration = result["exercises"][0]["duration_min"]
calories = result["exercises"][0]["nf_calories"]


##### Upload to Google Sheets #####

sheety_url = "https://api.sheety.co/7166f9424cc69ab6c44732a4cbf6c74a/pythonWorkouts/workouts"

today = datetime.now()

sheety_auth = (SHEETY_USERNAME, SHEETY_PASSWORD)  # ("username", Password")

for exercise in result["exercises"]:
    sheety_params = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%T"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    response = requests.post(url=sheety_url, json=sheety_params, auth=sheety_auth)
    print(response.text)


