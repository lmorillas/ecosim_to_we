from amara.bindery import html
from amara.lib import U
import urllib
import urlparse


BASE = 'http://academics.smcvt.edu/dmccabe/teaching/Community/'


doc = html.parse('http://academics.smcvt.edu/dmccabe/teaching/Community/NullModelData.html')
ecosim_files = doc.xml_select(u'//a[contains(@href, "matrices_ecosim")]')

example = ecosim_files[100]

url = urlparse.urljoin(BASE, example.href)



f = urllib.urlopen(url)

lines = [l for l in f.readlines()]



species = len(lines) -1
sites = len(lines[0].split()) -1

print U(example), sites, species
