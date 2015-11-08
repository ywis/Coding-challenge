# example of program that calculates the number of tweets cleaned
import re

# Read the tweets
txt = open('/Users/siqi/DataEngineering/coding-challenge/data-gen/tweets.txt')
content = txt.read()  # return a string object
line = content.split(',"')
# print len(line)
txt.close()

# Write to a file
f = open('/Users/siqi/DataEngineering/coding-challenge/tweet_output/ft1.txt', 'w')
N = len(line)  # number of tweets in tweets.txt
output = [0] * N  # number to be decided later
timestamp = [0] * N
ts = [0] * N
j = 0
k = 0
for i in range(len(line)):
    if len(re.findall(r'^text"', line[i])) == 1:
        output[j] = line[i]
        j += 1
    elif len(re.findall(r'{"created_at"', line[i])) == 1:
        timestamp[k] = line[i]
        k += 1
    else:
        pass

def remove_escape_char(s):
    return s.replace("\ ", '').replace('\b', '').replace('\f', '').replace('\\n', '').replace('\r', '').replace('\t', '').replace('\v', '').replace('\?', '').replace('&gt', '').replace('&lt', '')


def clean_text(s):
    # input the slices of data and return the cleaned format of data
    if len(s.split('":"')) >= 2:
        return remove_escape_char(s.split('":"')[1][0:-1]). \
            decode('unicode_escape').encode('ascii', 'ignore').replace('\\', '')


def clean_timestamp(s):
    # input the slices of timestamp and return the cleaned format of data
    return s.split('at":"')[1][0:-1]

for i in range(j):
    f.write(clean_text(output[i]) + ' (timestamp: ' +
            str(clean_timestamp(timestamp[i])) + ')\n')

n = 0  # count the number of contents which have the unicode
for i in range(j):
    #    if clean_text(output[i]) == \
    #            remove_escape_char(output[i]).split('":"')[1][0:-1].replace('\\', ''):
    if clean_text(output[i]) != remove_escape_char(output[i]. \
                                                           split('":"')[1][
                                                   0:-1]).replace('\\', ''):
        n += 1

f.write('\n' + str(n) + " tweets contained unicode.")
f.close()


# Two distinct hashtags
# time difference
# remove the http at the end of hashtags
