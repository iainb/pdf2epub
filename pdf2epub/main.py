from lxml import etree

from filter import pageFilters
from filter import tokenFilters
from extractor import lineExtractors
from grouping import lineGrouping
from grouping import paragraphGrouping
from grouping import pageGrouping

import common

from printers import stdout

def main(f):
    c = {   'input_path': f,
            'start_page': 23, 
            'end_page'  : 274,
            'header_size': 42,
            'footer_size': 60,
            'y_height_diff': 5,
            'line_height_diff': 0.1,
            'para_indent_diff': 1,
            'vertical_diff': 1
    }

    processBook(c)

def processBook(c):
    f = open(c['input_path'], 'r')
    tree = etree.parse(f)
    book = tree.getroot()
    output = common.copyElementAttributes(book)

    # process book
    book = pageFilters.removePages.apply(book,c)

    # initial page processing
    for page in book.iter('PAGE'):
        p = processPage(page, c)
        output.append(p)

    # merge paragraphs that span pages
    output = pageGrouping.mergeMultiPageParagraphs.apply(output, c)

    # merge hypenated words between lines
    for page in output.iter('PAGE'):
        for para in page.iter('PARAGRAPH'):
            lineGrouping.mergeTrailingHyphens.apply(para,c )            

    stdout.printBook(output)

def processPage(page, c):
    # remove header and footer from page
    page = tokenFilters.trimHeaderAndFooter.apply(page, c)

    # split the page up based on horizontal lines
    page = lineExtractors.simpleLineExtractor.apply(page, c)

    # group paragraphs based on line height (text size)
    page = paragraphGrouping.lineHeightGrouping.apply(page, c)

    # merge large paragraph initial letters into main text
    page = paragraphGrouping.chapterStartLetter.apply(page, c)
    
    # split up paragraphs based on the vertical gap between lines
    page = paragraphGrouping.splitOnVerticalGap.apply(page, c)

    # split up paragraphs based on indenting
    page = paragraphGrouping.splitOnIndent.apply(page, c)

    # finally update paragraph summary
    page = paragraphGrouping.createSummary.apply(page, c)

    return page
