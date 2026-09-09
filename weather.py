import requests

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
OWM_api_key = "6ca0e0f0a3e1576a1ffbfbed97897237"

weather_params = {
    "lat":48.659550,
    "lon":8.940970,
    "appid":OWM_api_key,
    "cnt":4,
}
response = requests.get(OWM_Endpoint,params=weather_params)
response.raise_for_status()
print(response.status_code)
weather_data = response.json()
# print(weather_data["list"][0]["weather"][0]["id"])
will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    print("Bring an umbrella.")