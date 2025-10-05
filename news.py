from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_KEY = "b2a1492c0041b2f02ff9f715c378755a"  # your Mediastack API key

# Countries to show
COUNTRIES = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Canada": "ca",
    "Australia": "au",
    "Germany": "de",
    "France": "fr",
    "Italy": "it",
    "Japan": "jp",
    "China": "cn",
    "Brazil": "br",
    "Russia": "ru",
    "South Africa": "za",
    "Mexico": "mx",
    "UAE": "ae"
}

# Store community-submitted news
community_articles = []

@app.route("/", methods=["GET"])
def home():
    country = request.args.get("country", "in")
    url = f"http://api.mediastack.com/v1/news?access_key={API_KEY}&countries={country}&limit=20"
    response = requests.get(url)
    data = response.json()

    articles = []
    if "data" in data:
        for entry in data["data"]:
            articles.append({
                "title": entry.get("title"),
                "description": entry.get("description"),
                "url": entry.get("url"),
                "image": entry.get("image")
            })

    # Trending = first 3 articles
    trending = articles[:3]

    return render_template(
        "index.html",
        articles=articles,
        trending=trending,
        country=country,
        countries=COUNTRIES
    )

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        url = request.form.get("url")
        image = request.form.get("image")

        community_articles.append({
            "title": title,
            "description": description,
            "url": url,
            "image": image
        })

        return redirect(url_for("community"))
    return render_template("submit.html")

@app.route("/community")
def community():
    return render_template("community.html", articles=community_articles)

if __name__ == "__main__":
    app.run(debug=True)



