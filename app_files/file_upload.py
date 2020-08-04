from flask import Flask, render_template
from flask import request, redirect
import os
# import google.cloud.storage
from google.api_core.protobuf_helpers import get_messages
from google.cloud import storage
from werkzeug.datastructures import ImmutableMultiDict

print('Credentials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

config={}
config["FILE_UPLOADS"]="C:\\Users\\Tejaswa\\flask-multiple-file-upload\\official_tut\\gcsfu\\dropped_files\\"
# config["bucket_name"]="sample-audio-humanity"

app = Flask(__name__)

def gcs_upload(filename, bucket_name, source_path):
    print("GCS UPLOAD VARIABLES")
    print(filename)
    print(bucket_name)
    print(source_path)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)

    blob.upload_from_filename(source_path+filename)

    print("File {} uploaded to {}.".format(source_path+filename, filename))

def delete_after_uploading():
    pass

@app.route("/uploadscreen", methods=["GET", "POST"])
def upload_file():

    gcs_contents={'sample-audio-humanity': ['Arnab Goswami 5 Kickass Newshour Debates That Ruled 9pm Indian TV News (online-audio-converter.com).wav', 'How to Design Impenetrable Airport Security (mp3cut.net).mp3', 'Who Is Playing Into The Hands Of China Arnab Goswami Debates On The China Gang (mp3cut.net).mp3', 'Who Is Playing Into The Hands Of China Arnab Goswami Debates On The China Gang (online-audio-converter.com).wav'], 'second_bucket_tejaswa': ['Annotation 2020-07-19 124655.png', 'gdrive_structure.png', 'thatsallfolks.jpg'], 'tejaswa_third_bucket': ['Arnab Goswami 5 Kickass Newshour Debates That Ruled 9pm Indian TV News (mp3cut.net).mp3']}

    if request.method=="POST":
        if not request.form.get("bucket_selected"):
            return
            
        if request.files:        
            bucket_selected=request.form.get("bucket_selected")

            files_dict=request.files.to_dict(flat=False)
            files_list=[]
            for file in files_dict["multi_file_selected"]:
                filename=file.filename
                files_list.append(filename)
                file.save(os.path.join(config["FILE_UPLOADS"], filename))
                gcs_upload(filename, bucket_selected, config["FILE_UPLOADS"])
                delete_after_uploading()
            return redirect(request.url)

    return render_template("public/upload_image.html", gcs_contents=gcs_contents)

if __name__ == '__main__':
   app.run(debug = True)