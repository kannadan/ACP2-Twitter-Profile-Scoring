import boto3
import time
import datetime
import configparser


def mturk_conf():
    keys = configparser.ConfigParser()
    keys.read("own_keys.ini")
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


def mturk_create_single_hit(ht1, ht2, ht3, ht4, ht5, line, group):
    # Create hit

    question = open(file='question2.xml', mode='r').read() % (ht1, ht2, ht3, ht4, ht5)

    time.sleep(1)  # to prevent "ThrottlingException": Rate exceeded
    new_hit = client.create_hit(
        Title='How trustworthy Twitter profile is?',
        Description='See twitter profile and tweets. On scale 1 to 10, choose how much you trust those.',
        Keywords='text, quick, labeling, Twitter',
        Reward='0.10',
        MaxAssignments=5,                   # max assignment per hit
        LifetimeInSeconds=172800,           # hit availability time 345600 - 4d, 900 - 15min
        # LifetimeInSeconds=900,            # 172800 - 2 days
        AssignmentDurationInSeconds=900,
        AutoApprovalDelayInSeconds=345600 + group,
        Question=question,
        RequesterAnnotation=line,
    )
    return new_hit


def mturk_hits(profilelist, group_size):
    # Reading from list.txt, writing to hits.csv

    hits_time = datetime.datetime.now().__str__()[:-7]
    hits_file = hits_time.replace(".", "")
    hits_file = hits_file.replace(" ", "_")
    hits_file = "hits_%s.csv" % hits_file.replace(":", "")

    t = open(hits_file, "a")
    group = 0
    c1 = 0
    with open(profilelist, "r") as f:
        for line in f:
            line = line.rstrip('\n')
            link = "https://mturk-critical.s3.eu-central-1.amazonaws.com/junhao-dataset/" + line

            # hyperlink_format = '<a href="{link}">{text}</a>'
            # hyperlink_format.format(link=link", text="Profile Link")
            ht1 = " "

            hyperlink_format = '<img src="{link}" alt="{text}">'

            ht2 = hyperlink_format.format(link=link + "_profile.png", text="Profile")
            ht3 = hyperlink_format.format(link=link + "_tweet_1.png", text="Tweet 1")
            ht4 = hyperlink_format.format(link=link + "_tweet_2.png", text="Tweet_2")
            ht5 = hyperlink_format.format(link=link + "_tweet_3.png", text="Tweet 3")

            new_hit = mturk_create_single_hit(ht1, ht2, ht3, ht4, ht5, line, group)

            c1 += 1
            if c1 > group_size:
                group += 1
                c1 = 0

            t.write(line + ",")
            t.write(new_hit['HIT']['HITId'] + ",")
            t.write(new_hit['HIT']['HITGroupId'] + ",")
            t.write("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'] + "\n")
    t.close()
    f.close()
    return


if __name__ == "__main__":
    client = mturk_conf()
    mturk_hits("random_100_idlist.txt", 110)
    # mturk_hits("list.txt", 100)
