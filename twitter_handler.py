import tas.tweets as tweetApi
def get_profile(profile_name):
    print(profile_name)
    profile = tweetApi.getProfileByUsername(profile_name)
    return profile

if __name__ == "__main__":    
    pass