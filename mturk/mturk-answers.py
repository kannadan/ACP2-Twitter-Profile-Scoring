import boto3
import csv
import configparser
import json
import datetime
import time
from xml.dom.minidom import parseString


def mturk_conf():
    keys = configparser.ConfigParser()
    keys.read("own_keys.ini")
    region_name = keys.get("mturk", "region_name")
    aws_access_key_id = keys.get("mturk", "aws_access_key_id")
    aws_secret_access_key = keys.get("mturk", "aws_secret_access_key")
    endpoint_url = keys.get("mturk", "endpoint_url")

    client = boto3.client(
        'mturk',
        endpoint_url=endpoint_url,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    return client


def auto_approve_hits(client, assignment_id, process_time):
    # Approve the Assignment (if it hasn't already been approved)
    if process_time >= 15:
        # 'Approving Assignment
        client.approve_assignment(
            AssignmentId=assignment_id,
            RequesterFeedback='good',
            OverrideRejection=False,
        )
    else:
        # Rejecting Assignment
        client.reject_assignment(
            AssignmentId=assignment_id,
            RequesterFeedback='auto reject, too short process time: %s s. Minimum is 15 s' % str(process_time),
        )


def mturk_result(mturk, hits_file):
    # Reading from hits.csv, writing to answers.json
    result_time = datetime.datetime.now().__str__()[:-7]
    result_file = result_time.replace(".", "")
    result_file = result_file.replace(" ", "_")
    result_file = "answers_%s.json" % result_file.replace(":", "")
    t = open(result_file, "a")
    t.write('{"results %s": [' % result_time)
    t.write("\n")
    first = True
    with open(hits_file, "r") as f:
        for row_list in csv.reader(f):
            time.sleep(1)  # to prevent "ThrottlingException": Rate exceeded
            response = mturk.list_assignments_for_hit(HITId=row_list[1], AssignmentStatuses=['Submitted', 'Approved'])
            assignments = response['Assignments']
            # 'The number of submitted assignments for profile {} is {}'.format(row_list[0], len(assignments)))
            x = 1
            for assignment in assignments:
                worker_id = assignment['WorkerId']
                assignment_id = assignment['AssignmentId']
                answer_xml = parseString(assignment['Answer'])

                accept_time = assignment['AcceptTime']
                submit_time = assignment['SubmitTime']
                time_difference = submit_time - accept_time
                time_difference = time_difference.total_seconds()
                assignment_status = assignment['AssignmentStatus']

                # the answer is a xml document. we pull out the value of the first
                # //QuestionFormAnswers/Answer/FreeText
                answer = answer_xml.getElementsByTagName('FreeText')[0]
                # See https://stackoverflow.com/questions/317413
                only_answer = " ".join(t.nodeValue for t in answer.childNodes if t.nodeType == t.TEXT_NODE)
                json_object = json.loads(only_answer)[0]
                dictionary = {
                    "twitter_ID": row_list[0],
                    "profile_score1": int(list(json_object["profile_score1"].keys())
                                          [list(json_object["profile_score1"].values()).index(True)]),
                    "profile_score2": int(list(json_object["profile_score2"].keys())
                                          [list(json_object["profile_score2"].values()).index(True)]),
                    "tweet_score1": int(list(json_object["tweet_score1"].keys())
                                        [list(json_object["tweet_score1"].values()).index(True)]),
                    "tweet_score2": int(list(json_object["tweet_score2"].keys())
                                        [list(json_object["tweet_score2"].values()).index(True)]),
                    "tweet_score3": int(list(json_object["tweet_score3"].keys())
                                        [list(json_object["tweet_score3"].values()).index(True)]),
                    "HIT_ID": row_list[1],
                    "assignment_id": assignment_id,
                    "worker_id": worker_id,
                    "assignment count": x,
                    "assignments": len(assignments),
                    "assignment status": assignment_status,
                    "accept time": accept_time.strftime("%Y-%m-%d, %H:%M:%S"),
                    "submit time": submit_time.strftime("%Y-%m-%d, %H:%M:%S"),
                    "assignment process time": time_difference
                }
                x += 1
                if first:
                    first = False
                else:
                    t.write(",\n")

                t.write(json.dumps(dictionary))
                if assignment['AssignmentStatus'] == 'Submitted':
                    auto_approve_hits(mturk, assignment_id, time_difference)

    t.write("]}\n")
    t.close()
    f.close()
    return


if __name__ == "__main__":
    client = mturk_conf()
    mturk_result(client, "hits_2022-03-01_011727.csv")
    # mturk_result(client, "hits.txt")
