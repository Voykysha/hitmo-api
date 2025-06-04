from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route("/hitmo", methods=["GET"])
def hitmo_search():
    song = request.args.get("q")
    if not song:
        return jsonify({"error": "No song name provided"}), 400

    link = "https://rus.hitmotop.com/search?q=" + "+".join(song.split())
    r = requests.get(link)
    bs = BeautifulSoup(r.text, "html.parser")

    result = []
    tracks = bs.find_all("li", {"class": "tracks__item"})

    if tracks:
        track = tracks[0]  # первая ссылка
        title = track.find("div", {"class": "track__title"}).text.strip()
        artist = track.find("div", {"class": "track__desc"}).text.strip()
        length = track.find("div", {"class": "track__fulltime"}).text.strip()
        dlink = track.find("a", {"class": "track__download-btn"})['href']
        result.append({
            "title": title,
            "artist": artist,
            "length": length,
            "download_link": dlink
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

