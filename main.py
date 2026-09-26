import os
import sys
import argparse
import requests
from dotenv import load_dotenv


# Load the environment variables from .env file
load_dotenv()

def print_by_mode(mode, text, response=None):
    if mode == "local" and response is not None:
        try:        
            print(response.status_code, response.json())
        except Exception:
            print(response.status_code, response.text)    
    else:
        print(text)


def get_location(ip_api_url, app_mode):
    if not ip_api_url:
        print("Error: IP_API_URL is not configured", file=sys.stderr)
        sys.exit(1)

    try:
        res_ip = requests.get(ip_api_url)
    except requests.RequestException as e:
        print(f"Error conecting to IP service: {e}", file=sys.stderr)    
        sys.exit(1)

    if res_ip.status_code == 200:
        data = res_ip.json()
        city = data.get("city") or data.get("City") or "Unknown"
        country = data.get("country") or data.get("Country") or "Unknown"
        ip_addr = data.get("IP") or data.get("ip") or "Unknown"

        display_msg = f"Detected IP: {ip_addr} - Location: {city}({country})"
        print_by_mode(app_mode, display_msg, res_ip)
        return data 
    else:
        err_msg = f"Error: Unable to detect location with status code {res_ip.status_code}."
        print_by_mode(app_mode, err_msg, res_ip)
        sys.exit(1)   


def checking_city():
    return True


def get_weather(city, app_mode, weather_api_url, weather_api_key):
    if not weather_api_url:
        print("Error: Weather_API_URL is not configured", file=sys.stderr)
        sys.exit(1)
    if not weather_api_key:
        print("Error: Weather_API_Key is not configured", file=sys.stderr)    
        sys.exit(1)


         
    params_weather = {
        "key" : weather_api_key,
        "q" : city
    }    
        

    try:
       
        res_weather = requests.get(weather_api_url + "/current.json", params = params_weather)
    except requests.RequestException as e:
        print(f"Error conecting to Weather service: {e}",file=sys.stderr)
        sys.exit(1)

    if res_weather.status_code == 200:
        data = res_weather.json()
        temp = data.get("current", {}).get("temp_c", 0)
        condition_text = data["current"]["condition"]["text"]

        display_msg =f"Current weather in {city}: {temp}°C, Condition is {condition_text}"
        print_by_mode(app_mode, display_msg, res_weather)
    else:
            
        err_msg ="Error: Unable to fetch weather information with status code: {res_wether.status_code}"
        print_by_mode(app_mode, err_msg, res_weather )
        sys.exit(1)



def parse_arguments():
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--ip")
    parser.add_argument("-m", "--mode")
    parser.add_argument("-c", "--city")
    return parser.parse_args()


def find_city(show_city,show_ip):    
    if show_ip=="127.0.0.1":
        return "Tehran"
    elif show_city is None and show_ip is not None:
        return "London"    
    elif show_city:
        # needs to a checking city function
        return show_city
    



def main():
    args = parse_arguments()
    app_mode = os.environ.get('APP_MODE')
    ip_api_url = os.environ.get('IP_API_URL').__str__()
    weather_api_url = os.environ.get('WEATHER_API_URL')
    weather_api_key = os.environ.get('WEATHER_API_KEY')
    show_ip = args.ip
    show_mode= args.mode
    show_city=args.city

    if not show_mode:  
        app_mode = os.environ.get('APP_MODE') 
    elif show_mode=="l":
        app_mode = "local"
    elif show_mode=="p" :       
        app_mode = "Prod" 
    else: 
        app_mode = "prod"


    if show_city is not None and show_ip is not None:
        print("choose only one of two parameters for city or IP")
        sys.exit(1)
    elif not show_ip and not show_city:      
        location_data = get_location(ip_api_url, app_mode)
        city = location_data.get("city")
    else: 
        city = find_city(show_city, show_ip)


    get_weather(city, app_mode , weather_api_url, weather_api_key)


if __name__=="__main__":
    main()


