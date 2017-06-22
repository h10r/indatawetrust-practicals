for line in open("full_search_after_petition.txt").readlines():
	for elem in line.split(" "):
		if elem.startswith("@"):
			print elem