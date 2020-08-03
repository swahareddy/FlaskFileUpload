from flask import Flask, render_template
from flask import request, redirect
import os

app = Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html")

@app.route('/hello/<user>')
def hello_world(user):
    return render_template('hello.html', name=user)

@app.route('/results')
def print_results():
    dict = {'phy':50,'che':60,'maths':70}
    return render_template('results.html', result=dict)


app.config["FILE_UPLOADS"]="C:\\Users\\Tejaswa\\flask-multiple-file-upload\\official_tut\\gcsfu\\dropped_files"
@app.route("/uploadscreen", methods=["GET", "POST"])
def upload_file():

    if request.method=="POST":
        if request.files:
            file_up=request.files["file_selected"]
            print(file_up)
            file_up.save(os.path.join(app.config["FILE_UPLOADS"], file_up.filename))
            print("image saved")
            return redirect(request.url)

    return render_template("public/upload_image.html")

if __name__ == '__main__':
   app.run(debug = True)