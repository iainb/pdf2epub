from lxml import etree

def copyElementAttributes(e):
    o = etree.Element(e.tag)
    for name in e.keys():
        o.set(name, e.get(name))
    return o

def tokenExtract(token):
    o = {}
    o['font-name']   = token.get('font-name')
    o['symbolic']    = True if token.get('symbolic') == "yes" else False
    o['fixed-width'] = True if token.get('fixed-width') == "yes" else False
    o['bold']        = True if token.get('bold') == "yes" else False
    o['italic']      = True if token.get('italic') == "yes" else False
    o['font-size']   = float(token.get('font-size'))
    o['font-color']  = token.get('font-color')
    o['rotation']    = float(token.get('rotation'))
    o['angle']       = float(token.get('angle'))
    o['x']           = float(token.get('x'))
    o['y']           = float(token.get('y'))
    o['base']        = float(token.get('base'))
    o['width']       = float(token.get('width'))
    o['height']      = float(token.get('height'))
    o['top']         = o['base'] - o['height']
    o['left']        = o['x']
    o['right']       = o['left'] + o['width']
    o['size']        = token.get('size','unknown')

    if (token.text != None):
        o['chars'] = len(token.text)
    else:
        o['chars'] = 0

    return o

def lineExtract(line):
    o = {}
    o['base']   = float(line.get('base'))
    o['top']    = float(line.get('top'))
    o['left']   = float(line.get('left'))
    o['right']  = float(line.get('right'))
    o['height'] = float(line.get('height'))
    o['chars']  = float(line.get('chars'))
    return o

def paraExtract(para):
    o = {}
    o['complete'] = True if para.get('complete') == "yes" else False
    o['base']     = float(para.get('base'))
    o['top']      = float(para.get('top'))
    o['left']     = float(para.get('left'))
    o['right']    = float(para.get('right'))
    o['chars']    = float(para.get('chars'))
    o['height']   = float(para.get('height'))
    o['lines']    = float(para.get('lines'))
    return o

def mergeLinesBtoA(a,b):
    for token in b.iter('TOKEN'):
        a.append(token)
    return a

def mergeParagraphsBtoA(a,b):
    for line in b.iter('LINE'):
        a.append(line)
    return a

def looseCompare(a,b,diff):
    if (a > b):
        val = a - b
    else:
        val = b - a

    if (val < diff):
        return True
    else:
        return False

def mostCommon(l):
    count = {}
    for el in l:
        if el not in count:
            count[el] = 0
        count[el] += 1
    m = None
    for el in count:
        if (m == None):
            m = el
        if count[el] > count[m]:
            m = el
    return  m

def smallest(l):
    m = None
    for i in l:
        if (m == None):
            m = i
        if (i < m):
            m = i
    return m

def largest(l):
    m = None
    for i in l:
        if (m == None):
            m = i
        if (i > m):
            m = i
    return m

