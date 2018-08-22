from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from .abstractions import DataMedium, Data

class TableWidget(QtWidgets.QTableWidget):

    DEFAULT_ROWS = 100
    DEFAULT_COLS = 100
    
    def __init__(self, *args):
        stylesheet_1 = "::section{Background-color:rgb(216,233,250);}"
        stylesheet_2 = (
        "QHeaderView::section{""border-right:1px solid #D8D8D8;""border-bottom: 1px solid #D8D8D8;}"
        "QTableCornerButton::section{border-right:1px solid #D8D8D8;border-bottom: 1px solid #D8D8D8;background-color:#d8e9fa;}")
        QtWidgets.QTableWidget.__init__(self, *args)

        self.gridLayout = QtWidgets.QGridLayout(args[0])
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout_tab_1")

        self.gridLayout.addWidget(self, 0, 0, 1, 1)
        
        self.setGeometry(QtCore.QRect(0, 0, -1, -1))
        self.setAutoFillBackground(False)
        self.setShowGrid(True)
        self.setGridStyle(QtCore.Qt.SolidLine)
        self.setWordWrap(True)
        self.setRowCount(self.DEFAULT_ROWS)
        self.setColumnCount(self.DEFAULT_COLS)
        self.setObjectName("tableWidget")
        self.setStyleSheet(stylesheet_1)
        self.horizontalHeader().setStyleSheet(stylesheet_2)
        self.horizontalHeader().setVisible(True)
        self.horizontalHeader().setCascadingSectionResizes(False)
        self.verticalHeader().setStyleSheet(stylesheet_2)
        self.verticalHeader().setVisible(True)
        self.verticalHeader().setCascadingSectionResizes(False)
        self.verticalHeader().setHighlightSections(True)
        self.verticalHeader().setSortIndicatorShown(False)
        self.verticalHeader().setStretchLastSection(False)
        self.setItemPrototype(self.CustomTableWidgetItem())

        self.cellChanged.connect(self.cell_changed)

        self.dataMedium = self.TableWidgetDataMedium(self)

    def load_data(self, all_data, *args, rowOffset=0, colOffset=0, **kwargs):
        """
        Load data into the table
        :param all_data: The data to load
        :type all_data: Data
        """
        data = all_data.get_data()
        columns = all_data.get_headers()
        
        if rowOffset+data.shape[0] > self.rowCount()-10:
            self.setRowCount(rowOffset+data.shape[0]+10)
        if colOffset+data.shape[1] > self.columnCount()-10:
            self.setColumnCount(colOffset+data.shape[1]+10)
        
        for i, row in enumerate(data):
            for j, elem in enumerate(row):
                self.setItem(rowOffset+i, colOffset+j, self.CustomTableWidgetItem(str(elem)))

        if columns is not None:
            if len(set(columns)) < len(columns):
                raise ValueError("Duplicate column name")
            else:
                newHeaders = []
                for i in range(0, colOffset):
                    newHeaders.append(str(i) if self.horizontalHeaderItem(i) is None else self.horizontalHeaderItem(i).text())
                newHeaders = newHeaders + columns
                self.setHorizontalHeaderLabels(newHeaders)
        
    def get_data(self):
        """
        Return the data in the table for use in other modules
        either as a matrix X or as a pair (X,y) of features and target.
        :param selection: Selection of data to use, all the available data by default
        :param target: Column to use as target (y). None by default
        :type selection: QTableWidgetSelectionRange
        :type target: str
        """
        if len(self.selectedRanges()) > 0:
            return self.get_selection()
        else:
            #Get columns which contain data
            columns = [x for x in range(0,self.columnCount()) if self.item(0,x) is not None]
            selection = []
            for col in columns:
                selection.append(QtWidgets.QTableWidgetSelectionRange(0, col, self.columnCount()-1, col))

            return self.is_column_selection(selection)[1]
        

    def cell_changed(self, row, col):
        #Internal use. Keep track of the rows and columns used
        if row > self.rowCount()-10:
            self.setRowCount(row+10)
        if col > self.columnCount()-10:
            self.setColumnCount(col+10)

            
    def get_selection(self):
        sel = self.selectedRanges()

        is_col = self.is_column_selection(sel)
        is_row = (False, -1)
        is_rect = (False, -1, -1)
        if is_col[0]:
            return is_col[1]
        else:
            is_row = self.is_row_selection(sel)
            
        if is_row[0]:
            return is_row[1]
        else:
            is_rect = self.is_rect_selection(sel)
            
        if is_rect[0]:
            return is_rect[1]
        else:
            raise ValueError("Not a valid selection")
        

    def is_column_selection(self, sel):
        # Test if the given selection is a column selection    
        if all(range_.leftColumn() == range_.rightColumn() and range_.topRow() == 0 and range_.bottomRow() == self.rowCount()-1 for range_ in sel):
            maxRow = 1
            for range_ in sel:
                for row in range(self.rowCount()):
                    if self.item(row, range_.leftColumn()) is not None and maxRow < row:
                        maxRow = row

            data = np.array([np.zeros(len(sel)) for i in range(maxRow+1)])
            col = 0
            column_names = []
            for range_ in sel:
                column_names.append(self.horizontalHeaderItem(range_.leftColumn()).text())
                for row in range(range_.topRow(), range_.topRow()+data.shape[0]):
                    try:
                        data[row, col] = float(self.item(row, range_.leftColumn()).text())
                    except AttributeError:
                        # item is None, cell is empty
                        data[row, col] = 0
                    except ValueError as err:
                        raise ValueError("The value at (" + row + "," + range_.leftColumn() +
                                         ") is not a number", err)
                col += 1
                
            return True, Data(data, column_names)
        else:
            return False, Data([])

                            
    def is_row_selection(self, sel):
         # Test if the given selection is a row selection
        if all(range_.topRow() == range_.bottomRow() and range_.leftColumn() == 0 and range_.rightColumn() == self.columnCount()-1 for range_ in sel):
            maxCol = 1
            for range_ in sel:
                for col in range(self.columnCount()):
                    if self.item(range_.topRow(), col) is not None and maxCol < col:
                        maxCol = col

            data = np.array([np.zeros(maxCol+1) for i in range(len(sel))])
            row = 0
            column_names = [self.horizontalHeaderItem(i).text() for i in range(range_.leftColumn(), range_.leftColumn()+data.shape[1])]
            for range_ in sel:
                for col in range(range_.leftColumn(), range_.leftColumn()+data.shape[1]):
                    try:
                        data[row, col] = float(self.item(range_.topRow(), col).text())
                    except AttributeError:
                        # item is None, cell is empty
                        data[row, col] = 0
                    except ValueError as err:
                        raise ValueError("The value at (" + range_.topRow() + "," + col +
                                         ") is not a number", err)
                row += 1
                
            return True, Data(data, column_names)
        else:
            return False, Data([])
        

    def is_rect_selection(self, sel):
        if len(sel) == 1:
            rows = sel[0].bottomRow()-sel[0].topRow()+1
            cols = sel[0].rightColumn()-sel[0].leftColumn()+1

            data = np.array([np.zeros(cols) for i in range(rows)])
            
            dataRow = 0
            column_names = [self.horizontalHeaderItem(i).text() for i in range(sel[0].leftColumn(), sel[0].leftColumn()+data.shape[1])]
            for row in range(sel[0].topRow(), sel[0].bottomRow()+1):
                dataCol = 0
                for col in range(sel[0].leftColumn(), sel[0].rightColumn()+1):
                    try:
                        data[dataRow, dataCol] = float(self.item(row, col).text())
                    except AttributeError:
                        # item is None, cell is empty
                        data[dataRow, dataCol] = 0
                    except ValueError as err:
                        raise ValueError("The value at (" + row + "," + column +
                                         ") is not a number", err)
                    dataCol += 1
                dataRow += 1
            return True, Data(data, column_names)
        else:
            return False, Data([])
                    
    class CustomTableWidgetItem(QtWidgets.QTableWidgetItem):
        # Custom table item with specified alignment
        def __init__(self, *args, align=QtCore.Qt.AlignCenter,
                     type=QtWidgets.QTableWidgetItem.UserType, **kwargs):
            super().__init__(*args, type=type, **kwargs)
            self.setTextAlignment(align)


    class TableWidgetDataMedium(DataMedium):
        # Data medium of the table, just a sort of adapter to avoid multiple inheritance issues
        def __init__(self, table):
            self.table = table
        
        def store_data(self, data, *args, **kwargs):
            self.table.load_data(data, *args, **kwargs)

        def get_data(self, *args, **kwargs):
            return self.table.get_data()
