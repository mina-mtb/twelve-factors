from statistics import mode

import requests
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

app_mode = os.environ.get('APP_MODE')
ip_api_url = os.environ.get('IP_API_URL').__str__()
weather_api_url = os.environ.get('WEATHER_API_URL').__str__()
weather_api_key = os.environ.get('WEATHER_API_KEY').__str__()
print(app_mode)
print(ip_api_url)
print(weather_api_key)
print(weather_api_url)
res_ip = requests.get(ip_api_url)
res_weather = requests.get(weather_api_url + "/current.json", params={"key": weather_api_key, "q": res_ip.json().get("city")})  







def Print_by_mode(mode, x,current_Api):
    if mode == "local":
        print(current_Api.status_code ,current_Api.json())
    else:
        print(x)



def Get_location():
    if res_ip.status_code == 200:
        x="Detecting location..."
        Print_by_mode(app_mode, x, res_ip)
        return res_ip.json().get("city",)
    else:
        x="Error: Unable to detect location."
        Print_by_mode(app_mode, x, res_ip)
        os._exit(1)    


def Get_weather(city, app_mode):
    params_weather = {
        "key": weather_api_key,
        "q": city
    }

    res_weather = requests.get(weather_api_url + "/current.json", params=params_weather)

    if res_weather.status_code == 200:
        x=f"Current weather in {city}: {res_weather.json().get('current', {}).get('temp_c')}°C, {res_weather.json().get('current', {}).get('condition', {}).get('text')}"
        Print_by_mode(app_mode, x, res_weather) 
    else:
        x="Error: Unable to fetch weather information."
        Print_by_mode(app_mode, x, res_weather)
        os._exit(1)    


city = Get_location()
Get_weather(city, app_mode)






"""    

    if res_weather.status_code == 200:
        x=f"Current weather in {city}: {res_weather.json().get('current', {}).get('temp_c')}°C, {res_weather.json().get('current', {}).get('condition', {}).get('text')}"
        Print_by_mode(app_mode, x)
    else:
        x="Error: Unable to fetch weather information."
        Print_by_mode(app_mode, x)
        os._exit(1)




if res_ip.status_code == 200:
    if app_mode == "local":
     print(res_ip.json())
    else:
     print("Detecting location...") 
else:
    if app_mode == "local":
     print(f"Error: {res_ip.status_code}")
    else:
     print("Error: Unable to detect location.")
     os._exit(1) 


city = res_ip.json().get("city",)

# Get the current weather information for the detected city

params_weather = {
    "key": weather_api_key,
    "q": city
}

res_weather = requests.get(weather_api_url + "/current.json", params=params_weather)

if res_weather.status_code == 200:
    if app_mode == "local":
        print(res_weather.json())
    else:
        print(f"Current weather in {city}: {res_weather.json().get('current', {}).get('temp_c')}°C, {res_weather.json().get('current', {}).get('condition', {}).get('text')}")  
else:
    if app_mode == "local":
        print(f"Error: {res_weather.status_code}")
    else:
        print("Error: Unable to fetch weather information.")
        os._exit(1)  




"""