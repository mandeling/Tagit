# editable tree view for groups:
# append, insert child, remove, edit text
# 

from PyQt5.QtCore import (QItemSelectionModel, Qt, pyqtSignal)
from PyQt5.QtWidgets import (QTreeView, QMenu, QAction, QMessageBox)

from models.GroupModel import GroupModel

class GroupTreeView(QTreeView):

    groupRemoved = pyqtSignal(list)

    def __init__(self, header, parent=None):
        ''':param headers: header of tree, e.g. ('name', 'value')
        '''
        super(GroupTreeView, self).__init__(parent)

        # init tree
        self.resizeColumnToContents(0)
        self.setAlternatingRowColors(True)
        self.header().hide()
        self.expandAll()

        # model
        self.sourceModel = GroupModel(header)
        self.setModel(self.sourceModel)

        # context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.customContextMenu)

    def setup(self, data=[], selected_key=2):
        '''reset tree with specified model data,
           and set the item with specified key as selected
        '''
        self.sourceModel.setup(data)       

        # refresh tree view to activate the model setting
        self.reset()
        self.expandAll()

        # set selected item
        index = self.sourceModel.getIndexByKey(selected_key)
        if index.isValid():
            self.selectionModel().select(index, QItemSelectionModel.ClearAndSelect)

    def customContextMenu(self, position):
        '''show context menu'''
        indexes = self.selectedIndexes()
        if not len(indexes):
            return

        # init context menu
        menu = QMenu()
        menu.addAction(self.tr("Create Group"), self.slot_insertRow)
        act_sb = menu.addAction(self.tr("Create Sub-Group"), self.slot_insertChild)
        menu.addSeparator()
        act_rv = menu.addAction(self.tr("Remove Group"), self.slot_removeRow)

        # set status
        s = not self.sourceModel.isDefaultItem(indexes[0])
        act_sb.setEnabled(s)
        act_rv.setEnabled(s)

        menu.exec_(self.viewport().mapToGlobal(position))

    def slot_insertChild(self):
        '''insert child item under current selected item'''
        index = self.selectionModel().currentIndex()

        # could not insert sub-items to default items
        if self.sourceModel.isDefaultItem(index):
            return

        # insert
        if self.sourceModel.insertRow(0, index):
            child = self.sourceModel.index(0, 0, index)
            self.sourceModel.setData(child, "[Sub Group]")
            self.selectionModel().setCurrentIndex(child, QItemSelectionModel.ClearAndSelect)

    def slot_insertRow(self):
        '''inset item at the same level with current selected item'''
        index = self.selectionModel().currentIndex()

        # could not prepend item to default items
        row = 3 if self.sourceModel.isDefaultItem(index) else index.row() + 1
        if self.sourceModel.insertRow(row, index.parent()):
            child = self.sourceModel.index(row, 0, index.parent())
            self.sourceModel.setData(child, "[New Group]")
            self.selectionModel().setCurrentIndex(child, QItemSelectionModel.ClearAndSelect)

    def slot_removeRow(self):
        '''delete selected item'''
        index = self.selectionModel().currentIndex()

        reply = QMessageBox.question(self, 'Confirm', self.tr(
            "Confirm to remove '{0}'?\n"
            "The items under this group will not be deleted,"
            " but moved to Ungrouped.".format(index.data())), 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply != QMessageBox.Yes:
            return        
        
        # ATTENTION: get the key before any actions are applied to the tree model
        keys = index.internalPointer().keys()
        if not self.sourceModel.isDefaultItem(index): 
            self.sourceModel.removeRow(index.row(), index.parent())
            # emit removing group signal
            self.groupRemoved.emit(keys)


    def slot_updateCounter(self, items):
        '''update count of items for each group
           :param items: the latest items list
        '''
        self.sourceModel.updateItems(items)