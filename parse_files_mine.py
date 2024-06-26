from random import randint, random
from datetime import datetime, timedelta
import time


def load_comments(path):
    output_data = {}
    with open(path, encoding='utf-8') as file:
        lines = file.readlines()
        comment = ""
        found_open_ellipsis = False
        found_close_ellipsis = False

        for index in range(1, len(lines)):

            line = lines[index]

            if line == "\n":
                comment += line

            if line[-1] == "\n":
                line = line[:-1]

            first_index = line.index("\"") if "\"" in line else -1
            if first_index > -1:
                found_open_ellipsis = True

            next_index = line.index("\"", first_index + 1) if "\"" in line[first_index + 1:] else -1
            if next_index > -1:
                found_close_ellipsis = True

            if found_open_ellipsis and not found_close_ellipsis:
                comment += line
                continue
            else:
                comment = line

            data = comment.split(",")
            n = len(data)

            if n < 14:
                raise Exception("Comment does not contain necessary data.")
            elif n > 14:
                comment_text = "".join(data[3:n - 10])
            else:
                comment_text = data[3]

            date_format = "%Y-%m-%d %H:%M:%S"
            vrijeme_string = data[5]
            vrijeme = datetime.strptime(vrijeme_string, date_format)

            # content = [data[1]]
            if data[4] not in output_data.keys():
                output_data[data[4]] = {}
                output_data[data[4]][data[1]] = {}
            if data[1] not in output_data[data[4]].keys():
                output_data[data[4]][data[1]] = {}
            output_data[data[4]][data[1]] = vrijeme

            found_open_ellipsis = found_close_ellipsis = False
            comment = ""
    return output_data


def load_statuses(path):
    extracted_statuses = {}
    with open(path, encoding='utf-8') as file:
        lines = file.readlines()
        comment = ""
        paired_ellipses = True

        for index in range(1, len(lines)):

            line = lines[index]

            if line == "\n":
                comment += line
                continue

            # if line[-1] == "\n":
            #     line = line[:-1]
            line = line.strip()

            previous_index = -1

            while True:
                index = line.index("\"", previous_index+1) if "\"" in line[previous_index+1:] else -1
                if index == -1:
                    break
                paired_ellipses = not paired_ellipses
                previous_index = index

            comment += line
            if not paired_ellipses:
                continue

            data = comment.split(",")
            n = len(data)

            if n < 16:
                raise Exception("Status does not contain necessary data.")
            elif n > 16:
                comment_text = "".join(data[1:n-14])

                if path == "dataset/statuses.csv":
                    n += 1

            else:
                comment_text = data[1]

            # date_format = "%Y-%m-%d %H:%M:%S"
            # vrijeme_string = data[4]
            # vrijeme = datetime.strptime(vrijeme_string, date_format)

            date_format_1 = "%Y-%m-%d %H:%M:%S"
            date_format_2 = "%Y/%m/%d %H:%M:%S"
            if path == "dataset/statuses.csv":
                n -= 1

            vrijeme_string = data[n-12]
            vrijeme = None

            try:
                vrijeme = datetime.strptime(vrijeme_string, date_format_1)
            except ValueError:
                try:
                    vrijeme = datetime.strptime(vrijeme_string, date_format_2)
                except ValueError:
                    print(data[n-12])
                    vrijeme = datetime.now()

            extracted_statuses[data[0]] = ([data[0], comment_text, data[n-14], data[n-13], vrijeme, data[n-11],
                             data[n-10], data[n-9], data[n-8], data[n-7], data[n-6], data[n-5], data[n-4],
                             data[n-3], data[n-2], data[n-1]])

            comment = ""
            paired_ellipses = True

    return extracted_statuses


def load_shares(path):
    shares = {}
    with open(path, encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines[1:]:

            podaci = line.strip().split(",")

            # date_format = "%Y-%m-%d %H:%M:%S"
            # vrijeme_string = podaci[2]
            # vrijeme = datetime.strptime(vrijeme_string, date_format)

            date_format_1 = "%Y-%m-%d %H:%M:%S"
            date_format_2 = "%Y/%m/%d %H:%M:%S"

            vrijeme_string = podaci[2]
            vrijeme = None

            try:
                vrijeme = datetime.strptime(vrijeme_string, date_format_1)
            except ValueError:
                try:
                    vrijeme = datetime.strptime(vrijeme_string, date_format_2)
                except ValueError:
                    print("Invalid date format")

            if podaci[1] not in shares.keys():
                shares[podaci[1]] = {}
                shares[podaci[1]][podaci[0]] = {}
            if podaci[0] not in shares[podaci[1]].keys():
                shares[podaci[1]][podaci[0]] = {}
            shares[podaci[1]][podaci[0]] = vrijeme
    return shares


def load_reactions(path):
    reactions = {}
    with open(path, encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines[1:]:

            podaci = line.strip().split(",")

            # date_format = "%Y-%m-%d %H:%M:%S"
            # vrijeme_string = podaci[3]
            # vrijeme = datetime.strptime(vrijeme_string, date_format)

            date_format_1 = "%Y-%m-%d %H:%M:%S"
            date_format_2 = "%Y/%m/%d %H:%M:%S"

            vrijeme_string = podaci[3]
            vrijeme = None

            try:
                vrijeme = datetime.strptime(vrijeme_string, date_format_1)
            except ValueError:
                try:
                    vrijeme = datetime.strptime(vrijeme_string, date_format_2)
                except ValueError:
                    print("Invalid date format")

            if podaci[2] not in reactions.keys():
                reactions[podaci[2]] = {}
                reactions[podaci[2]][podaci[0]] = []
            if podaci[0] not in reactions[podaci[2]].keys():
                reactions[podaci[2]][podaci[0]] = []
            reactions[podaci[2]][podaci[0]].append(podaci[1])
            reactions[podaci[2]][podaci[0]].append(vrijeme)
    return reactions


def load_friends(path):
    friends = {}
    with open(path, encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines[1:]:
            friends[line.strip().split(",")[0]] = (line.strip().split(",")[2:])
    return friends
