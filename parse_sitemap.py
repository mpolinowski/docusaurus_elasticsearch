from lxml import etree
import requests

sideLinks = {}

r = requests.get("https://mpolinowski.github.io/sitemap.xml")
root = etree.fromstring(r.content)

print("INFO :: {0} pages imported from sitemap.".format(len(root)))

for sitemap in root:
    children = sitemap.getchildren()
    sideLinks[children[0].text] = children[1].text

# write to file

with open('pages/sideLinks.txt', 'w') as file:
    file.writelines('\n'.join(sideLinks))
    
 
