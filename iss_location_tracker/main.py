import os
import requests
import smtplib
from datetime import datetime

# PythonAnywhere allows you to set these securely in the dashboard or web app setup
MY_LAT = 29.453546  
MY_LONG = 77.312581  
MY_EMAIL = os.environ.get("MY_EMAIL", "hashiramasenju2025@gmail.com")
MY_PASSWORD = os.environ.get("MY_PASSWORD")  # Hidden for security


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.utcnow().hour  

    if time_now >= sunset or time_now <= sunrise:
        return True
    return False


# Execution block (No "while True" loop needed for a scheduled task)
if is_iss_overhead() and is_night():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up!😀😀(●'◡'●)\n\nThe ISS is above you in the sky right now - go look!"
        )