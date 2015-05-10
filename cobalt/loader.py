import sys
import requests
import constants

def load_initial_data(csv_file):
    print csv_file
    uri=constants.API_URL + '/questions'
    line=None
    question_data=[]
    isfirst=True
    with open(csv_file, 'r') as F:
        for line in F:
            if isfirst:
                isfirst = False
                continue
            line=line.strip()
            (question, answer, distractors)=line.split('|')
            distractor_list=[d for d in distractors.split(',') if d]
            question_dict={'question':question,
                           'answer':answer,
                           'distractor': distractor_list}
            question_data.append(question_dict)
     
    for question in question_data:
        print "POSTing data for question {}".format(question['question'])
        response=requests.post(uri, data=question)
        if response.status_code != 201:
            raise Exception("Failed to POST data for question : {}".format(question));

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Name of seed data file required")
        sys.exit(1)
    try:
        load_initial_data(sys.argv[1])
    except Exception as e:
        sys.stderr.write(e.message)

