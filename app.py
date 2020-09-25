from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from engine import parseJMX
from engine import validateJMX, createJSON
from engine import cleanup
import json

import os

UPLOAD_FOLDER='uploads'
ALLOWED_EXTENSIONS = {'jmx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config["ALLOWED_JMX_EXTENSIONS"] = ["JMX"]

cleanup()
createJSON()

@app.route('/')
def home():
    #print(os.path.abspath(UPLOAD_FOLDER))
    return render_template('home.html')

def allowed_jmx(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_JMX_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/', methods=['POST'])
def upload():
    if request.method == 'POST':
        if request.files:
            file = request.files['file']
            if allowed_jmx(file.filename):                
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
                jmxFile = os.path.abspath(app.config["UPLOAD_FOLDER"] + '\\' + file.filename)
                parseJMX(jmxFile)
                return redirect('result')
            else:
                print("Extension not allowed")
                return redirect(request.url)
    return


@app.route('/result', methods=['POST', 'GET'])
def result():
    with open("./output/output.json","r") as f:
        print("Inside results")
        data = json.loads(f.read())
    #return '''
    #The value is {}
    #'''.format(data)
    return render_template('result.html', string=data)

if __name__ == '__main__':
    app.run(debug=True)
