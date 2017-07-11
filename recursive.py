import sys
import os
import json
import argparse
from collections import Counter

def main():
	parser = argparse.ArgumentParser(description='Recursively crawl Instagram profiles.')
	parser.add_argument('--input_file',
                      dest='input_file',
                      type=str,
                      help='File with seed list of profiles.')
	parser.add_argument('--output_file',
                      dest='output_file',
                      type=str,
                      help='File to write outputs to.')
	parser.add_argument('--skip_download',
                      dest='skip_download',
                      action='store_true',
                      help='Flag to skip initial profile loading.')
	args = parser.parse_args()

	seed = args.input_file
	save = args.output_file
	with open(save, 'w+') as f:
		pass

	seedList = []
	users = set()

	fName = seed
	lines = [line.rstrip('\r\n') for line in open(fName)];
	for line in lines:
		seedList.append(line)
		users.add(line)
		if not args.skip_download:
			os.system('npm-run instagram-profilecrawl ' + line)
	addList = list(users)

	userMentions = {}
	mentionedUsers = Counter()
	userProfiles = {}

	unreadable = []



	while (True):
		for toRead in addList:
			profileFName = 'profile ' + toRead + '.json'
			if not os.path.isfile(profileFName):
				users.remove(toRead)
				unreadable.append(toRead)
				continue

			with open(profileFName, 'r') as f:
				profile = json.loads(f.read())

			if toRead not in seedList:
				#if profile["numberFollowers"] < 100000 or profile["official"] == True:
				if profile["numberFollowers"] < 100000:
					unreadable.append(toRead)
					addList.remove(toRead)
					continue
				else:
					with open(save, 'a+') as f:
						f.write(toRead + '\n')


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
		addList = [s for s in addList if s not in unreadable]
		if not addList:
			break
		for toAdd in addList:
			os.system('npm-run instagram-profilecrawl ' + toAdd)
			users.add(toAdd)
		#with open(save, 'a+') as f:
		#	for li in addList:
		#		#f.write('\n' + li)
		#		f.write(li + '\n')

def multiple_mention(counter):
	return [key for key in counter if counter[key] > 1]


if __name__ == '__main__':
	main()