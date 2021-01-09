import pywikibot
"""
Remove a qualifier from claims/statements
"""
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, "Q102044164")
item.get() #Fetch all page data, and cache it.

for claim in item.claims['P527']: 
    if 'P1120' in claim.qualifiers:
        for qual in claim.qualifiers['P1120']: 
            claim.removeQualifier(qual, summary=u'Remove qualifier.') 
    if 'P1603' in claim.qualifiers: 
        for qual in claim.qualifiers['P1603']: 
            claim.removeQualifier(qual, summary=u'Remove qualifier.') 
    if 'P1603' in claim.qualifiers: 
        for qual in claim.qualifiers['P3457']: 
            claim.removeQualifier(qual, summary=u'Remove qualifier.') 
    if 'P585' in claim.qualifiers: 
        for qual in claim.qualifiers['P585']: 
            claim.removeQualifier(qual, summary=u'Remove qualifier.')