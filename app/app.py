import logging
import pickle
import re
import traceback

from concurrent_log_handler import ConcurrentRotatingFileHandler
from flask import Flask, request, jsonify, make_response, render_template, url_for
import pickle
from schema import SchemaError
from datetime import datetime

from settings import *
from helpers import features, validation
from utils import files

app = Flask(__name__)
model = None
time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

#####################################################################################
################################### ROUTES ##########################################
#####################################################################################


@app.route('/<version>/healthcheck', methods=['GET'])
def healthcheck(version):
    if models.get(version, None) is not None:
        return ("OK", 200)
    else:
        return ("Not OK", 200)


@app.route('/<version>/predict',methods=['POST', 'GET'])
def predict(version):

    collection = {"id": None }
    rounded_prediction = None
    if request.method == 'GET':
        return render_template('index.html',version=version)
        #collection = request.form.to_dict()
    elif request.method == 'POST':
        if models.get(version, None) is not None:
            if request.form is not None:
                #collect = request.form.to_dict(flat=True)
                collection = {}
                collection['year'] = int(request.form.get('year'))
                collection['mileage'] = int(request.form.get('mileage'))
                collection['id'] = request.form.get('id')
                collection['manufacturer'] = request.form.get('manufacturer')
                collection['sec_status'] = request.form.get('sec_status')
                #collection = jsonify(collection)

                validation.validate("predict", collection)

                feature_vector = features.make_feature_vector(collection)

                prediction = models[version].predict(feature_vector)

                rounded_prediction = int(prediction)

                rounded_prediction = '₦' + f"{rounded_prediction:,}"

                #output = make_response((jsonify({'id': collection["id"], 'prediction': rounded_prediction,
                 #                           'model_version' : version , 'date' : time }))) 
                
                return render_template('result.html', prediction_text= "{}" 
                                                                            .format(collection['id']), 
                                                                            prediction_text2= "{}"
                                                                            .format(rounded_prediction),
                                                                            prediction_text3= "{}"
                                                                            .format(version), 
                                                                            prediction_text4= "{}"
                                                                            .format(time),
                                                                            prediction_text5= "{}"
                                                                            .format(collection['sec_status']),
                                                                            prediction_text6= "{}"
                                                                            .format(collection['mileage']),
                                                                            prediction_text7= "{}"
                                                                            .format(collection['manufacturer']),
                                                                            prediction_text8= "{}"
                                                                            .format(collection['year']))


                #{'Car ID': collection['id'], 'Car Price': rounded_prediction,
                    #'Model Version' : version ,'Timestamp' : time }

@app.route('/<version>/predict_api', methods=['POST'])
def predict_api(version):
    if models.get(version, None) is not None:

        try:

            collection = request.get_json(force=True)

            validation.validate("predict", collection)

            feature_vector = features.make_feature_vector(collection)

            prediction = models[version].predict(feature_vector)

            rounded_prediction = int(prediction)

            rounded_prediction = '₦' + f"{rounded_prediction:,}"

            return make_response((jsonify({'id': collection["id"], 'prediction': rounded_prediction,
                                            'model_version' : version , 'date' : time }))) 

        except SchemaError as ex:
            return make_response(jsonify({"message": ex.errors}), 400)

    else:
        return make_response(jsonify({"message": "Trained model version '{}' was not found.".format(version)}), 404)


@app.after_request
def after_request(response):
    # 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        app.logger.info('%s %s %s %s %s',
                        request.remote_addr,
                        request.method,
                        request.scheme,
                        request.full_path,
                        response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()

    resp = "Internal Server Error", 500

    app.logger.error('%s %s %s %s 5XX INTERNAL SERVER ERROR\n%s',
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)

    return resp


#####################################################################################
############################### INTIALIZATION CODE ##################################
#####################################################################################

if __name__ == '__main__':
    try:
        port = int(PORT)
    except Exception as e:
        print("Failed to bind to port {}".format(PORT))
        port = 80

    pattern = '^.+\-(v\d+)\.p$'

    models_available = files.get_files_matching(MODELS_ROOT, '^.+\-v\d+\.p$')

    models = dict()

    # load the models to memory only once, when the app boots
    for path_to_model in models_available:
        version_id = re.match(pattern, path_to_model).group(1)
        models[version_id] = pickle.load(open(path_to_model, "rb"))

    # 10M = 1024*1000*10 bytes
    handler = ConcurrentRotatingFileHandler(LOG_FILE, maxBytes=1024 * 1000 * 10, backupCount=5, use_gzip=True)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    # https://stackoverflow.com/a/20423005/436721
    app.logger.setLevel(logging.INFO)

    app.run(port=port , debug = True)

else:
    pattern = '^.+\-(v\d+)\.p$'

    models_available = files.get_files_matching(MODELS_ROOT, '^.+\-v\d+\.p$')

    models = dict()

    # load the models only once, when the app boots
    for path_to_model in models_available:
        version_id = re.match(pattern, path_to_model).group(1)
        with open(path_to_model,"rb") as f:

            models[version_id] = pickle.load(f)

    # disable logging so it doesn't interfere with testing
    app.logger.disabled = True
