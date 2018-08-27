import sys
import pyudev
import psutil

from PyQt5.QtCore import QAbstractListModel, QStringListModel, QModelIndex, Qt
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QWidget, QComboBox, QVBoxLayout, QPushButton, QHBoxLayout
from QtPyVCP.utilities.info import Info


class ListModel(QAbstractListModel):
    """
    Class for list management with a QAbstractListModel.
    Implements required virtual methods rowCount() and data().
    Resizeable ListModels must implement insertRows(), removeRows().
    If a nicely labeled header is desired, implement headerData().
    """

    def __init__(self, input_list, parent=None):
        super(ListModel, self).__init__(parent)
        self.list_data = []
        self.enabled = []
        for thing in input_list:
            self.append_item(thing)

    def append_item(self, thing):
        ins_row = self.rowCount()
        self.beginInsertRows(QModelIndex(), ins_row, ins_row + 1)
        self.list_data.append(thing)
        self.enabled.append(True)
        self.endInsertRows()

    def remove_item(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        self.list_data.pop(row)
        self.enabled.pop(row)
        self.endRemoveRows()

    def set_disabled(self, row):
        self.enabled[row] = False

    def flags(self, idx):
        if self.enabled[idx.row()]:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.NoItemFlags

    def rowCount(self, parent=QModelIndex()):
        return len(self.list_data)

    def data(self, idx, data_role):
        return self.list_data[idx.row()]

    def insertRows(self, row, count):
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        for j in range(row, row + count):
            self.list_data.insert(j, None)
        self.endInsertRows()

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        for j in range(row, row + count)[::-1]:
            self.list_items.pop(j)
        self.endRemoveRows()

    def headerData(self, section, orientation, data_role):
        return None


class FileSystemTree(QTreeView):

    def __init__(self, parent=None):
        super(FileSystemTree, self).__init__(parent)

        # This prevents doing unneeded initialization
        # when QtDesginer loads the plugin.
        if parent is None:
            return

        self.info = Info()

        nc_files = self.info.getProgramPrefix()

        self.model = QFileSystemModel()
        self.model.setRootPath(nc_files)
        self.model.setReadOnly(False)

        self.setModel(self.model)

        self.setRootIndex(self.model.index(nc_files))

        self.setAnimated(True)
        self.setIndentation(20)
        self.setSortingEnabled(True)


class FileSystem(QWidget):

    def __init__(self, parent=None):
        super(FileSystem, self).__init__(parent)

        # This prevents doing unneeded initialization
        # when QtDesginer loads the plugin.
        if parent is None:
            return

        self.deviceList = list()

        self.fileSystemCombo = QComboBox(self)
        self.fileSystemCombo.model = ListModel(self.deviceList, self)

        self.fileSystemCombo.setModel(self.fileSystemCombo.model)

        self.refreshfileSystemButton = QPushButton(self)
        self.refreshfileSystemButton.setText("Refresh Devices")

        self.fileSystemTree = FileSystemTree(self)

        hbox = QHBoxLayout()
        hbox.addWidget(self.fileSystemCombo)
        hbox.addWidget(self.refreshfileSystemButton)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.fileSystemTree)

        self.setLayout(vbox)

        self.refreshfileSystemButton.clicked.connect(self.scanUsb)
        self.fileSystemCombo.currentIndexChanged.connect(self.changeRoot)

        self.scanUsb()

    def scanUsb(self):

        for i in range(self.fileSystemCombo.model.rowCount()):
            self.fileSystemCombo.model.remove_item(self.fileSystemCombo.currentIndex())

        context = pyudev.Context()

        removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if
                     device.attributes.asstring('removable') == "1"]

        for device in removable:
            partitions = [device.device_node for device in
                          context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]

            # print("All removable partitions: {}".format(", ".join(partitions)))
            # print("Mounted removable partitions:")
            for p in psutil.disk_partitions():
                if p.device in partitions:
                    # print("  {}: {}".format(p.device, p.mountpoint))
                    self.fileSystemCombo.model.append_item(p.mountpoint)

                self.fileSystemCombo.setCurrentIndex(0)

    def changeRoot(self, value):
        new_path = self.fileSystemCombo.itemText(value)
        self.fileSystemTree.model.setRootPath(new_path)
        self.fileSystemTree.setRootIndex(self.fileSystemTree.model.index(new_path))
        