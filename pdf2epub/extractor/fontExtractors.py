from lxml import etree
import pdf2epub.common as common
import bisect

class _fontSizeExtractor():
    def __init__(self):
        self.table = {
            7    : 'xx-small',
            7.5  : 'x-small',
            10   : 'small',
            12   : 'medium',
            13.5 : 'large',
            14   : 'larger',
            18   : 'x-large',
            24   : 'xx-large'
        }

        self.sizes = [7, 7.5, 10, 12, 13.5, 14, 18, 24]
        self.smallest = 7
        self.largest  = 24

    def apply(self, token, c):
        info = common.tokenExtract(token)
        sz   = info['font-size']
        s    = "unknown"
        if (sz < self.smallest):
            s = 'xx-small'
        elif (sz > self.largest):
            s = 'xx-large'
        else:
            v = bisect.bisect_right(self.sizes, sz)
            s = self.table[self.sizes[v]]
        token.set('size', unicode(s))
            


fontSizeExtractor = _fontSizeExtractor()
