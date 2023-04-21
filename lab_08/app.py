from flask import Flask, jsonify
import geopandas
import json

app = Flask(__name__)
	
@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/get_json/<string:filename>', methods=['GET'])
def get_json(filename):
    try:
        with open(filename + '.json', 'r') as file:
            json_data = file.read()
            return jsonify(json_data)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'})

@app.route('/field/<string:field_name>', methods=['GET'])
def get_field(field_name):
    field_data = geopandas.read_file("../images_data/lab_06/field_data.geojson")
    result = (field_data.loc[field_data['name'] == field_name])
    json_result = result.to_json(default=lambda x: x.__geo_interface__)
    return jsonify(json_result)

if __name__ == '__main__':
    app.run(debug=True)