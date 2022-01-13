import boto3
import csv
import configparser


def mturk_conf():
    keys = configparser.ConfigParser()
    keys.read("keys.ini")
    region_name = keys.get("mturk", "region_name")
    aws_access_key_id = keys.get("mturk", "aws_access_key_id")
    aws_secret_access_key = keys.get("mturk", "aws_secret_access_key")
    endpoint_url = keys.get("mturk", "endpoint_url")

    mturk_client = boto3.client(
        'mturk',
        endpoint_url=endpoint_url,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    return mturk_client


def mturk_create_single_hit(ht1, ht2, ht3, ht4, ht5, line):
    # Create hit

    question = open(file='question.xml', mode='r').read() % (ht1, ht2, ht3, ht4, ht5)

    new_hit = client.create_hit(
        Title='How trustworthy Twitter profile is?',
        Description='See twitter profile and tweets and select how trustworthy you think profile is',
        Keywords='text, quick, labeling',
        Reward='0.03',
        MaxAssignments=2,
        # LifetimeInSeconds = 172800,
        LifetimeInSeconds=900,
        AssignmentDurationInSeconds=600,
        AutoApprovalDelayInSeconds=14400,
        Question=question,
        RequesterAnnotation=line,
    )
    return new_hit


def mturk_hits():
    print("Reading from list.txt, writing to hits.txt")
    t = open("hits.txt", "a")
    with open("list.txt", "r") as f:
        for line in f:
            # for link in csv.reader(f):
            line = line.rstrip('\n')
            link = "https://mturk-critical.s3.eu-central-1.amazonaws.com/junhao-dataset/" + line

            # hyperlink_format = '<a href="{link}">{text}</a>'
            # hyperlink_format.format(link=link", text="Profile Link")
            ht1 = ""

            hyperlink_format = '<img src="{link}" alt="{text}">'
            ht2 = hyperlink_format.format(link=link + "_profile.png", text="Profile")
            ht3 = hyperlink_format.format(link=link + "_tweet_1.png", text="Tweet 1")
            ht4 = hyperlink_format.format(link=link + "_tweet_2.png", text="Tweet_2")
            ht5 = hyperlink_format.format(link=link + "_tweet_3.png", text="Tweet 3")

            new_hit = mturk_create_single_hit(ht1, ht2, ht3, ht4, ht5, line)

            print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
            print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")
            t.write(line + ",")
            t.write(new_hit['HIT']['HITId'] + ",")
            t.write(new_hit['HIT']['HITGroupId'] + ",")
            t.write("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'] + "\n")
    t.close()
    f.close()
    return


client = mturk_conf()
mturk_hits()
