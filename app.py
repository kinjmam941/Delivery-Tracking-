from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# ShipRocket API token
SHIPROCKET_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjYyOTI4ODIsInNvdXJjZSI6InNyLWF1dGgtaW50IiwiZXhwIjoxNzQ1Mzk5NzUxLCJqdGkiOiJBYmRCWW5SYkx3bGRlaGd5IiwiaWF0IjoxNzQ0NTM1NzUxLCJpc3MiOiJodHRwczovL3NyLWF1dGguc2hpcHJvY2tldC5pbi9hdXRob3JpemUvdXNlciIsIm5iZiI6MTc0NDUzNTc1MSwiY2lkIjo1NDA3MDIzLCJ0YyI6MzYwLCJ2ZXJib3NlIjpmYWxzZSwidmVuZG9yX2lkIjowLCJ2ZW5kb3JfY29kZSI6IiJ9.NI5E9k96eXThu5Y944hNDD6EM_-I5ha2aH0ctu7Zm2Y"

def track_shipment(awb_code):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SHIPROCKET_TOKEN}"
    }

    url = f"https://apiv2.shiprocket.in/v1/external/courier/track/awb/{awb_code}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        awb_code = request.form.get("awb_code")
        tracking_data = track_shipment(awb_code)
        return render_template("result.html", data=tracking_data)
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
