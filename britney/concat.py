

filenames = ['mod0/file1.txt', 'file2.txt', 'mod3/']
with open('DailyMail_content', 'w') as outfile:
	for fname in filenames:
		with open(fname) in infile:
			for line in infile:
				outline.write(line)
				