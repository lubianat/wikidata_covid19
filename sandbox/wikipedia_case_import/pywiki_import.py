import pywikibot
"""
Remove a qualifier from claims/statements
"""
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, "Q102044164")
item.get() #Fetch all page data, and cache it.

for claim in item.claims['P527']: #Finds all statements (P131)
    if 'P1120' in claim.qualifiers: #If has the qualifier we want to remove
        for qual in claim.qualifiers['P1120']: #iterate over all P100
            claim.removeQualifier(qual, summary=u'Remove qualifier.') #remove P100
    if 'P1603' in claim.qualifiers: #If has the qualifier we want to remove 
        for qual in claim.qualifiers['P1603']: #iterate over all P100
            claim.removeQualifier(qual, summary=u'Remove qualifier.') #remove P100
    if 'P1603' in claim.qualifiers: #If has the qualifier we want to remove
        for qual in claim.qualifiers['P3457']: #iterate over all P100
            claim.removeQualifier(qual, summary=u'Remove qualifier.') #remove P100
    if 'P585' in claim.qualifiers: #If has the qualifier we want to remove
        for qual in claim.qualifiers['P585']: #iterate over all P100
            claim.removeQualifier(qual, summary=u'Remove qualifier.') #remove P100