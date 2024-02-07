"""View for the NFA ShotGrid Project Creator, written by Mervin van Brakel (2024)"""

from pathlib import Path

from PySide2 import QtCore, QtGui, QtSvg, QtWidgets

from controller import ProjectCreatorController

SCRIPT_LOCATION = Path(__file__).parent


class ProjectCreatorView(QtWidgets.QWidget):
    """View for the ShotGrid Project Creator.

    This view has all functions related to the Qt UI.
    It also creates the controller."""

    def __init__(self):
        """Initializes the view class and creates the controller."""
        super().__init__()

        self.controller = ProjectCreatorController(self)
        self.setup_ui()

    def setup_ui(self) -> None:
        """Creates the UI of the window."""
        stylesheet_path = SCRIPT_LOCATION / "styles.qss"
        with Path.open(stylesheet_path) as stylesheet_file:
            self.setStyleSheet(stylesheet_file.read())

        icon_path = str(
            SCRIPT_LOCATION / "ui_files" / "project_creator_logo.png"
        )
        window_icon = QtGui.QIcon(icon_path)
        self.setWindowIcon(window_icon)

        self.setWindowTitle("NFA ShotGrid Project Creator")
        self.resize(500, 800)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setMargin(0)

        self.layout.addWidget(self.get_top_widget())
        self.layout.addWidget(self.get_start_widget())

    @staticmethod
    def get_top_widget() -> QtWidgets.QWidget:
        """Gets the top widget of the layout.
        This widget contains the section at the top with the logos.

        Returns:
            QtWidgets.QWidget: Widget containing top section
        """
        top_widget = QtWidgets.QWidget()
        top_widget.setFixedHeight(80)
        top_widget.setStyleSheet("background-color: #2D2D2D")

        top_layout = QtWidgets.QHBoxLayout()

        nfa_logo = QtGui.QPixmap(
            str(SCRIPT_LOCATION / "ui_files" / "nfa_logo.png")
        ).scaledToHeight(35, QtCore.Qt.SmoothTransformation)
        nfa_logo_label = QtWidgets.QLabel()
        nfa_logo_label.setPixmap(nfa_logo)

        shotgrid_creator_label = QtWidgets.QLabel(
            "NFA ShotGrid<br>Project Creator"
        )
        shotgrid_creator_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )

        shotgrid_logo = QtGui.QPixmap(
            str(SCRIPT_LOCATION / "ui_files" / "project_creator_logo.png")
        ).scaledToHeight(40, QtCore.Qt.SmoothTransformation)
        shotgrid_logo_label = QtWidgets.QLabel()
        shotgrid_logo_label.setPixmap(shotgrid_logo)

        top_layout.addWidget(nfa_logo_label)
        top_layout.addStretch()
        top_layout.addWidget(shotgrid_creator_label)
        top_layout.addWidget(shotgrid_logo_label)

        top_widget.setLayout(top_layout)

        return top_widget

    def get_start_widget(self) -> QtWidgets.QWidget:
        """Gets the start widget for the layout.
        This widgets contains all other widgets for the start menu.

        Returns:
            QtWidgets.QWidget: Widget containing start widgets.
        """
        self.start_widget = QtWidgets.QWidget()
        start_widget_layout = QtWidgets.QVBoxLayout()
        start_widget_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.start_widget.setLayout(start_widget_layout)

        start_text_1 = QtWidgets.QLabel(
            "Welcome to the NFA ShotGrid project creator!"
        )
        start_text_1.setAlignment(QtCore.Qt.AlignCenter)
        start_text_1.setWordWrap(True)
        start_widget_layout.addWidget(start_text_1)

        start_text_2 = QtWidgets.QLabel(
            "This tool is for properly creating a ShotGrid project according to our pipeline specifications."
        )
        start_text_2.setAlignment(QtCore.Qt.AlignCenter)
        start_text_2.setWordWrap(True)
        start_widget_layout.addWidget(start_text_2)

        start_text_3 = QtWidgets.QLabel("Press the start button to begin.")
        start_text_3.setAlignment(QtCore.Qt.AlignCenter)
        start_text_3.setWordWrap(True)
        start_widget_layout.addWidget(start_text_3)

        start_button = QtWidgets.QPushButton("Start")
        start_button.clicked.connect(self.controller.connect_to_shotgrid)
        start_button.setMaximumWidth(500)
        start_button.setStyleSheet("margin-bottom: 30px;")
        start_widget_layout.addWidget(start_button, 0)

        return self.start_widget

    def get_username_widget(self, username_list: list) -> QtWidgets.QWidget:
        """Gets the username widget for the layout.
        This widgets contains all other widgets for when we need user input for the username.

        Returns:
            QtWidgets.QWidget: Widget containing username widgets.
        """
        self.username_widget = QtWidgets.QWidget()
        username_widget_layout = QtWidgets.QVBoxLayout()
        username_widget_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.username_widget.setLayout(username_widget_layout)

        validation_error_text = QtWidgets.QLabel(
            "We were unable to automatically find your ShotGrid username."
        )
        username_widget_layout.addWidget(
            validation_error_text, 0, QtCore.Qt.AlignCenter
        )

        validation_error_text2 = QtWidgets.QLabel(
            "Please enter your ShotGrid username below to get started."
        )
        username_widget_layout.addWidget(
            validation_error_text2, 0, QtCore.Qt.AlignCenter
        )

        self.username_lineedit = QtWidgets.QLineEdit()
        self.username_lineedit.setMinimumWidth(300)
        self.username_completer = QtWidgets.QCompleter(username_list)
        self.username_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.username_lineedit.setCompleter(self.username_completer)
        username_widget_layout.addWidget(
            self.username_lineedit, 0, QtCore.Qt.AlignCenter
        )

        self.username_validation_text = QtWidgets.QLabel("")
        self.username_validation_text.hide()
        username_widget_layout.addWidget(
            self.username_validation_text, 0, QtCore.Qt.AlignCenter
        )

        continue_button = QtWidgets.QPushButton("Continue")
        continue_button.setMinimumWidth(300)
        continue_button.clicked.connect(self.controller.validate_username)
        username_widget_layout.addWidget(
            continue_button, 0, QtCore.Qt.AlignCenter
        )

        return self.username_widget

    def get_loading_widget(self) -> QtWidgets.QWidget:
        """Gets the loading widget for the layout.
        This widgets contains all other widgets for when loading.

        Returns:
            QtWidgets.QWidget: Widget containing loading widgets.
        """
        self.loading_widget = QtWidgets.QWidget()
        loading_widget_layout = QtWidgets.QVBoxLayout()
        loading_widget_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.loading_widget.setLayout(loading_widget_layout)

        loading_spinner = QtSvg.QSvgWidget(
            str(SCRIPT_LOCATION / "ui_files" / "loading_spinner.svg")
        )
        loading_spinner.setFixedSize(100, 100)
        loading_widget_layout.addWidget(
            loading_spinner, 0, QtCore.Qt.AlignHCenter
        )

        self.loading_text = QtWidgets.QLabel("Connecting to ShotGrid...")
        self.loading_text.setStyleSheet(
            "margin-top: 6px; margin-bottom: 30px;"
        )
        loading_widget_layout.addWidget(self.loading_text)

        return self.loading_widget

    def get_error_widget(self) -> QtWidgets.QWidget:
        """Gets the error widget for the layout.
        This widgets contains all other widgets for when an error occurs.

        Returns:
            QtWidgets.QWidget: Widgets containing error widgets.
        """
        self.error_widget = QtWidgets.QWidget()
        error_widget_layout = QtWidgets.QVBoxLayout()
        error_widget_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.error_widget.setLayout(error_widget_layout)

        error_icon = QtSvg.QSvgWidget(
            str(SCRIPT_LOCATION / "ui_files" / "error.svg")
        )
        error_icon.setFixedSize(60, 60)
        error_widget_layout.addWidget(error_icon, 0, QtCore.Qt.AlignHCenter)

        self.error_text = QtWidgets.QLabel("")
        self.error_text.setAlignment(QtCore.Qt.AlignCenter)
        self.error_text.setWordWrap(True)
        self.error_text.setStyleSheet("margin-top: 6px; margin-bottom: 30px;")
        error_widget_layout.addWidget(
            self.error_text, 0, QtCore.Qt.AlignHCenter
        )

        return self.error_widget

    def get_main_widget(
        self, username: str, usernames_list: list
    ) -> QtWidgets.QWidget:
        """Gets the main widget of the layout.
        This widgets contains all other widgets for user input.

        Returns:
            QtWidgets.QWidget: Widget containing the main widgets.
        """
        self.main_widget = QtWidgets.QWidget()
        main_widget_layout = QtWidgets.QVBoxLayout()
        main_widget_layout.setMargin(15)
        self.main_widget.setLayout(main_widget_layout)

        main_widget_layout.addWidget(self.get_welcome_widget(username))
        main_widget_layout.addWidget(self.get_project_name_widget())
        main_widget_layout.addWidget(self.get_production_code_widget())
        main_widget_layout.addWidget(
            self.get_supervisors_widget(usernames_list)
        )
        main_widget_layout.addWidget(self.get_render_engine_widget())
        main_widget_layout.addWidget(self.get_project_type_widget())
        main_widget_layout.addWidget(self.get_fps_widget())
        main_widget_layout.addWidget(self.get_create_project_widget())

        return self.main_widget

    def get_welcome_widget(self, username: str) -> QtWidgets.QLabel:
        """Gets the welcome section widget for our main layout.

        Returns:
            QtWidgets.QLabel: Widget containing welcome text
        """
        welcome_text = f"""Welcome, {username}! Fill out the following form and press
    the create button to create your new ShotGrid project."""
        self.welcome_text_widget = QtWidgets.QLabel(welcome_text)
        self.welcome_text_widget.setAlignment(QtCore.Qt.AlignHCenter)

        return self.welcome_text_widget

    def get_project_name_widget(self) -> QtWidgets.QWidget:
        """Gets the project name widget for the main layout."

        Returns:
            QtWidgets.QWidget: Widget containing project name widgets.
        """
        project_name_widget = QtWidgets.QWidget()
        project_name_widget_layout = QtWidgets.QVBoxLayout()
        project_name_widget.setLayout(project_name_widget_layout)

        project_name_text = QtWidgets.QLabel("What is your project name?")
        project_name_widget_layout.addWidget(project_name_text)

        project_name_lineedit = QtWidgets.QLineEdit("")
        project_name_lineedit.textChanged.connect(
            self.controller.validate_project_name
        )
        project_name_widget_layout.addWidget(project_name_lineedit)

        self.project_name_validation_text = QtWidgets.QLabel("")
        self.project_name_validation_text.hide()
        project_name_widget_layout.addWidget(self.project_name_validation_text)

        return project_name_widget

    def get_production_code_widget(self) -> QtWidgets.QWidget:
        """Gets the production code widget for the main layout.

        Returns:
            QtWidgets.QWidget: Widget containing production code widgets.
        """
        production_code_widget = QtWidgets.QWidget()
        production_code_widget_layout = QtWidgets.QVBoxLayout()
        production_code_widget.setLayout(production_code_widget_layout)

        production_code_widget_layout.addWidget(
            QtWidgets.QLabel(
                "Does your project have a production code? (e.g. P22412)"
            )
        )
        horizontal_button_box_widget = QtWidgets.QWidget()
        horizontal_button_box_layout = QtWidgets.QHBoxLayout()
        horizontal_button_box_layout.setContentsMargins(0, 0, 0, 16)
        horizontal_button_box_widget.setLayout(horizontal_button_box_layout)

        self.production_code_yes_button = QtWidgets.QPushButton("Yes")
        self.production_code_yes_button.setCheckable(True)
        self.production_code_yes_button.setChecked(True)
        self.production_code_yes_button.clicked.connect(
            self.controller.set_production_code_yes
        )
        horizontal_button_box_layout.addWidget(
            self.production_code_yes_button, 0, QtCore.Qt.AlignLeft
        )

        self.production_code_no_button = QtWidgets.QPushButton("No")
        self.production_code_no_button.setCheckable(True)
        self.production_code_no_button.clicked.connect(
            self.controller.set_production_code_no
        )
        horizontal_button_box_layout.addWidget(
            self.production_code_no_button, 0, QtCore.Qt.AlignLeft
        )

        horizontal_button_box_layout.addStretch(1)
        production_code_widget_layout.addWidget(horizontal_button_box_widget)

        self.production_code_enter_text = QtWidgets.QLabel(
            "Enter the production code below.",
        )
        production_code_widget_layout.addWidget(
            self.production_code_enter_text
        )

        self.project_code_lineedit = QtWidgets.QLineEdit("")
        self.project_code_lineedit.textChanged.connect(
            self.controller.validate_project_code
        )
        production_code_widget_layout.addWidget(self.project_code_lineedit)

        self.production_code_validation_text = QtWidgets.QLabel("")
        self.production_code_validation_text.hide()
        production_code_widget_layout.addWidget(
            self.production_code_validation_text
        )

        return production_code_widget

    def get_supervisors_widget(
        self, usernames_list: list
    ) -> QtWidgets.QWidget:
        """Gets the supervisors widget for the main layout.

        Returns:
            QtWidgets.QWidget: Widget containing supervisors widgets.
        """

        supervisors_widget = QtWidgets.QWidget()
        supervisors_widget_layout = QtWidgets.QVBoxLayout()
        supervisors_widget.setLayout(supervisors_widget_layout)

        supervisors_widget_layout.addWidget(
            QtWidgets.QLabel("Add all project supervisors to this list.")
        )

        supervisors_adding_widget = QtWidgets.QWidget()
        supervisors_adding_widget_layout = QtWidgets.QHBoxLayout()
        supervisors_adding_widget_layout.setMargin(0)
        supervisors_adding_widget.setLayout(supervisors_adding_widget_layout)

        self.supervisors_lineedit = QtWidgets.QLineEdit()
        supervisors_adding_widget_layout.addWidget(self.supervisors_lineedit)

        self.supervisor_completer = QtWidgets.QCompleter(usernames_list)
        self.supervisor_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.supervisors_lineedit.setCompleter(self.supervisor_completer)

        supervisor_add_button = QtWidgets.QPushButton("+")
        supervisor_add_button.clicked.connect(self.controller.add_supervisor)
        supervisors_adding_widget_layout.addWidget(supervisor_add_button)

        supervisors_widget_layout.addWidget(supervisors_adding_widget)

        self.supervisors_validation_text = QtWidgets.QLabel("")
        self.supervisors_validation_text.hide()
        supervisors_widget_layout.addWidget(self.supervisors_validation_text)

        supervisor_list_widget = QtWidgets.QWidget()
        supervisor_list_layout = QtWidgets.QHBoxLayout()
        supervisor_list_layout.setMargin(0)
        supervisor_list_widget.setLayout(supervisor_list_layout)

        self.supervisors_list = QtWidgets.QComboBox()
        supervisor_list_layout.addWidget(self.supervisors_list, 1)

        supervisor_remove_button = QtWidgets.QPushButton("-")
        supervisor_remove_button.clicked.connect(
            self.controller.remove_supervisor
        )
        supervisor_list_layout.addWidget(supervisor_remove_button, 0)

        supervisors_widget_layout.addWidget(supervisor_list_widget)

        return supervisors_widget

    def get_render_engine_widget(self) -> QtWidgets.QWidget:
        """Gets the render engine widget for the main layout.

        Returns:
            QtWidgets.QWidget: Widget containing render engine widgets.
        """
        render_engine_widget = QtWidgets.QWidget()
        render_engine_widget_layout = QtWidgets.QVBoxLayout()
        render_engine_widget.setLayout(render_engine_widget_layout)

        render_engine_widget_layout.addWidget(
            QtWidgets.QLabel("What render engine are you using?")
        )

        render_engine_list = QtWidgets.QComboBox()
        render_engine_list.currentTextChanged.connect(
            self.controller.set_render_engine
        )
        render_engine_list.setMaximumWidth(100)
        render_engine_list.addItem("All")
        render_engine_list.addItem("Arnold")
        render_engine_list.addItem("Karma")
        render_engine_list.addItem("RenderMan")

        render_engine_widget_layout.addWidget(render_engine_list)
        return render_engine_widget

    def get_project_type_widget(self) -> QtWidgets.QWidget:
        """Gets the project type widget for the main layout.

        Returns:
            QtWidgets.QWidget: Widget containing project type widgets.
        """
        project_type_widget = QtWidgets.QWidget()
        project_type_widget_layout = QtWidgets.QVBoxLayout()
        project_type_widget.setLayout(project_type_widget_layout)

        project_type_widget_layout.addWidget(
            QtWidgets.QLabel("Is this a fiction or documentary project?")
        )

        horizontal_button_box_widget = QtWidgets.QWidget()
        horizontal_button_box_layout = QtWidgets.QHBoxLayout()
        horizontal_button_box_layout.setMargin(0)
        horizontal_button_box_widget.setLayout(horizontal_button_box_layout)

        self.project_type_fiction_button = QtWidgets.QPushButton("Fiction")
        self.project_type_fiction_button.clicked.connect(
            self.controller.set_project_type_fiction
        )
        self.project_type_fiction_button.setCheckable(True)
        self.project_type_fiction_button.setChecked(True)
        horizontal_button_box_layout.addWidget(
            self.project_type_fiction_button, 0, QtCore.Qt.AlignLeft
        )

        self.project_type_documentary_button = QtWidgets.QPushButton(
            "Documentary"
        )
        self.project_type_documentary_button.clicked.connect(
            self.controller.set_project_type_documentary
        )
        self.project_type_documentary_button.setCheckable(True)
        horizontal_button_box_layout.addWidget(
            self.project_type_documentary_button, 0, QtCore.Qt.AlignLeft
        )

        horizontal_button_box_layout.addStretch(1)
        project_type_widget_layout.addWidget(horizontal_button_box_widget)

        return project_type_widget

    def get_fps_widget(self) -> QtWidgets.QWidget:
        """Gets the fps widget for the main layout.

        Returns:
            QtWidgets.QWidget: Widget containing fps widgets.
        """
        fps_widget = QtWidgets.QWidget()
        fps_widget_layout = QtWidgets.QVBoxLayout()
        fps_widget.setLayout(fps_widget_layout)

        fps_widget_layout.addWidget(
            QtWidgets.QLabel("What is the FPS for the project?")
        )

        fps_spinbox = QtWidgets.QSpinBox()
        fps_spinbox.valueChanged.connect(self.controller.set_fps)
        fps_spinbox.setMaximumWidth(60)
        fps_spinbox.setValue(25)
        fps_spinbox.setRange(1, 120)
        fps_widget_layout.addWidget(fps_spinbox)

        return fps_widget

    def get_create_project_widget(self) -> QtWidgets.QWidget:
        """Gets the create project widget for the main layout.

        Returns:
            QtWidgets.QWidget: Widget with create project button
        """
        create_project_widget = QtWidgets.QWidget()
        create_project_widget_layout = QtWidgets.QVBoxLayout()
        create_project_widget_layout.setAlignment(QtCore.Qt.AlignHCenter)
        create_project_widget.setLayout(create_project_widget_layout)

        create_project_button = QtWidgets.QPushButton("Create project")
        create_project_button.clicked.connect(self.controller.create_project)
        create_project_button.setMaximumWidth(150)
        create_project_widget_layout.addWidget(
            create_project_button, 0, QtCore.Qt.AlignHCenter
        )

        self.project_validation_text = QtWidgets.QLabel("")
        self.project_validation_text.hide()
        create_project_widget_layout.addWidget(
            self.project_validation_text, 0, QtCore.Qt.AlignHCenter
        )

        return create_project_widget

    def get_project_creation_successful_widget(
        self, project_link: str
    ) -> QtWidgets.QWidget:
        """_summary_

        Args:
            project_link (str): _description_

        Returns:
            QtWidgets.QWidget: _description_
        """
        successful_widget = QtWidgets.QWidget()
        successful_widget_layout = QtWidgets.QVBoxLayout()
        successful_widget_layout.setAlignment(QtCore.Qt.AlignCenter)
        successful_widget.setLayout(successful_widget_layout)

        success_icon = QtSvg.QSvgWidget(
            str(SCRIPT_LOCATION / "ui_files" / "success.svg")
        )
        success_icon.setFixedSize(100, 100)
        successful_widget_layout.addWidget(
            success_icon, 0, QtCore.Qt.AlignHCenter
        )

        success_text = QtWidgets.QLabel("ShotGrid project created!")
        success_text.setAlignment(QtCore.Qt.AlignCenter)
        success_text.setStyleSheet("margin-top: 6px")
        successful_widget_layout.addWidget(
            success_text, 0, QtCore.Qt.AlignHCenter
        )

        project_link = QtWidgets.QLabel(
            f"<a href='{project_link}' style='color: #37A5CC; text-decoration: none;'>Click here to open the project in your browser.</a>"
        )
        project_link.setAlignment(QtCore.Qt.AlignCenter)
        project_link.setOpenExternalLinks(True)
        project_link.setWordWrap(True)
        project_link.setMinimumWidth(200)
        project_link.setStyleSheet("margin-top: 1px; margin-bottom: 30px;")
        successful_widget_layout.addWidget(
            project_link, 0, QtCore.Qt.AlignHCenter
        )

        return successful_widget
