# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 22:15:16 2020

@author: Kundan Jha
"""

from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QAction
import pandas as pd
import  csv, io

class About(QtWidgets.QDialog):
    def __init__(self):
        super(About, self).__init__()
        self.data_tmp_flag=0
        uic.loadUi('About.ui', self)
        
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.data_tmp_flag=0
        uic.loadUi('CSV_viewer_layout.ui', self)
        #self.model = pandasModel(data)
        #self.data=data
        #self.data_load()
        self.file_open()
        self.applied_filter=''
        ##self.comboBox.clear()
        #self.columns_data=columns_data
        #self.comboBox.addItems(self.columns_data)
        self.actionOpen.triggered.connect(self.file_open)
        self.actionExit.triggered.connect(self.file_exit)
        self.actionAbout.triggered.connect(self.show_about)
        #self.tableView.setModel(self.model)
        self.lineEdit.editingFinished.connect(self.handleEditingFinished)
        # install event filter
        self.tableView.installEventFilter(self)
        self.show()
       
    #Connecting database
    def data_load(self):
        if not self.lineEdit.text():
            print('no filter')
            self.data_tmp_flag=0
            self.model = pandasModel(self.data)
            self.label.setText('')
            self.applied_filter=''
            self.tableView.setModel(self.model)
        if self.data_tmp_flag:
            if self.lineEdit.text():
                try:
                    try:
                        selected_column=str(self.comboBox.currentText())
                        self.data_temp=self.data_temp.loc[(self.data_temp[selected_column].str.contains(self.lineEdit.text()))]
                        self.model = pandasModel(self.data_temp)
                        self.tableView.setModel(self.model)
                        self.applied_filter+=selected_column+self.lineEdit.text()+'\n'
                        self.label.setText(self.applied_filter)
                        print('.....')
                    except:
                        selected_column=str(self.comboBox.currentText())
                        self.data_temp=self.data_temp.loc[(self.data_temp[selected_column]==int(self.lineEdit.text()))]
                        self.model = pandasModel(self.data_temp)
                        self.tableView.setModel(self.model)
                        self.applied_filter+=selected_column+self.lineEdit.text()+'\n'
                        self.label.setText(self.applied_filter)
                        print('......')
                except:
                    self.data_temp=data.dropna()
                    try:
                        selected_column=str(self.comboBox.currentText())
                        self.data_temp=self.data_temp.loc[(self.data_temp[selected_column].str.contains(self.lineEdit.text()))]
                        self.model = pandasModel(self.data_temp)
                        self.tableView.setModel(self.model)
                        self.applied_filter+=selected_column+self.lineEdit.text()+'\n'
                        self.label.setText(self.applied_filter)
                        print('.......')
                    except:
                        selected_column=str(self.comboBox.currentText())
                        self.data_temp=self.data_temp.loc[(self.data_temp[selected_column]==int(self.lineEdit.text()))]
                        self.model = pandasModel(self.data_temp)
                        self.tableView.setModel(self.model)
                        self.applied_filter+=selected_column+self.lineEdit.text()+'\n'
                        self.label.setText(self.applied_filter)
                        print('........')
                    #print('not found')
        if not self.data_tmp_flag:
            try:
                if self.lineEdit.text():
                    try:
                        selected_column=str(self.comboBox.currentText())
                        self.data_temp=self.data.loc[(self.data[selected_column].str.contains(self.lineEdit.text()))]
                        self.data_tmp_flag=1
                        self.model = pandasModel(self.data_temp)
                        self.tableView.setModel(self.model)
                        self.applied_filter+=selected_column+self.lineEdit.text()+'\n'
                        self.label.setText(self.applied_filter)
                        print('.')
                    except:
                        selected_column=str(self.comboBox.currentText())
                        self.data_temp=self.data.loc[(self.data[selected_column]==int(self.lineEdit.text()))]
                        self.data_tmp_flag=1
                        self.model = pandasModel(self.data_temp)
                        self.tableView.setModel(self.model)
                        self.applied_filter+=selected_column+self.lineEdit.text()+'\n'
                        self.label.setText(self.applied_filter)
                        print('..')
            except:
                self.data_temp=self.data.dropna()
                try:
                    selected_column=str(self.comboBox.currentText())
                    self.data_temp=self.data_temp.loc[(self.data_temp[selected_column].str.contains(self.lineEdit.text()))]
                    self.data_tmp_flag=1
                    self.model = pandasModel(self.data_temp)
                    self.tableView.setModel(self.model)
                    self.applied_filter+=selected_column+self.lineEdit.text()+'\n'
                    self.label.setText(self.applied_filter)
                    print('...')
                except:
                    selected_column=str(self.comboBox.currentText())
                    self.data_temp=self.data_temp.loc[(self.data_temp[selected_column]==int(self.lineEdit.text()))]
                    self.data_tmp_flag=1
                    self.model = pandasModel(self.data_temp)
                    self.tableView.setModel(self.model)
                    self.applied_filter+=selected_column+self.lineEdit.text()+'\n'
                    self.label.setText(self.applied_filter)
                    print('....')
                #print('not found')

    # add event filter
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress and
            event.matches(QtGui.QKeySequence.Copy)):
            self.copySelection()
            return True
        return super(Ui, self).eventFilter(source, event)
    
    # add copy method
    def copySelection(self):
        selection = self.tableView.selectedIndexes()
        if selection:
            print('something selected')
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream).writerows(table)
            QtWidgets.qApp.clipboard().setText(stream.getvalue())
    def handleEditingFinished(self):
        if self.lineEdit.isModified():
            print('editing finished')
            self.data_load()
        self.lineEdit.setModified(False)
    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "CSV Files (*.csv)")

        if path:
            try:
                self.data=pd.read_csv(path)
                print(path)
                self.columns_data=list(self.data.columns.values)
                self.comboBox.clear()
                self.columns_data=list(self.data.columns.values)
                self.comboBox.addItems(self.columns_data)
                self.model = pandasModel(self.data)
                self.tableView.setModel(self.model)
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.data=pd.read_csv(self.path)
                self.columns_data=list(self.data.columns.values)
                self.comboBox.clear()
                self.columns_data=list(self.data.columns.values)
                self.comboBox.addItems(self.columns_data)
                self.tableView.setModel(self.model)
                #self.update_title()
    def file_exit(self):
        sys.exit(0)
    #def file_save(self):
        #self.data_temp.to_csv('Exported_Data.csv')
    def file_save(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "CSV Files (*.csv)")
        if path:
            try:
                self.data_temp.to_csv(path, index=False)
            #except Exception as e:
                #self.dialog_critical(str(e))
            except:
                self.path = path
                self.data.to_csv(self.path, index=False)
    def show_about(self):
        abt=About()
        if abt.exec_():
            print('Open about dialog')
        else:
            print('Closed About')
        
class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index[col]
        return None

 
#data=pd.read_csv('Book23.csv')
#columns_data=list(data.columns.values)
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()