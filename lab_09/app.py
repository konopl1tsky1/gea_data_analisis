from flask import Flask, jsonify, request
import rasterio
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/get_image_box', methods=['GET'])
@cross_origin()
def get_image_box():
    try:
        dataset = rasterio.open(r'../images_data/soil_moisture.tif')
        dataset.close()
        return jsonify(dataset.bounds)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'})


@app.route('/get_moisture_value/lng=<float:lng>/lat=<float:lat>', methods=['GET'])
@cross_origin()
def get_moisture_value(lng, lat):
    try:
        dataset = rasterio.open(r'../images_data/soil_moisture.tif')
        try:
            index = dataset.index(lng, lat)
            array = dataset.read(1)
            moisture = array[index]
            dataset.close()
            return jsonify({'moisture': int(moisture)})
        except ValueError:
            return jsonify({'moisture': 'no data'})
    except FileNotFoundError:
        return jsonify({'error': 'File not found'})


if __name__ == '__main__':
    app.run(debug=True)
