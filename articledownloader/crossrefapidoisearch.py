from crossref.restful import Works,Journals

works=Works()
journals=Journals()
response=journals.works(issn).query(query).filter(from_online_pub_date=pub_after).sample(rows).select('DOI','deposited')

for item in response:
	print(item)