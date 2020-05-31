import os
import json
from datetime import datetime

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



def main():
    files = []
    while files == []:
        location = input("Enter the location of the message files \n(Just press 'Enter' if in the same folder):")
        files = m_files(location)
        if files == []:
            print("No json message files in the location \n")
        else:
            print("\nThe message files are:")
            for m in files:
                print(m.strip(location + "/"))
            break
    
    msg = parse(files)
    total_count, details, words = count(msg)
    print(msg['participants'])
    print(total_count)
    print(details)
    input()
    

if __name__ == "__main__":
    main()
    