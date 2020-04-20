import requests
from datetime import datetime

'''
Just a quick-and-dirty function to generate QS from some papers. 
Not a lot of thought went into this, so it can certainly be improved. 
I only sketched it up in 5 min to add some of the papers from BIOGrid to Wikidata.
'''
def qs_from_doi(doi,full_link):
  response = requests.get(f'http://api.crossref.org/works/{doi}')
  info = response.json()['message']
  title = info['title'][0]
  published_in = info['institution']['name']
  date_list = info['posted']['date-parts']
  date_str = '/'.join(map(str, date_list[0]))
  date = datetime.strptime(date_str, "%Y/%m/%d").strftime("+%Y-%m-%dT00:00:00Z/11")
  doi = info['URL'][18:]
  print("CREATE\n" + 
      'LAST|Len|' + '"' + title + '"\n' +
      'LAST|Den|' + '"'+ f"journal article from '{published_in}' published in 2020" + '"\n' +
      'LAST|P31|' + "Q13442814" + '\n' +
      'LAST|P356|' + '"' + doi + '"\n' +
      "LAST|P577|" + '"' + date + '"\n' +
      "LAST|P1476|" + '"' + title + '"\n' +
      "LAST|P407|" + 'Q1860' + "\n"
      "LAST|P953|" + '"' + full_link + '"'
     )

if __name__ == "__main__":
  qs_from_doi(
    doi = input("DOI for the publication:"),
    full_link = input("Link to full work(P953):")
  )
