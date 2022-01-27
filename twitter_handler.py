import tas.tweets as tweetApi
def get_profile(profile_name):
    print(profile_name)
    profile = tweetApi.getSingleProfileByUsername(profile_name)
    print(profile)
    return profile

if __name__ == "__main__":    
    pass