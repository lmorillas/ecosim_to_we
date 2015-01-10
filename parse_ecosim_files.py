from amara.bindery import html
from amara.lib import U
import urllib
import urlparse
import shelve
from create_we_pages import *


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
    f = 'http://academics.smcvt.edu/dmccabe/teaching/Community/NullModelData.html'
    doc = html.parse(f)
    ecosim_files = doc.xml_select(u'//a[contains(@href, "matrices_ecosim")]')
    notes_files = doc.xml_select(u'//a[contains(@href, "matrices_notes")]')
    ecodict = dict([parse_anchor_ecosim(e) for e in ecosim_files])
    notesdict = dict([parse_anchor_notes(e) for e in notes_files])
    ecokeys = ecodict.keys()
    ecokeys.sort()
    #create_shelve(notesdict)  # is the shelve created?
    fnotes = shelve.open('notes.dat')
    pages = []

    for x in range(10):
        k = str(ecokeys[x])  # element to process
        data, species, sites = parse_ecosim_file(ecodict.get(k))
        d = fnotes.get(k)
        if not d:
            print 'no encontrado', k
            break
        d['data'] = data
        create_page(d)
        pages.append([d.get('title'), species, sites])

    create_index(pages)
