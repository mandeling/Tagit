# editable table view for tags:
# insert, remove, edit color
# 

from PyQt5.QtCore import QItemSelectionModel, Qt
from PyQt5.QtWidgets import (QHeaderView, QTableView, QMenu, QAction, QMessageBox)

from Model.TagModel import TagModel, TagDelegate


class TagTableView(QTableView):
    def __init__(self, header, parent=None):
        super(TagTableView, self).__init__(parent)

        # table style
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStyleSheet("QHeaderView::section{background:#eee;}")
        self.setSelectionMode(QTableView.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setAlternatingRowColors(True)
        self.resizeColumnsToContents()

        # model
        model = TagModel(header)
        self.setModel(model)

        # delegate
        delegate = TagDelegate()
        self.setItemDelegate(delegate)

        # context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.customContextMenu)

    def setup(self, data=[], selected_key=-1):
        '''reset tag table with specified model data,
           and set the row with specified key as selected
        '''
        self.model().setup(data)
        self.reset()
        # set selected item
        index = self.model().getIndexByKey(selected_key)        
        if index.isValid():
            # self.selectionModel().select(index, QItemSelectionModel.ClearAndSelect)
            self.selectionModel().setCurrentIndex(index, QItemSelectionModel.ClearAndSelect)

    def customContextMenu(self, position):
        '''show context menu'''
        indexes = self.selectedIndexes()
        if not len(indexes):
            return

        # init context menu
        menu = QMenu()
        menu.addAction(self.tr("Create Tag"), self.slot_insertRow)
        menu.addSeparator()
        act_rv = menu.addAction(self.tr("Remove Tag"), self.slot_removeRow)

        # set status
        model = self.model()
        s = not model.isDefaultItem(indexes[0])
        act_rv.setEnabled(s)

        menu.exec_(self.viewport().mapToGlobal(position))

    def slot_finishedEditing(self, index):
        self.closePersistentEditor(index)

    def slot_insertRow(self):
        '''inset item at the same level with current selected item'''
        index = self.selectionModel().currentIndex()
        model = self.model()

        row = index.row() + 1
        if model.insertRow(row, index.parent()):
            child_key = model.index(row, 0, index.parent())
            child_name = model.index(row, 1, index.parent())
            child_color = model.index(row, 2, index.parent())

            # set default data
            model.setData(child_key, model.nextKey())
            model.setData(child_name, 'New Tag')
            model.setData(child_color, '#000000')
            self.selectionModel().setCurrentIndex(child_name, QItemSelectionModel.ClearAndSelect)

            # enter editing status and quit when finished
            self.openPersistentEditor(child_name)
            editWidget = self.indexWidget(child_name)
            if editWidget:
                editWidget.setFocus()
                editWidget.editingFinished.connect(lambda:self.slot_finishedEditing(child_name))


    def slot_removeRow(self):
        '''delete selected item'''
        index = self.selectionModel().currentIndex()
        reply = QMessageBox.question(self, 'Confirm', self.tr(
            "Confirm to remove '{0}'?\n"
            "Items with this TAG will not be deleted.".format(index.data())), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        
        model = self.model()
        if not model.isDefaultItem(index): 
            model.removeRow(index.row(), index.parent())




if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    config = [[1,'No Tag', '#0000ff'], [2, 'Python', '#ff0000'], [3, 'Java', '#00ff00']]

    app = QApplication(sys.argv)
    
    tag = TagTableView(['Tag', 'Color'])
    tag.setup(config,2)
    tag.show()

    sys.exit(app.exec_())  