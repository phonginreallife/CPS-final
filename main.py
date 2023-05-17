from flask import Flask, request, jsonify
from flask_cors import CORS
import return_value as retu
import mqtt_public as mqtt

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
            return {
                'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },
                    'body': retu.recognize()
                } # Handle POST request with the recognize() function
  

if __name__ == '__main__':
    app.run(debug=True)