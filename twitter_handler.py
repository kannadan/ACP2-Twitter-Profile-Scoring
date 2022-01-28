import tas.tweets as tweetApi
from common.logger import logger

def get_profile(profile_name):
    logger.info(profile_name)
    profile = tweetApi.getSingleProfileByUsername(profile_name)
    logger.info(profile)
    return profile

if __name__ == "__main__":    
    pass