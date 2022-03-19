"""
:author: 0xb301
:version: 3.9.6

:begin: 18/03/2022
:end: ??/??/????
"""


import flask
import hashlib
import classes.ciphers


app = flask.Flask(__name__)


@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def index():
    if flask.request.method == "GET":
        return flask.render_template("index.html")


@app.route("/8d9fb6d780c63ed73fd39c61391b4bac619ed37bcd7272f4fc8c5d78c8c20d27", methods=["GET", "POST"])
def the_post_office():    
    if flask.request.method == "GET":
        return flask.render_template("the_post_office.html")
    elif flask.request.method == "POST":
        data = dict(flask.request.values)
        print(data, flask.request.values)
        if "Animal" in data.keys():
            if data["Animal"] == "Quokka":
                return "Well done! "
        return "Too bad!"
    return "?"


@app.route("/1e30adb19df164cea9015f9d4819cb67e1e87ea88ec63b26c7dfba48f30bb434", methods=["GET"])
def quokka():
    return flask.send_file("./static/assets/quokka.jpeg", mimetype="image/jpeg")


@app.route("/robots", methods=["GET"])
@app.route("/robots.txt", methods=["GET"])
def robots():
    return flask.send_file("./static/assets/robots.txt", mimetype="text/plain")


# Hashes
@app.route("/md5", methods=["GET", "POST"])
@app.route("/md5.html", methods=["GET", "POST"])
def md5():
    if flask.request.method == "GET":
        return flask.render_template("md5.html")
    elif flask.request.method == "POST":
        data = dict(flask.request.values)
        hash = ""
        if "pre-hash" in data.keys():
            if data["pre-hash"] != '':
                hash = hashlib.md5(data["pre-hash"].encode()).hexdigest()
                return flask.render_template("md5.html", data=hash)
            return flask.redirect(flask.url_for("md5"))

@app.route("/sha256", methods=["GET", "POST"])
@app.route("/sha256.html", methods=["GET", "POST"])
def sha256():
    if flask.request.method == "GET":
        return flask.render_template("sha256.html")
    elif flask.request.method == "POST":
        data = dict(flask.request.values)
        if "pre-hash" in data.keys():
            if "pre-hash" in data.keys():
                hash = hashlib.sha256(data["pre-hash"].encode()).hexdigest()
                return flask.render_template("sha256.html", data=hash)
            return flask.redirect(flask.url_for("sha256"))
            


@app.route("/devops", methods=["GET"])
def devops():
    return flask.render_template("devops.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    def __check_extension(name: str):
        ALLOWED = ["txt", "jpg", "jpeg", "png", "wav", "mp4", "mp3"]
        if '.' not in name or name.split('.')[-1] not in ALLOWED or len(name.split('.')) < 2:
            return False
        return True

    if flask.request.method == "GET":
        return flask.render_template("upload.html")
    elif flask.request.method == "POST":
        data = dict(flask.request.files)
        if "file-name" in data.keys():
            file = data["file-name"]
            if file.filename == "":
                return flask.redirect(flask.url_for("upload"))
            if __check_extension(file.filename):
                try:
                    with open(f"static/uploads/{file.filename}", 'wb') as f:
                        f.write(file.read())
                    return flask.redirect(flask.url_for("upload"))
                except:
                    return flask.render_template("upload.html", data="Failure .. file exits already")
            return flask.render_template("upload.html", data=f"Failure .. doesn't accept {file.filename.split('.')[-1]}")
        return "404"


# Ciphers
@app.route("/playfair", methods=["GET", "POST"])
@app.route("/playfair.html", methods=["GET", "POST"])
def playfair():
    if flask.request.method == "GET":
        return flask.render_template("ciphers/playfair.html")
    elif flask.request.method == "POST":
        data = dict(flask.request.values)
        if set(data.keys()) ==  {"mode", "string", "key"}:
            if data["key"] == '' or data["string"] == '':
                return flask.render_template("ciphers/playfair.html", data="Please fill all the fields...")
            result = classes.ciphers.playfair(message=data["string"], keyword=data["key"], mode=data["mode"])
            if data["mode"] == "decode":
                return flask.render_template("ciphers/playfair.html", data=result[0], var=result[1])
            return flask.render_template("ciphers/playfair.html", data=result)
        return flask.redirect(flask.url_for("playfair"))


@app.route("/temp", methods=["GET"])
def temp():
    return "Who cares?"


if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
