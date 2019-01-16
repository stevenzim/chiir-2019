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
csv_file = open('resources/data/annotations/csv/URL_DOMAIN_METADATA_HELPFUL_v_FINAL.csv', 'r')
reader = csv.reader(csv_file)
fieldnames = reader.next()

url_domain_dict = {}
reader = csv.DictReader( csv_file, fieldnames)
for row in reader:
    url_domain_dict[row["BASE_DOMAIN_PK"]] = row
    url_domain_dict[row["BASE_DOMAIN_PK"]].pop("BASE_DOMAIN_PK", None)

helper.dump_json_to_file('resources/data/annotations/json/URL_DOMAIN_METADATA.json', url_domain_dict)
csv_file.close()


# PAIN IN ASS.... needed to add title... there is some strange character in first postion of CSV...hence the correction
# of field name 0
# The file name is now XLS_JUDGMENTS_HELPFUL
csv_file = open('resources/data/annotations/csv/XLS_JUDGMENTS_HELPFUL_v_FINAL.csv', 'r')
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

helper.dump_json_to_file('resources/data/annotations/json/JUDGMENTS_HELPFUL.json', judgment_dict)
csv_file.close()

# # JUDGMENTS HELPFUL CONVESRION
# csv_file = open('resources/data/annotations/csv/JUDGMENTS_HELPFUL_v_FINAL.csv', 'r')
# reader = csv.reader(csv_file)
# fieldnames = reader.next()
#
# judgment_dict = {}
# # needs to be format {task id: [{everything else}}}
# reader = csv.DictReader( csv_file, fieldnames)
# i = 1
# for row in reader:
#     judgment_dict[row["UNIQUE_ID_PK"]] = row
#     judgment_dict[row["UNIQUE_ID_PK"]].pop("UNIQUE_ID__PK", None)
#
# helper.dump_json_to_file('resources/data/annotations/json/JUDGMENTS_HELPFUL.json', judgment_dict)
# csv_file.close()


