from flask import Flask, request, jsonify
import scoring
import db
import twitter_handler as th
import os
from dotenv import load_dotenv

# ENVIRONMENT VARIABLES
load_dotenv()
TWITTER_API = os.getenv('TWITTER_API')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

app = Flask(__name__)
app.config["DEBUG"] = True

test_profile = {
    "name": "Test user",
    "score": 9.9,
    "tweets": 232
}

@app.route("/api/GetProfile", methods=['GET'])
def get_profile_data():
    username = request.args.get('username')
    if username != None:
        # fetch profile data from twitter api        
        profile = th.get_profile(username)

        #score profile
        score = scoring.score_profile(profile)
        profile["score"] = score

        #save profile to database
        db.save_profile(profile)

        return jsonify(profile)
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
    app.run()