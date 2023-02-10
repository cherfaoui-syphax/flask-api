from flask import Flask, request, render_template , flash , redirect , url_for , send_from_directory
import re
import os
import os.path
from werkzeug.utils import secure_filename
from flask import json 

import src.cermine as CERMINE
UPLOAD_FOLDER = './pdfs'
ALLOWED_EXTENSIONS = {'pdf'}




app = Flask(__name__, static_folder='static', template_folder='templates')


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Flask Dockerized'



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/cermine', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.system('java -cp ./cermine_jar/cermine-impl-1.13-jar-with-dependencies.jar pl.edu.icm.cermine.ContentExtractor -path "./pdfs" -outputs zones ')
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #Le chemin vers le fichier que donne sermine
            cermine_file = os.path.join(app.config['UPLOAD_FOLDER'], filename.replace('pdf', 'cermzones'))


            #os.remove(cermine_file)
            #return render_template('result.html', data=data)
            return str(CERMINE.extract_cermine(cermine_file))
            return send_from_directory(cermine_file)
    return send_from_directory("./templates", "upload.html")



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')