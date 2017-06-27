import os, sys

def main(arguments):
	if (len(arguments) > 1):
		for arg in arguments:
			os.system('npm-run instagram-profilecrawl ' + arg)
	else:
		fname = arguments[0]
		lines = [line.rstrip('\n') for line in open(fname)];
		for line in lines:
			os.system('npm-run instagram-profilecrawl ' + line)

if __name__ == '__main__':
	main(sys.argv[1:])
