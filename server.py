import logging
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import skimage.io as io

#from src.feature_extractors import hist_ext
from src.parsers import v1image_parser
from src.indexes import es_index

#cnn_extractor = hist_ext.HistogramExtractor()

parser = v1image_parser.V1ImageParser()

esIndex = es_index.ESIndex('elasticsearch:9200')


PORT = 8081

app = Flask(__name__)
CORS(app)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logging.info('Flask server initialized on port ' + str(PORT))

@app.route('/')
def index():
    ''' Index route '''
    return 'Server is alive!'

@app.route('/search', methods=['POST'])
def search():

    data = request.get_json()

    img = data['image'].split(',', 1)[1]
    file_ending = data['file_ending']
    feature = data['feature']
    evaluation = data['evaluation']

    file_name = 'tmp.' + file_ending

    img_data = base64.b64decode(img)
    with open(file_name, 'wb') as f:
        f.write(img_data)

    query = parser.prepare_query(io.imread(file_name))[feature]

    query_dict = {'doc_name': None, 'features': query}

    query_response = esIndex.query_index(query_dict, evaluation, feature)

    return jsonify(query_response)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.debug('flask app debug logging enabled')
    app.run(host='0.0.0.0', port=PORT, debug=True)

