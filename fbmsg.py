import os
import os.path
import sys
import json
from datetime import datetime

class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.grpfile = open(filename, "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.grpfile.write(message)  

    def flush(self):
        #flush method
        pass


def start_file(filename):
    sys.stdout = Logger(filename)


def stop_file():
    sys.stdout.grpfile.close()
    sys.stdout = sys.stdout.terminal


def del_line():
    sys.stdout.write("\033[K")


def m_files(location):
    if location == "":
            location = "."
    files = []
    try:
        for f in os.listdir(location):
            if f.endswith(".json"):
                files.append(os.path.join(location, f))
    except FileNotFoundError:
        print("\nNo such location")
    return files


def fixup_str(text):
    return text.encode('latin1').decode('utf8')


def fixup_list(l):
    return [fixup(e) for e in l]


def fixup_dict(dct):
    return {fixup_str(k): fixup(v) for k, v in dct.items()}


def fixup(e):
    if isinstance(e, dict):
        return fixup_dict(e)
    if isinstance(e, list):
        return fixup_list(e)
    if isinstance(e, str):
        return fixup_str(e)
    return e


def filter_messages(messages):
    for message in messages:
        if message['type'] == 'Generic':
            yield message


def format_message(message):
    sender = message['sender_name']
    timestamp = datetime.fromtimestamp(message['timestamp_ms']/1000)
    content = message.get('content', "")
    return timestamp, sender, content


def parse(files):
    out = []

    with open(files[0], 'r') as f:
        parts = fixup(json.loads(f.read()))['participants']
    for fname in files:
        with open(fname, 'r') as f:
            messages = fixup(json.loads(f.read()))['messages']

        for message in filter_messages(messages):
            #print(format_message(message))
            time, sender, msg = format_message(message)
            if msg == "":
                continue
            d = {'time': str(time), 'sender': sender, 'message': msg}
            out.append(d.copy())
    out_msg = {'participants': parts, 'messages': out}
    return out_msg


def count(msg):
    total_count = 0
    details = {}
    words = {}
    for p in msg['messages']:
        details[p['sender']] = {'count': 0}
    for m in msg['messages']:
        total_count += len(m['message'].split())
        for d in details:
            if m['sender'] == d:
                details[d]['count'] += len(m['message'].split())
        word = m['message'].strip().split()
        for w in word:
            wl = w.lower()
            if wl not in words:
                words[wl] = {'count': 1}
                for p in details:
                    words[wl][p] = 0
                words[wl][m['sender']] = 1
            else:
                words[wl]['count'] += 1
                words[wl][m['sender']] += 1

    return total_count, details, words


def p_words(g_name, total_count, details, words, from_date, to_date):
    filename = g_name.replace(" ", "_") + "_analysis.txt"
    start = False
    if not os.path.isfile(filename):
        start = True 
        start_file(filename)
    print("Words Analysis for '" + g_name + "'")
    print("\nMessages from", from_date ,"to", to_date, "\n")
    print("Total no. of unique words in the group:", len(words), "\n")
    print("Total no. of words in the group:", total_count, "\n")    
    for i in details:
        print(i, ":", details[i]['count'])
    print()
    print("Overall top 50 words:")
    print(*(i for i in stop(words)), sep=', ', end='')
    parts = parts_count(details, words)
    parts_sorted = words_parts(parts)
    for i in parts_sorted:
        if len(parts_sorted[i]) > 50: 
            number = 50 
        else: 
            number = len(parts_sorted[i])
        print("\n")
        print(i + ":")
        print(*(parts_sorted[i][j][0] for j in range(number)), sep=', ', end='')
    print("\n")
    if start: stop_file()
    print_word_count(words, filename)  
    return 


def stop(words):
    sorted_words = sorted(words.items(), key=lambda word: word[1]['count'], reverse = True)
    i = 0
    for s in sorted_words:
        i += 1
        if i > 50:
            break
        yield s[0]


def parts_count(details, words):
    parts = {k: {} for k in details}
    for k, v in words.items():
        for i in v:
            if i == 'count':
                continue
            else:
                if v[i] != 0:
                    parts[i][k] = v[i]
    return parts


def words_parts(parts):
    parts_sorted = {}
    for i in parts:
        parts_sorted[i] = sorted(parts[i].items(), key=lambda part: part[1], reverse=True)
    return parts_sorted


def print_word_count(words, filename):
    input_word = True
    while input_word:
        input_word = input("\n\nEnter the word to see the count:")
        if input_word == "":
            break
        try:
            words_input = words[input_word]
        except KeyError:
            print("\nNo such word in the message.")
        else:
            start_file(filename)
            print("\n\nWord: ", input_word, "\n")
            for i in words_input: 
                print(i, ":", words_input[i])
            stop_file()             
    return
            


def main():
    g_name = input("Enter the group name:")
    files = []
    while files == []:
        location = input("\nEnter the location of the message files \n(Just press 'Enter' if in the same folder):")
        files = m_files(location)
        if files == []:
            print("No json message files in the location \n")
        else:
            print("\nThe message files are:")
            for m in files:
                print(m.strip(location + "/"))
            break
    print()
    msg = parse(files)
    from_date = msg['messages'][-1]['time'][:-7]
    to_date = msg['messages'][0]['time'][:-7]
    total_count, details, words = count(msg)
    p_words(g_name, total_count, details, words, from_date, to_date)
    input("Enter to exit:")
    
    

if __name__ == "__main__":
    main()
    