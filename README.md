# Ecosim to WE

## Create pages in WE ready to parse with Ecosim

Data from http://academics.smcvt.edu/dmccabe/teaching/Community/NullModelData.html

For testing: 
```bash
$ python parse_ecosim_files.py
```

## The objective

To extract notes and data from the web source and to create new pages in Wikieducator (mediawiki) offering a free and more easy access to the data.

## Steps
* Create new templates for [Notes](http://wikieducator.org/Template:NMNotes) and [Data](http://wikieducator.org/Template:NMData)
* Extract and parse notes (Title and notes)
* Extract and parse data (content, species, sites)
* Create pages at Wikieducator from the http://wikieducator.org/NullModelData path
  * Be care with titles because they are repated
* Create the new index with a wiki sortable table

## Requirements
* Amara
* mwclient

## Execute
```
$ python parse_ecosim_files.py
$ python create_we_pages.py
```
