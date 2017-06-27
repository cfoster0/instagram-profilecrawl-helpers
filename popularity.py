import sys
import os
import json
from collections import Counter

def main():
	postCount = Counter()
	likeCount = Counter()
	commentCount = Counter()
	
	for fName in os.listdir('profiles'):	
		if (not fName.endswith('.json')):
			continue
		with open('profiles/' + fName, 'r') as f:
			profile = json.loads(f.read())

		profilename = fName[8:-5]

		for post in profile["posts"]:
			postCount[profilename] += 1
			likeCount[profilename] += post["numberLikes"]
			commentCount[profilename] += post["numberComments"]
	
	likeRatio = {}
	commentRatio = {}

	for key in postCount:
		likeRatio[key] = likeCount[key] / postCount[key]
		commentRatio[key] = commentCount[key] / postCount[key]

	sortedLikes = sorted(likeRatio, key=likeRatio.get, reverse=True)
	sortedComments = sorted(commentRatio, key=commentRatio.get, reverse=True)

	print("Top Liked:")
	for key in sortedLikes:
		print("\t" + key)
	print("Top Commented:")
	for key in sortedComments:
		print("\t" + key)

if __name__ == '__main__':
	main()