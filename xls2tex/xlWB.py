
"""
Workbook class for xls2tex
Created on Mon Mar 23 12:47:40 2020

@author: ppenguin
"""

import openpyxl
from itertools import compress
# from . import e2lvp
from . import xlTableTeX


class xlWorkbookTeX(openpyxl.Workbook):
    
    # why does Workbook not have the load_workbook function??!!
    # so we cannot instantiate and read afterwards, unles we overwrite self?? Is this possible?
    # more importantly: do we keep our added functions?
    
    def __init__(self, filename):
        super().__init__()
        # ok, awaiting a beter solution, just copy the data
        wb = openpyxl.load_workbook(filename=filename, data_only=True)
        self._sheets = wb._sheets
               

    def getTeX(self, sheetname, textcharwidth=80, caption=None, label=None):
        
        xt = xlTableTeX.xlTableTeX(self[sheetname])
        xt.genTex(textcharwidth, caption, label)
               
        return xt.texout


    def getTeX_old(self, sheetname, booktabs=True, tabular=True, longtable=True, caption=None, label=None):
        
        usr_settings={'booktabs': booktabs, 'includetabular': tabular}
        #if roundto is None:
        #    usr_settings['roundtodp'] = False
        #else:
        #    usr_settings['roundtodp'] = True
        #    usr_settings['numdp'] = roundto
        
        sheet = self[sheetname]
        texout = ""
        
        # The table within the sheet may not start in cell A1. So find the location of the upper-left and bottom-right
        # corner cells of the table within the sheet
        start_row_idx, start_col_idx, end_row_idx, end_col_idx = e2lvp._get_table_dimensions(sheet)

        # Get the excel cell labels of the upper-left and bottom-right cells of the table
        start_cell_label = list(sheet.rows)[start_row_idx][start_col_idx].coordinate
        end_cell_label = list(sheet.rows)[end_row_idx][end_col_idx].coordinate

        # Get the number of columns and rows in the table
        num_cols = end_col_idx - start_col_idx + 1
        num_rows = end_row_idx - start_row_idx + 1

        # Trim sheet object down to just the range we care about and store this in a tuple
        table_tuple = tuple(sheet[start_cell_label:end_cell_label])

        # Print to the terminal the name of the table file that is being created this iteration and the excel cells
        # being used to create it
        # print('    ' + sheet_name + '.tex    ' + list(sheet.rows)[start_row_idx][start_col_idx].coordinate + ':'
        #      + list(sheet.rows)[end_row_idx][end_col_idx].coordinate)

        # Preamble of the individual table
        # --------------------------------

        # If the user requested the booktabs options, add a reminder (as a LaTeX comment) to the top of the table that
        # the user will need to load up the package in the preamble of their file.
        if booktabs:
            texout += "% Note: make sure \\usepackage{booktabs} is included in the preamble \n"
            texout += "% Note: If your table contains colors, make sure \\usepackage[table]{xcolor} is included in the preamble \n"

        if longtable:
            texout+= "\\begin{longtable}{@{}c@{}} \n" 
            
        if caption is not None:
            texout += "\\caption{%s}\label{%s}\\tabularnewline \n"%(caption, label)
    
        # If the user wants the table rows wrapped in the tabular environment, write the start of the begin environment
        # command to the output tex output
        if tabular:

            col_align_str = "\\begin{tabular}{"  # Preallocate string
            # For each column of the table, append to "col_align_str" any vertical dividers and alignment code for the
            # column
            for colnum in range(0, num_cols):

                # Create column to analyze from the table
                col2a = e2lvp._create_column(table_tuple, colnum)

                # check to see if there is a vline left of column
                if e2lvp._check_for_vline(col2a, 'left'):
                    col_align_str += '|'

                # Choose the alignment (l,c,r) of the column based on the majority of alignments in the column's cells
                col_align_str += e2lvp._pick_col_text_alignment(col2a)

                # check to see if there is a vline right of column
                if e2lvp._check_for_vline(col2a, 'right'):
                    col_align_str += '|'

            # Create code to write to tex output
            begin_str = str(col_align_str) + "} \n"

            # Write the \begin{tabular}{*} code to the tex content
            texout += begin_str
    
            # Body of the individual table
            # ----------------------------
    
            # Find any merged cells within this particular worksheet
            merged_details_list = e2lvp._get_merged_cells(sheet)
    
            # Adjust the merged_details_list values for the fact that the table might not start in cell A1
            merged_details_list[0] = [x - start_row_idx for x in merged_details_list[0]]  # start_row
            merged_details_list[1] = [x - start_col_idx for x in merged_details_list[1]]  # start_col
            merged_details_list[2] = [x - start_row_idx for x in merged_details_list[2]]  # end_row
            merged_details_list[3] = [x - start_col_idx for x in merged_details_list[3]]  # end_col
    
            # For each row in the table's body create a string containing the tex code for that row and write to the output
            # file
            for row_num in range(0, num_rows):
    
                # Generate list of True/False values to see if they match the row
                elem_picker = [True if item in [row_num] else False for item in merged_details_list[0]]
    
                # Pick out the column number and mutlicolumn/row details corresponding to this row
                merge_start_cols = list(compress(merged_details_list[1], elem_picker))
                merge_end_cols = list(compress(merged_details_list[3], elem_picker))
                merge_match_det = list(compress(merged_details_list[4], elem_picker))
    
                # If there is a horizontal rule across all cells at the top, add it to the table
                hrule_str = e2lvp._create_horzrule_code(table_tuple[row_num], 'top', merge_start_cols, merge_end_cols, usr_settings)
    
                # If user requested booktabs, and this is the first row, use toprule rather than midrule
                if (row_num == 0) and usr_settings['booktabs']:
                    hrule_str = hrule_str.replace('\\midrule', '\\toprule')
    
                texout += hrule_str
    
                # Get string of rows contents
                str_2_write = e2lvp._tuple2latexstring(table_tuple[row_num], usr_settings, [merge_start_cols, merge_end_cols,
                                                                                       merge_match_det])
    
                # Write row string to file
                texout += str_2_write
    
                # Add any horizontal rule below the row
                hrule_str = e2lvp._create_horzrule_code(table_tuple[row_num], 'bottom', merge_start_cols, merge_end_cols,
                                                  usr_settings)
    
                # If user requested booktabs, and this is the final row, use bottomrule rather than midrule
                if (row_num == num_rows - 1) & usr_settings['booktabs']:
                    hrule_str = hrule_str.replace('\\midrule', '\\bottomrule')
    
                texout += hrule_str
    
            # Postamble of the individual table
            # ---------------------------------
            if usr_settings['includetabular']:
                # User has requested tabular environment wrapped around the table rows, so end the table
                texout += "\\end{tabular} \n"
                
            if longtable:
                texout+= "\\end{longtable} \n"
    
            return texout

