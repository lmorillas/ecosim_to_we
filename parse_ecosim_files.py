from amara.bindery import html
from amara.lib import U
import urllib
import urlparse
import shelve
from create_we_pages import *
import time


BASE = 'http://academics.smcvt.edu/dmccabe/teaching/Community/'


def parse_notes_file(f):
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
    return {'title': title, 'content': ' '.join(content)}


def parse_anchor_ecosim(anchor):
    name = U(anchor).lower().strip()
    url = urlparse.urljoin(BASE, anchor.href)
    return name, url

def parse_anchor_notes(anchor):
    name = U(anchor).replace('Notes and data from:', '').lower().strip()
    url = urlparse.urljoin(BASE, anchor.href)
    return name, url


def parse_ecosim_file(url):
    '''returns data, species, files'''
    f = urllib.urlopen(url)
    lines = [l for l in f.readlines()]
    species = len(lines) -1
    sites = len(lines[0].split()) -1
    return ''.join(lines), species, sites


def create_shelve(notesdict):
    '''
    Create a notes.dat shelve file. For testing
    key:
    value: dict: title / content of the notes file
    '''
    fnotes = shelve.open('notes.dat')
    for k in notesdict:
        print k
        fnotes[str(k)] = parse_notes_file(urllib.urlopen(notesdict.get(k)))

    #typo
    fnotes['1000islm.txt'] = fnotes.pop('notes and \n\t\t\t\t\t\tdata from:1000islm.txt')
    fnotes.sync()
    fnotes.close()


if __name__ == '__main__':

    # Main index file
    f = 'http://academics.smcvt.edu/dmccabe/teaching/Community/NullModelData.html'
    doc = html.parse(f)

    #ecosim matrices links
    ecosim_files = doc.xml_select(u'//a[contains(@href, "matrices_ecosim")]')
    # ecosim notes links
    notes_files = doc.xml_select(u'//a[contains(@href, "matrices_notes")]')

    ecodict = dict([parse_anchor_ecosim(e) for e in ecosim_files])
    notesdict = dict([parse_anchor_notes(e) for e in notes_files])

    # names
    ecokeys = ecodict.keys()
    ecokeys.sort()

    #create_shelve(notesdict)  #  Create a shelve as cache for testing the first time.
    # Is the shelve created?
    fnotes = shelve.open('notes.dat')
    pages = []

    for x in ecokeys:
        k = str(x)  # element to process Shelve keys must be Str
        eco_url = ecodict.get(k)
        data, species, sites = parse_ecosim_file(eco_url)
        d = fnotes.get(k)
        if not d:
            print 'Not found', k
            continue
        d['data'] = data
        create_page(d, eco_url)
        pages.append([d.get('title'), species, sites])

        time.sleep(0.2)

    create_index(pages)

    #pages created for debugging
    import json
    json.dump(pages, open('pages_created.json', 'w'))
