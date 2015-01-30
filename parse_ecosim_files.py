from amara.bindery import html
from amara.lib import U
import urllib
import urlparse
import shelve
import time

'''
This script extract data from html pages and write the data into a .json file ready
to create the mediawiki / wikieducator pages

'''


BASE = 'http://academics.smcvt.edu/dmccabe/teaching/Community/'


def parse_notes_file(f):
    '''
    Parse file like stream and returns title & content.

    Title is the first line of the file
    Content is delimited by 'beginnotes' and 'endnotes' words
    '''
    title = f.readline().strip()
    content = []
    for line in f:
        if line.startswith('beginnotes'):
            break
    for line in f:
        if line.startswith('endnotes'):
            break
        else:
            line = line.strip() or '\n\n'
            content.append(line)
    content = ' '.join(content)
    content = content.decode('utf-8', 'replace')
    return {'title': title, 'content': content}


def parse_anchor_ecosim(anchor):
    '''
    It returns text and href url from an html anchor for ecosim
    '''
    name = U(anchor).lower().strip()
    url = urlparse.urljoin(BASE, anchor.href)
    return name, url


def parse_anchor_notes(anchor):
    '''
    It returns the text and href url from an html anchor for ecosim notes. Removes the
    'Notes adn data from:' words from teh text.
    '''
    name = U(anchor).replace('Notes and data from:', '').lower().strip()
    url = urlparse.urljoin(BASE, anchor.href)
    return name, url


def parse_ecosim_file(url):
    '''
    Parse the url from an ecosim data file.

    It returns the data, species, files
    '''
    f = urllib.urlopen(url)
    lines = [l for l in f.readlines()]
    species = len(lines) -1
    sites = len(lines[0].split()) -1
    return ''.join(lines), species, sites


def parse_all_notes(notesdict):
    allnotes = {}
    for k in notesdict:
        print 'parsing notes', k
        allnotes[str(k)] = parse_notes_file(urllib.urlopen(notesdict.get(k)))
    #typo
    allnotes['1000islm.txt'] = allnotes.pop('notes and \n\t\t\t\t\t\tdata from:1000islm.txt')
    return allnotes

def change_titles(pages):
    '''
    Adds numbres to repeated titles
    '''
    titles = {}

    def numbertit(title, n):
        pos = title.find('(')
        return title[:pos]+str(n)+' '+title[pos:]

    for p in pages:
        title = p.get('title')
        n = titles.get(title, 0)
        if n == 0:
            titles[title] = 1
        else:
            titles[title] = n + 1
            title = numbertit(title, n)
            p['title'] = title


if __name__ == '__main__':

    import json

    # Main index file
    f = 'http://academics.smcvt.edu/dmccabe/teaching/Community/NullModelData.html'
    doc = html.parse(f)

    #ecosim data links
    ecosim_files = doc.xml_select(u'//a[contains(@href, "matrices_ecosim")]')

    # ecosim notes links
    notes_files = doc.xml_select(u'//a[contains(@href, "matrices_notes")]')

    # name -> url
    ecodict = dict([parse_anchor_ecosim(e) for e in ecosim_files])
    notesdict = dict([parse_anchor_notes(e) for e in notes_files])

    # names sorted
    ecokeys = ecodict.keys()

    allnotes = parse_all_notes(notesdict)

    # json.dump(allnotes, open('allnotes.json', 'w'))  # if you want to create a dump

    pages = []

    for x in ecokeys:
        print 'parsing data', x
        k = str(x)  # element to process Shelve keys must be Str
        eco_url = ecodict.get(k)
        data, species, sites = parse_ecosim_file(eco_url)
        d = allnotes.get(k)
        if not d:
            print 'Not found', k
            continue
        d['data'] = data
        #create_page(d, eco_url)
        d['species'] = species
        d['sites'] = sites
        d['source'] = eco_url
        d['name'] = k

        pages.append(d)

        time.sleep(0.2)  # no want DOS

    change_titles(pages)

    json.dump(pages, open('pages_to_create.json', 'w'))


    #pages created for debugging

