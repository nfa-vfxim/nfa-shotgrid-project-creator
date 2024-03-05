"""Controller for the NFA ShotGrid Project Creator, written by Mervin van Brakel (2024)"""

from __future__ import annotations

from model import ProjectCreatorModel, ValidationError
from view import ProjectCreatorView


class ProjectCreatorController:
    """Controller for the ShotGrid Project Creator.

    This controller handles all interactions between the view and the model.
    """

    def __init__(self):
        """Initializes the controller class and creates the view and model."""
        self.view = ProjectCreatorView()
        self.view.show()
        self.view.start_button.clicked.connect(self.connect_to_shotgrid)

        self.model = ProjectCreatorModel()

    def connect_to_shotgrid(self) -> None:
        """Starts the ShotGrid model connection."""
        self.view.start_widget.hide()
        self.view.layout.addWidget(self.view.get_loading_widget())

        self.model.connect_to_shotgrid(
            self.shotgrid_connection_successful,
            self.shotgrid_connection_failed,
        )

    def shotgrid_connection_successful(self) -> None:
        """Runs when model is connected to ShotGrid. Triggers the username search."""
        self.find_username()

    def shotgrid_connection_failed(self, error: str) -> None:
        """Show an error message when the ShotGrid connection failed.

        Args:
            error: Python error message in string format.
        """
        self.view.loading_widget.hide()
        self.view.layout.addWidget(self.view.get_error_widget())
        self.view.error_text.setText(
            f"ShotGrid connection error: {error}. Please contact a pipeline TD if problem persist."
        )

    def find_username(self) -> None:
        """Checks the username with the model. If we can't find a ShotGrid username,
        we show the username selection screen to the user.
        """
        self.view.loading_widget.hide()

        shotgrid_user = self.model.get_shotgrid_user_from_computer_username()

        if shotgrid_user:
            self.model.set_user_information(shotgrid_user)
            self.view.layout.addWidget(
                self.view.get_main_widget(
                    shotgrid_user.get("name"), self.model.usernames
                )
            )
            self.connect_view_functions()

        else:
            self.view.layout.addWidget(
                self.view.get_username_widget(self.model.usernames)
            )
            self.view.continue_button.clicked.connect(self.validate_username)

    def validate_username(self) -> None:
        """Checks if user submitted username is in ShotGrid. Moves on to next
        step if username exists."""
        shotgrid_user = self.model.get_shotgrid_user(
            self.view.username_lineedit.text()
        )

        if not shotgrid_user:
            self.view.username_validation_text.setStyleSheet(
                "color: '#FF3E3E'; font-size: 12px;"
            )
            self.view.username_validation_text.setText(
                "Could not find user in ShotGrid database."
            )
            self.view.username_validation_text.show()

        else:
            self.view.username_widget.hide()
            self.view.layout.addWidget(
                self.view.get_main_widget(
                    shotgrid_user.get("name"), self.model.usernames
                )
            )
            self.connect_view_functions()
            self.model.set_user_information(shotgrid_user)

    def connect_view_functions(self) -> None:
        """Connects all our view buttons and text changes to corresponding
        functions in this controller."""
        self.view.project_name_lineedit.textChanged.connect(
            self.validate_project_name
        )
        self.view.production_code_yes_button.clicked.connect(
            self.set_production_code_yes
        )
        self.view.production_code_no_button.clicked.connect(
            self.set_production_code_no
        )
        self.view.project_code_lineedit.textChanged.connect(
            self.validate_project_code
        )
        self.view.supervisor_add_button.clicked.connect(self.add_supervisor)
        self.view.supervisor_remove_button.clicked.connect(
            self.remove_supervisor
        )
        self.view.render_engine_list.currentTextChanged.connect(
            self.set_render_engine
        )
        self.view.project_type_fiction_button.clicked.connect(
            self.set_project_type_fiction
        )
        self.view.project_type_documentary_button.clicked.connect(
            self.set_project_type_documentary
        )
        self.view.fps_spinbox.valueChanged.connect(self.set_fps)
        self.view.create_project_button.clicked.connect(self.create_project)

    def validate_project_name(self, project_name: str) -> None:
        """Validates project name and updates view.

        Args:
            project_name: Name of project
        """
        project_name_validation_text = self.view.project_name_validation_text

        try:
            self.model.validate_project_name(project_name)
            project_name_validation_text.setText("Project name available!")
            project_name_validation_text.setStyleSheet(
                "color: '#8BFF3E'; font-size: 12px;"
            )

        except ValidationError as validation_message:
            project_name_validation_text.setText(str(validation_message))
            project_name_validation_text.setStyleSheet(
                "color: '#FF3E3E'; font-size: 12px;"
            )

        project_name_validation_text.show()

    def set_production_code_yes(self) -> None:
        """Switches production code to yes and informs the model."""
        self.view.production_code_yes_button.setChecked(True)
        self.view.production_code_no_button.setChecked(False)
        self.model.set_has_production_code(True)
        self.view.production_code_enter_text.setText(
            "Enter the production code below."
        )

        self.validate_project_code(self.view.project_code_lineedit.text())

    def set_production_code_no(self) -> None:
        """Switches production code to no and informs the model."""
        self.view.production_code_no_button.setChecked(True)
        self.view.production_code_yes_button.setChecked(False)
        self.model.set_has_production_code(False)
        self.view.production_code_enter_text.setText(
            "Come up with a three-letter code for your project. (e.g. ABC)"
        )

        self.validate_project_code(self.view.project_code_lineedit.text())

    def validate_project_code(self, project_code: str) -> None:
        """Validates project name and updates view.

        Args:
            project_code: String project code, either P#### or ABC.
        """
        production_code_validation_text = (
            self.view.production_code_validation_text
        )

        try:
            self.model.validate_project_code(project_code)
            production_code_validation_text.setText("Project code available!")
            production_code_validation_text.setStyleSheet(
                "color: '#8BFF3E'; font-size: 12px;"
            )

        except ValidationError as validation_message:
            production_code_validation_text.setText(str(validation_message))
            production_code_validation_text.setStyleSheet(
                "color: '#FF3E3E'; font-size: 12px;"
            )

        production_code_validation_text.show()

    def add_supervisor(self) -> None:
        """Tries to add the supervisor from the LineEdit to the list of supervisors."""
        supervisors_validation_text = self.view.supervisors_validation_text

        try:
            username = self.model.add_supervisor(
                self.view.supervisors_lineedit.text()
            )

            supervisors_validation_text.setText("Added supervisor to list!")
            supervisors_validation_text.setStyleSheet(
                "color: '#8BFF3E'; font-size: 12px;"
            )

            self.view.supervisors_list.insertItem(0, username)
            self.view.supervisors_list.setCurrentIndex(0)
            self.view.supervisors_lineedit.setText("")

        except ValidationError as validation_message:
            supervisors_validation_text.setText(str(validation_message))
            supervisors_validation_text.setStyleSheet(
                "color: '#FF3E3E'; font-size: 12px;"
            )

        supervisors_validation_text.show()

    def remove_supervisor(self) -> None:
        """Tries to remove a supervisor from the list."""
        supervisors_validation_text = self.view.supervisors_validation_text

        try:
            self.model.remove_supervisor(
                self.view.supervisors_list.currentText()
            )

            self.view.supervisors_list.removeItem(
                self.view.supervisors_list.findText(
                    self.view.supervisors_list.currentText()
                )
            )

            supervisors_validation_text.setText(
                "Removed supervisor from list!"
            )
            supervisors_validation_text.setStyleSheet(
                "color: '#8BFF3E'; font-size: 12px;"
            )

        except ValidationError as validation_message:
            supervisors_validation_text.setText(str(validation_message))
            supervisors_validation_text.setStyleSheet(
                "color: '#FF3E3E'; font-size: 12px;"
            )

        supervisors_validation_text.show()

    def set_render_engine(self, render_engine: str) -> None:
        """Informs the model of the new render engine choice."""
        self.model.set_render_engine(render_engine)

    def set_project_type_fiction(self) -> None:
        """Sets the project type to fiction and informs the model."""
        self.view.project_type_fiction_button.setChecked(True)
        self.view.project_type_documentary_button.setChecked(False)
        self.model.set_project_type("Fiction")

    def set_project_type_documentary(self) -> None:
        """Sets the project type to documentary and informs the model."""
        self.view.project_type_documentary_button.setChecked(True)
        self.view.project_type_fiction_button.setChecked(False)
        self.model.set_project_type("Documentary")

    def set_fps(self, fps: int) -> None:
        """Informs the model of the new FPS.

        Args:
            fps: New project FPS"""
        self.model.set_fps(fps)

    def create_project(self) -> None:
        """Validates the project, then starts project creation on a separate thread."""
        try:
            self.model.validate_project()

        except ValidationError as validation_message:
            self.view.project_validation_text.setText(str(validation_message))
            self.view.project_validation_text.setStyleSheet(
                "color: '#FF3E3E'; font-size: 12px;"
            )
            self.view.project_validation_text.show()
            return

        self.view.main_widget.hide()
        self.view.loading_text.setText("Creating project...")
        self.view.loading_widget.show()

        self.model.start_project_creation(
            self.project_creation_successful, self.project_creation_failed
        )

    def project_creation_successful(self, project_url: str) -> None:
        """Runs when project creation has successfully finished.

        Args:
            project_url: Link to ShotGrid site for project.
        """
        self.view.loading_widget.hide()

        self.view.layout.addWidget(
            self.view.get_project_creation_successful_widget(project_url)
        )

    def project_creation_failed(self, error: str) -> None:
        """Runs when project creation has failed.

        Args:
            error: Python error message in string format.
        """
        self.view.loading_widget.hide()
        self.view.layout.addWidget(self.view.get_error_widget())
        self.view.error_text.setText(
            f"Project creation error: {error}. Please contact a pipeline TD if problem persist."
        )
