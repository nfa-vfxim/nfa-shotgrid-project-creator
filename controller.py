"""Controller for the NFA ShotGrid Project Creator, written by Mervin van Brakel (2024)"""

from __future__ import annotations

from PySide2 import QtCore

from model import ProjectCreatorModel


class ProjectCreatorController:
    """Controller for the ShotGrid Project Creator.

    This controller handles all interactions between the view and the model.
    It also creates the model.

    Attributes:
        view: The ProjectCreatorView class."""

    def __init__(self, view):
        """Initializes the controller class and creates the model."""
        self.view = view
        self.model = ProjectCreatorModel()

    def connect_to_shotgrid(self) -> None:
        """Starts the ShotGrid model connection on a seperate thread."""
        self.view.start_widget.hide()
        self.view.layout.addWidget(self.view.get_loading_widget())

        self.shotgrid_connection_thread = ShotGridConnectionThread(self.model)
        self.shotgrid_connection_thread.connection_response_received.connect(
            self.connection_response_received
        )
        self.shotgrid_connection_thread.start()

    def connection_response_received(
        self, connection_information: tuple(bool, str)
    ) -> None:
        """Runs when the ShotGrid connection thread is finished.
        Shows error if needed, else moves on to finding the username.

        Args:
            connection_information: ShotGrid connection information
        """
        connected, error = connection_information

        if connected:
            self.find_username()
        else:
            self.view.loading_widget.hide()
            self.view.layout.addWidget(self.view.get_error_widget())
            self.view.error_text.setText(
                f"Error: {error}. Please contact a pipeliner if problem persist."
            )

    def find_username(self) -> None:
        """Checks the username with the model. If we can't find a ShotGrid username,
        we show the username selection sceen to the user.
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
        else:
            self.view.layout.addWidget(
                self.view.get_username_widget(self.model.usernames)
            )

    def validate_username(self) -> None:
        """Checks if user submitted username is in ShotGrid. Moves on to next
        step if username is correct."""
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
            self.model.set_user_information(shotgrid_user)

    def validate_project_name(self, project_name: str) -> None:
        """Validates project name and updates view."""
        validated, message = self.model.validate_project_name(project_name)
        project_name_validation_text = self.view.project_name_validation_text

        project_name_validation_text.setText(message)
        project_name_validation_text.setStyleSheet(
            f"color: {'#8BFF3E' if validated else '#FF3E3E'}; font-size: 12px;"
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
        validated, message = self.model.validate_project_code(project_code)
        production_code_validation_text = (
            self.view.production_code_validation_text
        )

        production_code_validation_text.setText(message)
        production_code_validation_text.setStyleSheet(
            f"color: {'#8BFF3E' if validated else '#FF3E3E'}; font-size: 12px;"
        )
        production_code_validation_text.show()

    def add_supervisor(self) -> None:
        """Tries to add the supervisor from the LineEdit to the list of supervisors."""
        validated, username, message = self.model.add_supervisor(
            self.view.supervisors_lineedit.text()
        )
        supervisors_validation_text = self.view.supervisors_validation_text

        if validated:
            self.view.supervisors_list.insertItem(0, username)
            self.view.supervisors_list.setCurrentIndex(0)
            self.view.supervisors_lineedit.setText("")

        supervisors_validation_text.setText(message)
        supervisors_validation_text.setStyleSheet(
            f"color: {'#8BFF3E' if validated else '#FF3E3E'}; font-size: 12px;"
        )
        supervisors_validation_text.show()

    def remove_supervisor(self) -> None:
        """Tries to remove a supervisor from the list."""
        removed, message = self.model.remove_supervisor(
            self.view.supervisors_list.currentText()
        )
        supervisors_validation_text = self.view.supervisors_validation_text

        if removed:
            self.view.supervisors_list.removeItem(
                self.view.supervisors_list.findText(
                    self.view.supervisors_list.currentText()
                )
            )

        supervisors_validation_text.setText(message)
        supervisors_validation_text.setStyleSheet(
            f"color: {'#8BFF3E' if removed else '#FF3E3E'}; font-size: 12px;"
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
        """Informs the model of the new FPS."""
        self.model.set_fps(fps)

    def create_project(self) -> None:
        """Validates, then creates the project."""
        validated, message = self.model.validate_project()

        if not validated:
            self.view.project_validation_text.setText(message)
            self.view.project_validation_text.setStyleSheet(
                "color: '#FF3E3E'; font-size: 12px;"
            )
            self.view.project_validation_text.show()
            return

        self.view.main_widget.hide()
        self.view.loading_text.setText("Creating project...")
        self.view.loading_widget.show()

        self.project_creation_thread = ProjectCreationThread(self.model)
        self.project_creation_thread.project_creation_finished.connect(
            self.project_creation_finished
        )
        self.project_creation_thread.start()

    def project_creation_finished(self, project_information: tuple) -> None:
        """Runs when project creation is finished on the seperate thread.

        Args:
            project_information: Whether or not creation was successful and error/link
        """
        created, message = project_information
        self.view.loading_widget.hide()

        if not created:
            self.view.main_widget.hide()
            self.view.layout.addWidget(self.view.get_error_widget())
            self.view.error_text.setText(
                f"Error: {message}. Please contact a pipeliner if problem persist."
            )
            return

        self.view.layout.addWidget(
            self.view.get_project_creation_successful_widget(message)
        )


class ShotGridConnectionThread(QtCore.QThread):
    """Class for connecting to ShotGrid on a seperate thread
    so the UI doesn't freeze."""

    connection_response_received = QtCore.Signal(object)

    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        connection_information = self.model.connect_to_shotgrid()
        self.connection_response_received.emit(connection_information)


class ProjectCreationThread(QtCore.QThread):
    """Class for creating the ShotGrid project on a seperate thread
    so the UI doesn't freeze."""

    project_creation_finished = QtCore.Signal(object)

    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        created_project_information = self.model.create_project()
        self.project_creation_finished.emit(created_project_information)
