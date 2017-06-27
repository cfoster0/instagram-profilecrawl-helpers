import sys
import os
import json
from collections import Counter
import networkx as nx

def main():
	mentionedUsers = Counter()
	officialProfiles = set()
	userMentions = {}
	G=nx.DiGraph()

	for fName in os.listdir('profiles'):	
		if (not fName.endswith('.json')):
			continue
		with open('profiles/' + fName, 'r') as f:
			profile = json.loads(f.read())

		if not G.has_node(fName):
			G.add_node(fName)
		mentions = set()

		if profile["official"]:
			officialProfiles.add("@"+profile["alias"])

		for post in profile["posts"]:
			for mentionedUser in post["mentions"]:
				mentionedUser = mentionedUser.lower()
				if mentionedUser not in mentions:
					mentionedUsers[mentionedUser] += 1
					mentions.add(mentionedUser)
					if not G.has_node(mentionedUser):
						G.add_node(mentionedUser)
					G.add_edge(fName, mentionedUser)
		userMentions[fName] = mentions
	
	print("Most Mentioned (Overall):")
	for (key, value) in mentionedUsers.most_common(10):
		print('\t' + str(value) + '\t' + key)

	print("PageRank Ranking (Overall):")
	pr = nx.pagerank(G)
	for w in sorted(pr, key=pr.get, reverse=True)[0:10]:
		print('\t' + str(pr[w]) + '\t' + w)

	for user in list(mentionedUsers):
		if user in officialProfiles:
			del mentionedUsers[user]

	print("Most Mentioned (non-Official):")
	for (key, value) in mentionedUsers.most_common(10):
		print('\t' + str(value) + '\t' + key)

	print("PageRank Ranking (non-Official):")
	prcount = 0
	for w in sorted(pr, key=pr.get, reverse=True):
		if prcount >= 10:
			break
		if w not in officialProfiles:
			print('\t' + str(pr[w]) + '\t' + w)
			prcount = prcount + 1

if __name__ == '__main__':
	main()