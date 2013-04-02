from lxml import etree
import pdf2epub.common as common

class _mergeTrailingHyphens():
    def __init__(self):
        pass
    
    def apply(self, para, c):
        lines = para.getchildren()
        for i in xrange(0, len(lines) - 1):
            cur_tokens = lines[i].getchildren()
            cur_last   = cur_tokens[-1] 
            if (cur_last.text[-1] == "-"):
                # hyphenated end of line found - merge word
                next_tokens = lines[i + 1].getchildren()
                next_first  = next_tokens[0]
                cur_last.text = cur_last.text[:-1] + next_first.text
                lines[i + 1].remove(next_first)

    def requirements(self):
        return {}

mergeTrailingHyphens = _mergeTrailingHyphens()
