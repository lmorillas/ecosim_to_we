import mwclient

USER = ''
PWD = ''

# where it is going to create the tree
WEBASE = "NullModelData"

# we connection
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
"""

    initial_page_end = """
    |}

    [[Category:NullModeData]]
    """

    table = [new_element(*d) for d in data]


    initial_page = site.Pages[WEBASE]
    initial_page.save(text_index + ''.join(table) + initial_page_end, summary='Creating null mode data with mwclient')


def new_element(title, site, species):
    return '''|-
    ! {}
    | {}
    | {}
    '''.format('[[{}/{}|{}]]'.format(WEBASE, title, title), site, species)



TEMPLATE = open('template_note.txt').read()
def new_page_content(d):
    '''
    d --> dictionary: title, content, data
    '''
    newp = TEMPLATE.format(**d)
#    newp = newp.replace('}', '}}')
#    newp = newp.replace('{', '{{')
    newp = newp.replace('\n ', '\n')
    return newp

def create_page(d, src=None):
    '''

    '''
    title = d.get('title').strip()
    title = WEBASE + '/' + title
    d['urlsrc'] = src
    d['namesrc'] = src.split('/')[-1].strip().lower()

    newpage = site.Pages[title]
    newpage.save(new_page_content(d), summary='Creating null mode data page for' + title)
