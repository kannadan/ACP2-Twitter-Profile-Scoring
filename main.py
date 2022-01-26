from flask import Flask, request, jsonify, render_template
import db
import twitter_handler as th
import os
from dotenv import load_dotenv
from ml.model_inference import query_model

# ENVIRONMENT VARIABLES
load_dotenv()
TWITTER_API = os.getenv('TWITTER_API')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

app = Flask(__name__,
            static_url_path='',
            static_folder="twitter-rater-ui/dist",
            template_folder='./twitter-rater-ui/dist')
app.config["DEBUG"] = True

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

        #score profile
        # score, explanations = query_model(profile)
        # profile["ml_output"] = {
        #     "score": score,
        #     "explanations": explanations
        # }

        #build response        
        response = jsonify(profile)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response 
    else: 
        return "Username not given", 400

@app.route("/api/ProfileSearch", methods=['POST'])
def search_profiles():    
    # parameters => search=<profile search term> application/x-www-form-urlencoded 
    print(request.form.get("search"))
    return jsonify([
        {"name": "person1", "id": 123},
        {"name": "person2", "id": 456}
    ])

if __name__ == "__main__":        
    app.run(host='0.0.0.0')
