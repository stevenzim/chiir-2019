# Scripts to create participant data folders and files from master.csv
# WARNING: Only run this to create new participant folders
# WARNING: Make a back up of folders before running

import csv

from src.crud import participant


# OPEN MASTER PARTICIPANT LIST
csv_file = open('resources/data/participant/test_master_participant_list.csv', 'r')
# csv_file = open('resources/data/participant/family_friend_participants.csv', 'r')
reader = csv.reader(csv_file)

fieldnames = next(reader)

temp_dict = {}
reader = csv.DictReader( csv_file, fieldnames)

for row in reader:
    temp_participant = participant.Participant(row['participant_id'],
                                               row['variant_id'],
                                               row['qualtrics_link'],
                                               int(row['random_seed']))
    try:
        temp_participant.create_new_participant()
    except OSError as err:
        print (err)
    print("Participant " + row['participant_id'] + " created.")

csv_file.close()