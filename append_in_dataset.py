import json
import csv
import os
import sys

subject_name = input("Enter username whose data is to be appended! :")
subject_files = []
for filename in os.listdir("./output/"):
    if filename.startswith(subject_name):
        subject_files.append(filename)
try:
    print("found:")
    for name in subject_files:
        print(name)
except:
    print("File not found")
    sys.exit()

# print(rows)
csv_dd_rows = []
csv_ud_rows = []
csv_ht_rows = []
all_keys = []
# csv_row = []
with open('DSL-StrongPasswordData.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        for item in row:
            all_keys.append(item)
            if item.startswith("H."):
                csv_ht_rows.append(item)
            elif item.startswith("DD."):
                csv_dd_rows.append(item)
            elif item.startswith("UD."):
                csv_ud_rows.append(item)

        break
csv_file.close()

# print(csv_ud_rows)
# print(csv_dd_rows)
# print(csv_ht_rows)

rows = []

hold_time_user = []
dd_key1_key2_user = []
ud_key1_key2_user = []



for i in range(0, len(subject_files)):
    cnt = 1
    fpath = "output/" + subject_files[i]
    try:
        with open(fpath) as readfile:
            print("Update .csv with: ", subject_files[i])
            hold_time_user_dict = dd_key1_key2_dict = ud_key1_key2_dict = {}
            data = json.load(readfile)
            for timing in data['timings']:
                hold_time_user.append(timing["hold_time"])
                dd_key1_key2_user.append(timing["dd_key1_key2"])
                ud_key1_key2_user.append(timing["ud_key1_key2"])
                row = dict()
                for key in timing["hold_time"].keys():
                    if key == "5":
                        new_key = "H.five"
                    elif key == "R":
                        new_key = "H.Shift.r"
                    else:
                        new_key = "H."+key
                    row[new_key] = timing["hold_time"][key]
                for key in timing["dd_key1_key2"].keys():
                    if key == "DD.5.R":
                        new_key = "DD.five.Shift.r"
                    elif key == "DD.R.o":
                        new_key = "DD.Shift.r.o"
                    elif key == "DD.e.5":
                        new_key = "DD.e.five"
                    else:
                        new_key = key
                    row[new_key] = timing["dd_key1_key2"][key]
                for key in timing["ud_key1_key2"].keys():
                    if key == "UD.5.R":
                        new_key = "UD.five.Shift.r"
                    elif key == "UD.R.o":
                        new_key = "UD.Shift.r.o"
                    elif key == "UD.e.5":
                        new_key = "UD.e.five"
                    else:
                        new_key = key
                    row[new_key] = timing["ud_key1_key2"][key]
                    # print(key)
                row["subject"] = subject_name
                row["rep"] = cnt
                row["sessionIndex"] = i+1
                rows.append(row)
                cnt += 1
                
    except FileNotFoundError as fnfe:
        print("Nothing happened")
        continue


# csv_file = "DSL-StrongPasswordData_mod.csv"
# try:
#     with open(csv_file, 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=all_keys)
#         writer.writeheader()
#         for data in rows:
#             writer.writerow(data)
# except IOError:
#     print("I/O error")


edit_csv_file = "edited_dataset/DSL-StrongPasswordData.csv"
try:
    with open(edit_csv_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_keys)
        # writer.writeheader()
        for data in rows:
            writer.writerow(data)
except IOError:
    print("I/O error")

csvfile.close()
