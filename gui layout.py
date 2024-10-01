import random
from wonderwords import RandomWord
import json

r = RandomWord()

drawer = []
d = input("What do you want to do? \"rs\" or \"load\"? ")
if d == "rs":
    for i in range(5):
        finished_str = "\""
        finished_str = finished_str + r.word().capitalize()
        for i in range(random.randint(10, 20)):
            finished_str = finished_str + " "
            finished_str = finished_str + r.word()
        finished_str = finished_str + "\""
        
        print(finished_str)
else:
    print("Loading...")
    with open('GUI Layout.json', 'r') as file:
        drawer = json.load(file)
    print("Finished loading")
    d = input("What do you want to do now? \"add\", \"duplicate\" or \"remove\"? ")
    if d == "duplicate":
        d = input("Which one do you want to duplicate? ")
        d = int(d)
        drawer.append(drawer[d])
        d = input("Do you want to save changes? \"y\" or \"n\"? ")
        if d == "y":
            print("Dumping...")
            with open('GUI Layout.json', 'w') as json_file:
                json.dump(drawer, json_file, indent=4)
            print("Finished dumping")
            