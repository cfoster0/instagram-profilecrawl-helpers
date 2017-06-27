import sys
import os
import json
from collections import Counter

def main(seed):
	users = set()

	fName = seed
	lines = [line.rstrip('\n') for line in open(fName)];
	for line in lines:
		users.add(line)
		os.system('npm-run instagram-profilecrawl ' + line)
	addList = list(users)

	userMentions = {}
	mentionedUsers = Counter()
	userProfiles = {}

	while (True):
		for toRead in addList:
			with open('profile ' + toRead + '.json', 'r') as f:
				profile = json.loads(f.read())
			userProfiles[toRead] = profile
			mentions = set()

			for post in profile["posts"]:
				for mentionedUser in post["mentions"]:
					mentionedUser = mentionedUser.encode('ascii', 'ignore')[1:]
					if mentionedUser not in mentions:
						mentionedUsers[mentionedUser] += 1
						mentions.add(mentionedUser)
			userMentions[toRead] = mentions
		mm = multiple_mention(mentionedUsers)
		addList = [s for s in list(set(mm) - users)]
		if not addList:
			break
		for toAdd in addList:
			users.add(toAdd)
			os.system('npm-run instagram-profilecrawl ' + toAdd)
		with open(seed, 'a+') as f:
			for li in addList:
				f.write('\n' + li)

def multiple_mention(counter):
	return [key for key in counter if counter[key] > 1]


if __name__ == '__main__':
	main(sys.argv[1])