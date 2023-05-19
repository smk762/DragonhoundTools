#!/bin/python3

from wordlist import english_wordlist as english

def calc_avg(word):
    sum_ = sum([ord(i)-96 for i in word])
    return sum_/len(word)


val_words = {}
for word in english:
    _avg = calc_avg(word)
    if str(_avg) not in val_words:
        val_words.update({str(_avg): []})
    val_words[str(_avg)].append(word)



dict_keys = list(val_words.keys())
dict_keys.sort()
sorted_dict = {i: val_words[i] for i in dict_keys}
print(sorted_dict)

eng_avg = [calc_avg(i) for i in english]
eng_avg.sort()
print(len(set(eng_avg)))

vals = {}
for i in eng_avg:
    if i not in vals:
        vals.update({i:0})
    vals[i] += 1
print(set(vals))