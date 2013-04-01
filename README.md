pdf2epub
=======

pdf2epub is a tool which converts pdf files to epubs using [pdftoxml](http://sourceforge.net/projects/pdf2xml/) (also called pdf2xml) as an intermediary format. 

The primary aim is to convert pdfs that look like books, i.e single column, justified, with the occasional title into something which is readable (although probably not perfect) on an ereader like the Kindle.

*warning* pdf2epub is a work in progress. 

Requirements
------------

1. pdf2xml
2. python 2.7.3 (only tested with - other higher versions may work) with lxm module

Instructions
------------

1. Convert your pdf file to xml using pdf2xml
2. Convert your xml file to epub using pdf2epub (currently only very basic output is working)

Description
-----------

The general flow of pdf2epub is to use the xml output from pdf2xml, which breaks down a pdf into pages with text and token elements. All tokens (which typically represent a single world) have positioning (x and y on the page) and formatting (font type, size) information associated with them.

This xml output is processed using various heuristics to group tokens into lines and paragraphs which can then be converted into HTML. Effectively this will allow the ereader to re-flow the text from the pdf based on the screen size etc.

Contributors
------------

Iain Bullard

Copyright (C) 2013 Iain Bullard

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

