from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

class TableWidget(QtWidgets.QTableWidget):

    DEFAULT_ROWS = 10000
    DEFAULT_COLS = 1000
    
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
        self.maxRow = 0
        self.maxCol = 0


    def load_data(self, data, columns=[]):
        """
        Load data into the table
        :param data: The data to load
        :param columns: Names of columns
        :type data: ndarray, shape=(n_samples, n_features)
        :type columns: array-like, shape=(n_features)
        """
        for i, row in enumerate(data):
            for j, elem in enumerate(row):
                self.setItem(i, j, self.CustomTableWidgetItem(str(elem)))

        if len(columns) > 0:
            if len(set(columns)) < len(columns):
                raise ValueError("Duplicate column name")
            else:
                self.setHorizontalHeaderLabels(columns)
        
    def get_data(self, selection=None, target=None):
        """
        Return the data in the table for use in other modules
        as a pair (X,y) of features and target.
        :param selection: Selection of data to use, all the available data by default
        :param target: Column to use as target (y). Last one by default
        :type selection: QTableWidgetSelectionRange
        :type target: str
        """
        if selection is not None:
            raise NotImplementedError("Data selection NYI")
        else:
            #Get columns which contain data
            columns = [x for x in range(0,self.maxCol) if self.item(0,x) is not None]
            if len(columns) < 2 or self.maxRow == 0:
                raise ValueError("Not enough data, at least two columns and one row required")
            
            if target is None:
                #Default target column
                target_column = columns[-1]
            else:
                pos_target_columns = [col for col in columns
                                      if self.horizontalHeaderItem(col) == target]
                if len(pos_target_columns) == 0:
                    raise ValueError("No column named " + target)
                target_column = pos_target_columns[0]


            y = np.zeros(self.maxRow)
            X = np.array([np.zeros(self.maxRow) for i in range(columns-1)])
            for col in columns:
                # Store the column in y or X depending on column
                if col == target_column:
                    storage = y
                else:
                    storage = X[col]
                    
                for row in range(0, maxCol):
                    try:
                        storage[row] = float(self.item(row, col).text())
                    except AttributeError:
                        # item is None, cell is empty
                        raise ValueError("All columns must have the same number of rows.\n" +
                                         "The cell at (" + row + "," + column +") is empty")
                    except ValueError as err:
                            raise ValueError("The value at (" + row + "," + column +
                                             ") is not a number", err)

            # Note that we have been indexing X by columns. We need to transpose it
            X = X.transpose()
            return (X,y)
        

    def cell_changed(self, row, col):
        #Internal use. Keep track of the rows and columns used
        if row > self.maxRow:
            self.maxRow = row
        if col > self.maxCol:
            self.maxCol = col

            
    def get_selection(self):
        data = np.arrange
        sel = self.selectedRanges()
        for range_ in sel:
            for row in range(range_.topRow(), min(range_.bottomRow()+1, self.maxRow)):
                for col in range(range_.leftColumn(), min(range_.rightColumn()+1, self.maxCol)):
                    item = self.item(row,col)
                    print(0 if item is None else item.text())

                    
    class CustomTableWidgetItem(QtWidgets.QTableWidgetItem):
        # Custom table item with specified alignment
        def __init__(self, *args, align=QtCore.Qt.AlignCenter,
                     type=QtWidgets.QTableWidgetItem.UserType, **kwargs):
            super().__init__(*args, type=type, **kwargs)
            self.setTextAlignment(align)
