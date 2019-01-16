# Scripts to convert 1) cochrane annotation csv files to json


import csv

from src import helper


# COCHRANE QUESTIONS CONVESRION
csv_file = open('resources/data/annotations/csv/COCHRANE_QUESTION_DEFINITIONS_FINAL.csv', 'r')
reader = csv.reader(csv_file)
fieldnames = next(reader)

question_def_dict = {}
reader = csv.DictReader( csv_file, fieldnames)
for row in reader:
    question_def_dict[row["TASK_ID_PK"]] = row
    question_def_dict[row["TASK_ID_PK"]].pop("TASK_ID_PK", None)

helper.dump_json_to_file('resources/data/annotations/json/COCHRANE_QUESTION_DEFINITIONS.json', question_def_dict)
csv_file.close()


# URL DOMAIN CONVESRION
csv_file = open('resources/data/annotations/csv/ALL_URL_DOMAIN_METADATA_v_1.0.csv', 'r')
reader = csv.reader(csv_file)
fieldnames = next(reader)

url_domain_dict = {}
reader = csv.DictReader( csv_file, fieldnames)
for row in reader:
    url_domain_dict[row["BASE_DOMAIN_PK"]] = row
    url_domain_dict[row["BASE_DOMAIN_PK"]].pop("BASE_DOMAIN_PK", None)

helper.dump_json_to_file('resources/data/annotations/json/ALL_URL_DOMAIN_METADATA.json', url_domain_dict)
csv_file.close()


# PAIN IN ASS.... needed to add title... there is some strange character in first postion of CSV...hence the correction
# of field name 0
# The file name is now XLS_JUDGMENTS_HELPFUL
csv_file = open('resources/data/annotations/csv/ALL_JUDGMENTS_v_1.csv', 'r')
reader = csv.reader(csv_file)
fieldnames = next(reader)
fieldnames[0] = 'UNIQUE_ID_PK'
print(fieldnames)
judgment_dict = {}
# needs to be format {task id: [{everything else}}}
reader = csv.DictReader( csv_file, fieldnames)
i = 1
for row in reader:
    print(i)
    i+=1
    judgment_dict[row["UNIQUE_ID_PK"]] = row
    judgment_dict[row["UNIQUE_ID_PK"]].pop("UNIQUE_ID__PK", None)

helper.dump_json_to_file('resources/data/annotations/json/ALL_JUDGMENTS_HELPFUL.json', judgment_dict)
csv_file.close()


import config
from src import helper
from nltk.tokenize import sent_tokenize
all_sent = sent_tokenize("Hello world.  Goodbye World!")
print (all_sent)
all_sent.join('a')


# Remove extra sentences from snippets and resave file
annotations = helper.load_json_from_file(config.JUDGMENTS_PATH)
for id in annotations.keys():
    snippet = annotations[id]['SNIPPET']
    print(id)
    print(len(annotations[id]['SNIPPET']))
    snippet_sentences = sent_tokenize(snippet)
    print(len(snippet_sentences))
    annotations[id]['SNIPPET'] = ' '.join(snippet_sentences[0:2])
    print(len(annotations[id]['SNIPPET']))

helper.dump_json_to_file(config.JUDGMENTS_PATH, annotations)


