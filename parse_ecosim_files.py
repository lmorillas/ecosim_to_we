from amara.bindery import html
from amara.lib import U
import urllib
import urlparse
import shelve


fnotes = shelve.open('notes.dat')

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



def parse_ecosim_file(f):
    f = urllib.urlopen(url)
    lines = [l for l in f.readlines()]
    species = len(lines) -1
    sites = len(lines[0].split()) -1



if __name__ == '__main__':
    f = 'http://academics.smcvt.edu/dmccabe/teaching/Community/NullModelData.html'
    doc = html.parse(f)
    ecosim_files = doc.xml_select(u'//a[contains(@href, "matrices_ecosim")]')
    notes_files = doc.xml_select(u'//a[contains(@href, "matrices_notes")]')
    ecodict = dict([parse_anchor_ecosim(e) for e in ecosim_files])
    notesdict = dict([parse_anchor_notes(e) for e in notes_files])
    for k in notesdict:
        print k
        fnotes[str(k)] = parse_notes_file(urllib.urlopen(notesdict.get(k)))

    fnotes.sync()
    fnotes.close()
