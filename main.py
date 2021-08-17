from flask import Flask, render_template, request, url_for
from pytube import YouTube
from pydub import AudioSegment as AS
import os
import string
from random import randrange

app = Flask(__name__)

def random_string(length):
	res = ""
	bank = string.ascii_uppercase + string.ascii_lowercase + string.digits
	for i in range(length):
		res += bank[randrange(len(bank))]
	return res

@app.route("/", methods=["POST", "GET"])
def index():
	if "url" in request.form:
		try:
			yt = YouTube(request.form.get("url"))

			converted_filename = "static/" + yt.title + ".mp3"
			temp_filename = random_string(32)

			if not os.path.isfile(converted_filename):
				stream = yt.streams.get_by_itag(251)
				stream.download(output_path="static", filename=temp_filename)

				webm = AS.from_file("static/" + temp_filename)
				webm.export(converted_filename, format="mp3")

				os.remove("static/" + temp_filename)

			return render_template("index.html", state="valid_link", video=yt, download_url=converted_filename)
		except Exception as e:
			print(e)
			return render_template("index.html", state="invalid_link")
	else:
		return render_template("index.html", state="no_link")

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")