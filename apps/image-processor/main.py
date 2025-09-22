import os

from PIL import Image
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/images/<filename>')
def images(filename):
    return send_from_directory('images', filename)


@app.route('/output/<filename>')
def output(filename):
    return send_from_directory('output', filename)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['image']
    filename = secure_filename(file.filename)
    saved_file_name = os.path.join(os.getcwd(), "images", filename)
    file.save(saved_file_name)
    img = Image.open(saved_file_name)
    img = img.resize((300, int(img.height * 300 / img.width)))
    resized_file = os.path.join(os.getcwd(), "output", filename)
    img.save(resized_file)
    return render_template("images.html",
                           filename=filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
