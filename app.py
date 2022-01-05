from flask import Flask, jsonify, request, render_template
from model import MNISTModel
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
ALLOW_FILE_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    file_ext = filename.split('.')[-1]
    if file_ext in ALLOW_FILE_EXTENSIONS:
        return True
    else:
        return False


try:
    model_path = os.path.join("model", "mnist_cnn_model.h5")
    mnist_model = MNISTModel(model_path)
except Exception as e:
    print(f"[ERROR] {e}")


@app.route("/", methods=["GET",  "POST"])
def index():
    if request.method == "GET":
        return jsonify({'GET_Reqest': "http://url/", "POST_Reqest": "http://url"})

    if request.method == "POST":
        # check if the post request has the file part
        if 'files[]' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp

        files = request.files.getlist('files[]')

        data = {}
        success = False
        predictions = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                global mnist_model
                prediction = mnist_model.predict(file)
                predictions.append(
                    [{"filename": f"{filename}", "prediction": f"{prediction}"}])
                success = True
            else:
                data[file.filename] = 'File type is not allowed'

        if success:
            data['result'] = predictions
            resp = jsonify([{'message': 'Files successfully uploaded'}, data])
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(data)
            resp.status_code = 500
            return resp


if __name__ == '__main__':
    app.run()
