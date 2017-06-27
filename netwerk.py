import sys
import os
import json
from collections import Counter

def main():
	mentionedUsers = Counter()

	for fName in os.listdir('profiles'):	
		if (not fName.endswith('.json')):
			continue
		with open('profiles/' + fName, 'r') as f:
			profile = json.loads(f.read())

		mentions = set()

		for post in profile["posts"]:
			for mentionedUser in post["mentions"]:
				#mentionedUsers[mentionedUser] += 1
				mentions.update(mentionedUsers)
				if mentionedUser not in mentions:
					mentionedUsers[mentionedUser] += 1
	
	print("Most Mentioned:")
	for (key, value) in mentionedUsers.most_common():
		print('\t' + str(value) + '\t' + key)

	addList = multiple_mention(mentionedUsers)
	print(addList)

def multiple_mention(counter):
	return [key for key in counter if counter[key] > 1]

if __name__ == '__main__':
	main()