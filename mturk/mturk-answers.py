import boto3
import csv
import configparser
import json
from xml.dom.minidom import parseString


def mturk_conf():
    keys = configparser.ConfigParser()
    keys.read("keys.ini")
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


def answer_number(text):
    return {
        'Very Trustworthy': 9,
        ' ': 8,
        'Trustworthy': 7,
        '  ' :6,
        'Somewhat Trustworthy': 5,
        'Somewhat Untrustworthy': 4,
        '   ': 3,
        'Untrustworthy': 2,
        '    ': 1,
        'Very Untrustworthy': 0,
    }[text]


def mturk_result(mturk):
    print("Reading from hits.txt, writting to answers.txt")
    t = open("answers.txt", "a")
    with open("hits.txt", "r") as f:
        for row_list in csv.reader(f):
            response = mturk.list_assignments_for_hit(HITId=row_list[2], AssignmentStatuses=['Submitted', 'Approved'])

            assignments = response['Assignments']
            print('The number of submitted assignments for profile {} is {}'.format(row_list[0], len(assignments)))
            for assignment in assignments:
                worker_id = assignment['WorkerId']
                assignment_id = assignment['AssignmentId']
                answer_xml = parseString(assignment['Answer'])

                # the answer is an xml document. we pull out the value of the first
                # //QuestionFormAnswers/Answer/FreeText
                answer = answer_xml.getElementsByTagName('FreeText')[0]

                # See https://stackoverflow.com/questions/317413
                only_answer = " ".join(t.nodeValue for t in answer.childNodes if t.nodeType == t.TEXT_NODE)
                json_object = json.loads(only_answer)[0]
                json_object = json_object["credibility"]

                t.write(row_list[0] + ",")
                t.write(row_list[1] + ",")
                t.write(str(answer_number(json_object["label"])) + ",")
                t.write(assignment_id + ",")
                t.write(worker_id + ",")
                t.write(row_list[2] + "\n")

                print('The Worker with ID {} submitted assignment {} for profile {} and gave the answer "{}"'.format(
                    worker_id, assignment_id, row_list[0], json_object["label"]))

                # Approve the Assignment (if it hasn't already been approved)
                if assignment['AssignmentStatus'] == 'Submitted':
                    print('Approving Assignment {}'.format(assignment_id))
                    client.approve_assignment(
                        AssignmentId=assignment_id,
                        RequesterFeedback='good',
                        OverrideRejection=False,
                    )
            print(" ")
    t.close()
    f.close()
    return


client = mturk_conf()
mturk_result(client)
