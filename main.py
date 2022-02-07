from flask import Flask, request, jsonify, render_template, Response
import db
import twitter_handler as th
import os
from dotenv import load_dotenv
from ml.model_inference import query_model
from common.logger import logger
from flask_cors import CORS
import csv
import os.path


# ENVIRONMENT VARIABLES
load_dotenv()
TWITTER_API = os.getenv('TWITTER_API')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

app = Flask(__name__,
            static_url_path='',
            static_folder="twitter-rater-ui/dist",
            template_folder='./twitter-rater-ui/dist')
app.config["DEBUG"] = True
CORS(app)

test_profile = {
    "name": "Test user",
    "score": 9.9,
    "tweets": 232
}

@app.route("/", methods=['GET'])
def entry_point():
    return render_template('index.html')


@app.route("/api/GetProfile", methods=['GET'])
def get_profile_data():
    username = request.args.get('username')
    if username != None:
        # fetch profile data from twitter api        
        profile = th.get_profile(username)
        print(profile)
        if profile != None:
            #score profile
            try:
                score, explanations = query_model(profile)
                profile["ml_output"] = {
                    "score": score,
                    "explanations": explanations
                }
            except Exception as e:
                logger.error(f"Model query failed: {e}")
                profile["ml_output"] = None

            #build response        
            response = jsonify(profile)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response 
        else:
            return "Username not given", 404    
    else: 
        return "Username not given", 400

@app.route("/api/SaveResults", methods=['POST'])
def post_user_session():        
    print("GOT SAVE DATA")
    content = request.json
    print(content["userId"])
    write_to_file(content)

    resp = Response('{}', status=201)
    resp.headers["Content-type"] = "application/json"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    print(resp.headers)
    return resp

def write_to_file(profile):
    log_headers = ["User Id", "Twitter username", "Twitter id", "Evaluation Score"]
    data = [profile["userId"], profile["username"], profile["id"], profile["ml_output"]["score"]]
    headers = False
    if os.path.isfile('UserLogs.csv'):
        headers = True
    with open('UserLogs.csv', 'a') as file:
        writer = csv.writer(file)
        if not headers:
            writer.writerow(log_headers)    
        writer.writerow(data)

if __name__ == "__main__":        
    app.run(host='0.0.0.0')
