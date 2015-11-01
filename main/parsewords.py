import json
f = open("words.txt", "r")

words = []
for line in f:  # append from file
    words.append(str(line))

for word in words:  # filter out words with 3 characters or less
    if len(word) <= 4:
        words.remove(word)

for idx, word in enumerate(words):
    print word
    if len(word) <= 4:
        words.remove(word)
        print "removed"
    words[idx] = word.rstrip()  # filter out \n
for item in words:
    print item
print len(words)
new_file = open("clean_words.json", "w")
new_file.write(json.dumps(words))
print json.dumps(words)
