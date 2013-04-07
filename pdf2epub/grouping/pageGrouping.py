from lxml import etree
import pdf2epub.common as common

class _mergeMultiPageParagraphs():
    def __init__(self):
        pass
            
    def apply(self, book, c):
        pages = book.getchildren()
        for i in xrange(0, len(pages) - 1):
            a_paragraphs = pages[i].getchildren()
            if (len(a_paragraphs) != 0):
                a_last = a_paragraphs[-1]
                a_last_info = common.paraExtract(a_last)
                if (a_last_info['complete'] == False):
                    b_paragraphs = pages[i + 1].getchildren()
                    if (len(b_paragraphs) > 0):
                        b_first = b_paragraphs[0]
                        b_first_info = common.paraExtract(b_first)
                        if (a_last_info['height'] == b_first_info['height']):
                            # merge, lines are the same height                    
                            common.mergeParagraphsBtoA(a_last, b_first)
                            # now remove b_first from page
                            pages[i + 1].remove(b_first)
        return book

    def requirements(self):
        return {}

mergeMultiPageParagraphs = _mergeMultiPageParagraphs()
