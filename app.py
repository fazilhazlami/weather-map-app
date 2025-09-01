from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API key dari OpenWeatherMap
API_KEY = "8ebb4c7a15949d2393fceea6304cc82e"  # ganti dengan API key kamu
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric",
                "lang": "id"
            }
            try:
                response = requests.get(BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                weather_data = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"]
                }
            except requests.exceptions.HTTPError:
                weather_data = {"error": "⚠️ Kota tidak ditemukan!"}
            except requests.exceptions.ConnectTimeout:
                weather_data = {"error": "⚠️ Timeout! Gagal terhubung ke server cuaca."}
            except requests.exceptions.RequestException as e:
                weather_data = {"error": f"⚠️ Terjadi kesalahan: {e}"}

    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
