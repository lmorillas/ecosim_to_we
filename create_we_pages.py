import mwclient
from mwclient.errors import APIError


#comfigure bot

USER = ''
PWD = ''

# where it is going to create the tree
WEBASE = "NullModelData"

TEMPLATE = open('template_note.txt').read()

# configure mediawiki connection
site = mwclient.Site('wikieducator.org', path="/")
site.login(USER, PWD)


# create index with a table
def create_index(data):
    text_index = """{{MyTitle| Null Model Data}}

==Files for null model analysis==

{{note|intended for educational use}}

These matrices were compiled under NSF grant BSR 9106981 awarded to Bruce Patterson in 1991.  The grant supported a collaboration of Wirt Atmar, Alan Cutler, Gregory Mikkelson, Bruce Patterson, and David Wright.  The original matrices, some additional matrices, and notes concerning their derivation can be downloaded in full from AICS Research INC.  Data sets are unzipped with the software.

'''Recommended citation format''': ''Atmar, J.W., and B.D. Patterson. 1995. The nestedness temperature calculator: a visual basic program, including 294 presence-absence matrices. AICS Research, Inc., University Park, NM, and The Field Museum, Chicago.''

'''Disclaimer''':  In the files linked on the left below, I have removed the notes and citations, and transposed the data. While I have not intentionally modified the data in any other way, neither have I gone back to the original publications to confirm accuracy.

'''Easy save option''': Right click on any link below.  Select 'save target as', and save it to a location of your choice.  The resulting file can be opened from Ecosim.

{| border="1" class="wikitable"
|+ Files for null model analysis
! Title
! Sites
! Species
! Data source
"""
    initial_page_end = """
    |}

    [[Category:NullModeData]]
    """
    datos = []
    for d in data:
        x = {}
        x['title'] = d['title']
        x['site'] = d['sites']
        x['species'] = d['species']
        x['link'] = d['source']
        datos.append(x)

    table = [new_element(**d) for d in datos]

    initial_page = site.Pages[WEBASE]
    content = text_index + ''.join(table) + initial_page_end
    initial_page.save(content, summary='Creating null mode data with mwclient')


def new_element(title, site, species, link):
    name = link.split('/')[-1].lower()
    return '''|-
    | {}
    | {}
    | {}
    | {}
    '''.format('[[{}/{}|{}]]'.format(WEBASE, title, title), site, species,
            '[{}  {}]'.format(link, name))


def new_page_content(d):
    '''
    d --> dictionary: title, content, data, source, name
    '''
    newp = TEMPLATE.format(**d)
    newp = newp.replace('\n ', '\n')
    return newp


def create_page_from_template(data):
    d = {}
    title = data.get('title').strip()
    d['title'] = title
    title = WEBASE + '/' + title
    d['title'] = title
    d['content'] = data['content'].encode('utf-8')
    d['data'] = data['data'].encode('utf-8')
    src = data.get('source')
    d['source'] = src  # can't write links now :-(
    d['name'] = src.split('/')[-1].strip().lower()

    print 'creating', title
    content = new_page_content(d)
    return {'title':title, 'content':content}

def create_we_pages(d):
    '''
    This need a bot account because pages have external links

    d --> dict: title / content keys
    '''
    title = d.get('title')
    d.get('content')

    try:
        newpage = site.Pages[title]
        newpage.save(d.get('content'), summary='Creating null mode data page for' + title)
    except APIError, e:
        print e
        errors.append(title)
    except:
        print 'Error with', title
        errors.append(title)


if __name__ == '__main__':

    import json
    import time

    errors = []

    # requires page_to_create.json
    pages = json.load(open('pages_to_create.json'))

    we_pages = []

    for p in pages:
        we_pages.append(create_page_from_template(p))

    map(create_we_pages, we_pages)

    # review errors list

    pages.sort(key=lambda x: x['title'])

    content = create_index(pages)
