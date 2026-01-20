
"""
Workbook class for xls2latex
Created on Mon Mar 23 12:47:40 2020

@author: ppenguin
"""

import openpyxl
from itertools import compress
from xls2latex import xlTableTeX


class xlWorkbookTeX(openpyxl.Workbook):

    # why does Workbook not have the load_workbook function??!!
    # so we cannot instantiate and read afterwards, unles we overwrite self?? Is this possible?
    # more importantly: do we keep our added functions?

    def __init__(self, filename):
        super().__init__()
        # ok, awaiting a beter solution, just copy the data
        wb = openpyxl.load_workbook(filename=filename, data_only=True)
        self._sheets = wb._sheets


    def getTeX(self, sheetname, textcharwidth=80, caption=None, label=None, colwidths=None, vfix=None, smalltext=False):

        xt = xlTableTeX.xlTableTeX(self[sheetname], textcharwidth, caption, label, colwidths, vfix, smalltext)
        xt.genTex()

        return xt.texout

