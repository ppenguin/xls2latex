#! /usr/bin/env python

"""
xls2tex
Created on Mon Mar 23 12:47:40 2020
@author: ppenguin

Based on https://github.com/michaelkirker/excel2latexviapython by Michael Kirker

Script to convert excel tables to LaTeX code, intended to be used as a filter, e.g. executed from a 
LaTeX macro.

Tested in a pandoc environment with the following:
    
testdoc.md:
    ...
    \input{|"xls2tex -f myfile.xlsx"}
    ...
    
pandoc command:
    pandoc --filter=pandoc-citeproc --filter=pandoc-xnos \
        --pdf-engine=xelatex --pdf-engine-opt=-shell-escape \
        -i testdoc.md -o testdoc.pdf

TODO: 
    - does it also work on Windows?
    - better format handling (e.g. number formats from excel file)

"""

from argparse import ArgumentParser
import re
import os
from xls2tex.xlWB import xlWorkbookTeX


# match multiple arguments to the sheet argument in order of occurence, or return empty if #sheets > #argame
def matchSheetOpt(argns, sheetname, argname):
    try:
        ret = argns[argname][argns.sheets.index(sheetname)]
    except:
        ret = vars(argns)[argname]   # if specified only once even with more sheets, just always take the specified value. 
                                     # This can lead to multiple occurences of a caption or label!!!
    return ret


# harmonise options according to precedence, implication and mutual exlusivity
def harmoniseOpt(argns):
    if argns.caption is not None:
        argns.sheetcaption = False

    if not (argns.caption is None and argns.nosheetcaption):
        argns.longtable = True
        
        
def caption2label(caption):
    return 'tbl:' + re.sub('[^\w\-]','',caption.strip().replace(' ','-')).lower()
    

if __name__ == '__main__':
    
    parg = ArgumentParser(description="Reads a given xls(x) file and outputs the contents of its worksheets as LaTeX tables. \n \
                          Designed for use in automated workflows for LaTeX processing, e.g. like so: \n \
                              \\input{|\"xls2tex -f myfile.xlsx\"}",
                          epilog="Since in LaTeX shell escaping becomes difficult, best is to avoid arguments with spaces or enclose in single quotes (') if called from LaTeX.")
    parg.add_argument("-f", "--file", dest="filename", required=True, type=str, help="input file (xls(x))")
    parg.add_argument("-s", "--sheet", dest="sheets", type=str, 
                      help="worksheet name (multiple times possible). If omitted, all worksheets are parsed.", action="append")
    # parg.add_argument("-b", "--booktabs", dest="booktabs", type=bool, default=True, 
    #                   help="(True/False) Use the booktabs package functions to make prettier horizontal lines. Default: True.")
    # parg.add_argument("-t", "--tabular", dest="tabular", type=bool, default=True, 
    #                  help="(True/False) Should the code include the tabular environment code around the table (\begin{tabular}, \end{tabular}), \
    #                      or just return the table rows.  Default: True." )
    # parg.add_argument("-l", "--longtable", dest="longtable", type=bool, 
    #                  help="If specified, enclose output (per table) in \longtable environment")
    # parg.add_argument("-r", "--roundto", dest="roundto", type=int, 
    #                  help="--roundto (int) If specified, rounds all numbers in the table to the given number of decimal places")
    # parg.add_argument("--thsep", dest="thsep", type=str, default="'", 
    #                  help="Thousands separator, defaults to ' (Yes, becasue it is nicely unambiguous because some countries use a decimal comma!)")
    parg.add_argument("-c", "--caption", dest="caption", type=str, 
                      help="If specified, include a table caption. Implies --longtable=True")
    parg.add_argument("--label", dest="label", type=str, 
                      help="--label=labeltext: Includes a \label{tabletext} with the caption. Only has an effect if --caption is defined.")
    parg.add_argument("--nosheetcaption", dest="nosheetcaption", default=False, action='store_true',
                      help="Do not use the worksheet name as the caption name when no explicit caption is given. The effect is no caption.")
    parg.add_argument("-e", "--with-stderr", dest="withstderr", default=False, action='store_true',
                      help="Use an internal redirect 2>&1 instead of the default 2>/dev/null.")

    optarg = parg.parse_args()
    # automatically exits on error, so we have the required arguments when we arrive here
    
    # the LaTeX pipe bombs on stderr (apparently), even if we don't output stuff to stderr
    # so redirect, unless user wants debug output in the final document (sensitive to invalid LaTeX characters!)
    # fd = os.open('/dev/null', os.O_WRONLY)
    if optarg.withstderr:
        os.dup2(1, 2) # equivalent of appending 2>&1 to the command line
    else:
        fd = os.open('/dev/null', os.O_WRONLY)
        os.dup2(fd, 2)
                
    harmoniseOpt(optarg)
  
    wb = xlWorkbookTeX(optarg.filename)
    
    # process all sheets
    if optarg.sheets is None:
        sheets = wb.sheetnames
    else:
        sheets = optarg.sheets

    # process selected sheets    
    for s in sheets:    
        if s in wb.sheetnames:
            c = matchSheetOpt(optarg, s, "caption")
            l = matchSheetOpt(optarg, s, "label")
            if c is None and not optarg.nosheetcaption:
                c = s
            if l is None and not optarg.nosheetcaption:
                l = caption2label(c)

            print(wb.getTeX(s, caption=c, label=l))
            print() # linefeed, on to the next table (if any)
    
        
    