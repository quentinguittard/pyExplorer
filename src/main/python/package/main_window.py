from functools import partial

from PySide2 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QMainWindow):
    """This is a class to create the main window of the application."""

    def __init__(self, ctx):
        """The constructor of the main window.

        :param ctx: The context of the application.
        :type ctx: ApplicationContext
        """
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("pyExplorer")
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface of the application."""
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.add_actions_to_toolbox()
        self.setup_connections()
        self.create_file_model()

    def create_widgets(self):
        """Create the widgets of the application."""
        self.toolbar = QtWidgets.QToolBar()
        self.tree_view = QtWidgets.QTreeView()
        self.list_view = QtWidgets.QListView()
        self.sld_iconSize = QtWidgets.QSlider()
        self.main_widget = QtWidgets.QWidget()

    def modify_widgets(self):
        """Apply a CSS style sheet to the user interface of the application and modify the style of the widgets."""
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

        self.list_view.setViewMode(QtWidgets.QListView.IconMode)
        self.list_view.setUniformItemSizes(True)
        self.list_view.setIconSize(QtCore.QSize(48, 48))

        self.sld_iconSize.setRange(48, 256)
        self.sld_iconSize.setValue(48)

        self.tree_view.setSortingEnabled(True)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def create_layouts(self):
        """Create the grid layout of the user interface."""
        self.main_layout = QtWidgets.QHBoxLayout(self.main_widget)

    def add_widgets_to_layouts(self):
        """Add created widgets to the user interface layout."""
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.setCentralWidget(self.main_widget)
        self.main_layout.addWidget(self.tree_view)
        self.main_layout.addWidget(self.list_view)
        self.main_layout.addWidget(self.sld_iconSize)

    def add_actions_to_toolbox(self):
        """Add directories shortcuts to the toolbox of the application."""
        locations = ["home", "desktop", "documents", "movies", "pictures", "music"]
        for location in locations:
            icon = self.ctx.get_resource(f"{location}.svg")
            action = self.toolbar.addAction(QtGui.QIcon(icon), location.capitalize())
            action.triggered.connect(partial(self.change_location, location))

    def setup_connections(self):
        """Setup the connections between the widgets and their functions."""
        self.tree_view.clicked.connect(self.treeview_clicked)
        self.list_view.clicked.connect(self.listview_clicked)
        self.list_view.doubleClicked.connect(self.listview_double_clicked)
        self.sld_iconSize.valueChanged.connect(self.change_icon_size)

    def change_icon_size(self, value):
        """Set a custom size to the list view icons.

        :param value: The size of the icon.
        :type value: int
        """
        self.list_view.setIconSize(QtCore.QSize(value, value))

    def change_location(self, location):
        """Update the root directory in the view widgets.

        :param location: The name of the new root directory.
        :type location: str
        """
        path = eval(f"QtCore.QStandardPaths().standardLocations("
                    f"QtCore.QStandardPaths.{location.capitalize()}Location)")
        path = path[0]
        self.tree_view.setRootIndex(self.model.index(path))
        self.list_view.setRootIndex(self.model.index(path))

    def create_file_model(self):
        """Create the file system model."""
        self.model = QtWidgets.QFileSystemModel()
        root_path = QtCore.QDir.rootPath()
        self.model.setRootPath(root_path)
        self.tree_view.setModel(self.model)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(root_path))
        self.tree_view.setRootIndex(self.model.index(root_path))

    def treeview_clicked(self, index):
        """Update root directory of the list view widget on tree view clicked.

        :param index: The new index of the root directory of the list view.
        :type index: int
        """
        if self.model.isDir(index):
            self.list_view.setRootIndex(index)
        else:
            self.list_view.setRootIndex(index.parent())

    def listview_clicked(self, index):
        """Update the selection of the tree view widget on list view clicked.

        :param index: The new index of the selected item of the tree view.
        :type index: int
        """
        self.tree_view.selectionModel().setCurrentIndex(index, QtCore.QItemSelectionModel.ClearAndSelect)

    def listview_double_clicked(self, index):
        """Update root directory of the list view widget on list view double clicked.

        :param index: The new index of the root directory of the list view.
        :type index: int
        """
        self.list_view.setRootIndex(index)

