from app import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def loginScreen():
    return render_template("login.html")