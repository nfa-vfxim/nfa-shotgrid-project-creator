"""Model for the NFA ShotGrid Project Creator, written by Mervin van Brakel (2024)"""

from __future__ import annotations

import datetime
import os
import re
from dataclasses import dataclass

from shotgun_api3 import shotgun


@dataclass
class ProjectInformation:
    """Dataclass used for storing all the information we need to create the project."""

    username: str
    project_name: str
    has_production_code: bool
    project_code: str
    has_other_supervisors: bool
    supervisor_list: list[dict]
    render_engine: str
    project_type: str
    project_fps: int


@dataclass
class UserInformation:
    """Dataclass used for storing information about the user who creates the project."""

    sg_username: str
    sg_user_id: str
    student_year: int
    student_graduation_year: int


class ProjectCreatorModel:
    """Model for the ShotGrid Project Creator.

    This model handles all validation and ShotGrid inferfacing."""

    def __init__(self) -> None:
        """Initializes this class and stores the project dataclass."""
        self.project_information = ProjectInformation(
            "", "", True, "", False, [], "All", "Fiction", 25
        )

    def connect_to_shotgrid(self) -> (bool, str):
        """Connects to ShotGrid database. Returns information based on
        whether or not connection was successful.


        Returns:
            Bool: Whether or not connection was successful.
            Str: Error message if connecting was not successful.
        """
        try:
            self.shotgrid_connection = shotgun.Shotgun(
                "https://nfa.shotgunstudio.com",
                script_name="project_creation_V2",
                api_key=os.environ["SHOTGRID_API_KEY"],
            )

            users = self.shotgrid_connection.find("HumanUser", [], ["name"])
            self.usernames = [user["name"] for user in users]

            projects = self.shotgrid_connection.find("Project", [], ["name"])
            self.projects = [project["name"] for project in projects]

            project_codes = self.shotgrid_connection.find(
                "Project", [], ["sg_projectcode"]
            )
            self.project_codes = [
                project_code["sg_projectcode"]
                for project_code in project_codes
            ]

            return True, ""

        except Exception as error:
            return False, str(error)

    def get_shotgrid_user_from_computer_username(self) -> bool:
        """Checks if the username of the computer matches an account name
        in the ShotGrid database. At school this is usually the case.

        Returns:
            bool: Whether or not usernames match.
        """
        username = os.getlogin()
        return self.get_shotgrid_user(username)

    def get_shotgrid_user(self, username: str) -> dict:
        """Tries to find a ShotGrid user in the database. This can be based
        on either the 'name' field or 'login' field.

        Args:
            username: ShotGrid user name or login

        Returns:
            dict: ShotGrid user object with needed info fields.
        """
        fields_to_retrieve = [
            "id",
            "name",
            "sg_lichting",
            "permission_rule_set",
        ]
        name_field_search = [["name", "contains", username]]
        login_field_search = [["login", "is", username]]

        name_search_user_object = self.shotgrid_connection.find_one(
            "HumanUser", name_field_search, fields_to_retrieve
        )

        if name_search_user_object:
            return name_search_user_object

        login_search_user_object = self.shotgrid_connection.find_one(
            "HumanUser", login_field_search, fields_to_retrieve
        )

        if login_search_user_object:
            return login_search_user_object

        return None

    def set_user_information(self, shotgrid_user: dict) -> None:
        """Stores the correct user information in this class.

        Args:
            shotgrid_user: The ShotGrid user we must store information about.
        """
        shotgrid_user_name = shotgrid_user.get("name")
        shotgrid_user_id = shotgrid_user.get("id")

        student_graduation_year = self.get_student_graduation_year(
            shotgrid_user
        )
        student_year = self.get_current_student_year(student_graduation_year)

        self.user_information = UserInformation(
            shotgrid_user_name,
            shotgrid_user_id,
            student_year,
            student_graduation_year,
        )

    @staticmethod
    def get_student_graduation_year(shotgrid_user: dict) -> int:
        """Gets the graduation year of the student. Needed for calculating which
        year they're currently in.

        Args:
            shotgrid_user: ShotGrid user to get graduation year for

        Returns:
            int: Year in which student graduates.
        """
        graduation_year_string = shotgrid_user.get("sg_lichting")
        return int(graduation_year_string[1:])

    @staticmethod
    def get_current_student_year(graduation_year: int) -> int:
        """Gets the year the student is in. This will be 4th, 3rd or 2nd year.
        This is necessary because each year has it's own storage server.

        Args:
            graduation_year: The year in which the student will graduate.

        Returns:
            int: The schoolyear the student is currently in.
        """
        current_time = datetime.datetime.now()
        corrected_time = current_time + datetime.timedelta(days=120)
        current_year = int(corrected_time.strftime("%Y"))
        to_graduation_year = graduation_year - current_year

        student_year = 4 - to_graduation_year

        if student_year > 4:
            student_year = 4

        return student_year

    def validate_project_name(self, project_name: str) -> (bool, str):
        """Validates the project name.

        Args:
            project_name: The string name for the project.

        Returns:
            Bool: Whether or not validation is successful.
            Str: Validation message for display in UI.
        """
        self.project_information.project_name = project_name

        if not project_name:
            return (
                False,
                "You must fill in a project name.",
            )

        legal_characters = "^[a-z_]*$"
        contains_only_legal_characters = re.match(
            legal_characters, project_name
        )

        if not contains_only_legal_characters:
            return (
                False,
                "Project name may only use lowercase a-z and underscores.",
            )

        if project_name in self.projects:
            return (
                False,
                "Project name already taken.",
            )

        return True, "Project name available!"

    def validate_project_code(self, project_code: str) -> (bool, str):
        """Validates the project code.

        Args:
            project_code: The string project code.

        Returns:
            Bool: Whether or not validation is successful.
            Str: Validation message for display in UI.
        """
        self.project_information.project_code = project_code.lower()

        if self.project_information.has_production_code:
            legal_characters = "^[Pp0-9]+$"
            code_length = 6
            legal_character_warning = (
                "Production code should start with a p and contain 5 numbers."
            )
        else:
            legal_characters = "^[A-Za-z]+$"
            code_length = 3
            legal_character_warning = (
                "Three-letter code should only use letters a-z."
            )

        contains_only_legal_characters = re.match(
            legal_characters, project_code
        )

        if not contains_only_legal_characters:
            return False, legal_character_warning

        if len(project_code) != code_length:
            return (
                False,
                f"Project code uses {'more' if len(project_code) > code_length else 'less'} characters than allowed.",
            )

        if project_code.lower() in self.project_codes:
            return (
                False,
                "Project code already taken.",
            )

        return True, "Project code available!"

    def set_has_production_code(self, has_code: bool) -> None:
        """Sets production code bool on the dataclass.

        Args:
            has_code: Wether or not project has production code.
        """
        self.project_information.has_production_code = has_code

    def add_supervisor(self, supervisor_name: str) -> (bool, str, str):
        """Validates the name of a supervisor and adds it to the dataclass.

        Args:
            supervisor_name: The username of the supervisor to add.

        Returns:
            Bool: Whether or not validation is successful.
            Str: Username after validation
            Str: Validation message for display in UI.
        """
        supervisor_user_object = self.get_shotgrid_user(supervisor_name)

        if not supervisor_user_object:
            return (
                False,
                None,
                "Could not find supervisor name in ShotGrid database.",
            )

        if supervisor_user_object in self.project_information.supervisor_list:
            return (
                False,
                None,
                "This supervisor has already been added.",
            )

        self.project_information.supervisor_list.append(supervisor_user_object)
        return (
            True,
            supervisor_user_object.get("name"),
            "Added supervisor to list!",
        )

    def remove_supervisor(self, supervisor_name: str) -> (bool, str):
        """Removes the given supervisor from the dataclass.

        Args:
            supervisor_name: Username of supervisor to remove

        Returns:
            Bool: Whether or not removal is successful.
            Str: Validation message for display in UI.
        """
        supervisor_user_object = self.get_shotgrid_user(supervisor_name)

        if (
            supervisor_user_object
            not in self.project_information.supervisor_list
        ):
            return False, "Can't remove because supervisor isn't on the list."

        self.project_information.supervisor_list.remove(supervisor_user_object)
        return True, "Removed supervisor from list!"

    def set_render_engine(self, render_engine: str) -> None:
        """Sets the render engine on the dataclass.

        Args:
            render_engine: Render engine to use.
        """
        self.project_information.render_engine = render_engine

    def set_project_type(self, project_type: str) -> None:
        """Sets the project type on the dataclass.

        Args:
            project_type: Project type to use. Either fiction or documentary.
        """
        self.project_information.project_type = project_type

    def set_fps(self, fps: int) -> None:
        """Sets the project FPS

        Args:
            fps: FPS to set. Most likely 25, as school requires that.
        """
        self.project_information.project_fps = fps

    def validate_project(self) -> (bool, str):
        """Runs through all validation again and then creates the ShotGrid project.

        Returns:
            Bool: Whether or not project creation was successful.
            Str: Validation message for display in UI.
        """

        project_name_validated, project_name_error = (
            self.validate_project_name(self.project_information.project_name)
        )

        if not project_name_validated:
            return False, project_name_error

        project_code_validated, project_code_error = (
            self.validate_project_code(self.project_information.project_code)
        )

        if not project_code_validated:
            return False, project_code_error

        if not self.project_information.supervisor_list:
            return False, "You haven't yet added any supervisors."

        return True, "Validation passed!"

    def get_formatted_supervisors_list(
        self, supervisors_list: list
    ) -> list[dict]:
        """Reworks the supervisor list into the list format that ShotGrid expects.
        Also adds the correct permissions to the supervisors on the list.

        Args:
            supervisors_list: List of supervisor usernames.

        Returns:
            list[dict]: List of dicts with supervisor ID and type.
        """
        formatted_supervisors_list = []
        for supervisor in supervisors_list:
            formatted_supervisors_list.append(
                {"id": supervisor.get("id"), "type": "HumanUser"}
            )

            self.add_supervisor_permissions_to_user(supervisor)

        return formatted_supervisors_list

    @staticmethod
    def get_pipeline_configuration_string(student_year: int) -> str:
        return f"sgtk:descriptor:git_branch?branch=release/s{student_year}&path=https://github.com/nfa-vfxim/nfa-shotgun-configuration.git"

    def add_supervisor_permissions_to_user(self, shotgrid_user: dict) -> None:
        """Adds the supervisor permission group to the user if they still have artist permissions.

        Args:
            shotgrid_user: ShotGrid user object to update
        """
        user_permission_group = shotgrid_user.get("permission_rule_set").get(
            "name"
        )

        if user_permission_group == "Artist":
            new_permission_configuration = {
                "permission_rule_set": {
                    "id": 190,
                    "name": "Supervisor",
                    "type": "PermissionRuleSet",
                }
            }
            self.shotgrid_connection.update(
                "HumanUser",
                shotgrid_user.get("id"),
                new_permission_configuration,
            )

    def create_project(self) -> (bool, str):
        """Creates the ShotGrid project and adds the pipeline configuration.

        Returns:
            bool: Whether or not creation was successful.
            str: Link to project page or error text.
        """
        try:
            formatted_supervisors_list = self.get_formatted_supervisors_list(
                self.project_information.supervisor_list
            )

            project_data = {
                "name": self.project_information.project_name,
                "tank_name": self.project_information.project_name,
                "sg_projectcode": self.project_information.project_code,
                "users": formatted_supervisors_list,
                "sg_supervisors": formatted_supervisors_list,
                "sg_render_engine": self.project_information.render_engine,
                "sg_type": self.project_information.project_type,
                "sg_lichting": f"L{self.user_information.student_graduation_year}",
                "sg_fps": self.project_information.project_fps,
                "sg_status": "Active",
            }

            created_project = self.shotgrid_connection.create(
                "Project", project_data
            )
            project_id = created_project.get("id")

            pipeline_configuration_data = {
                "code": "Primary",
                "descriptor": self.get_pipeline_configuration_string(
                    self.user_information.student_year
                ),
                "plugin_ids": "basic.*",
                "project": {"id": project_id, "type": "Project"},
                "sg_lichting": f"s{self.user_information.student_year}",
            }
            self.shotgrid_connection.create(
                "PipelineConfiguration", pipeline_configuration_data
            )

            return (
                True,
                f"https://nfa.shotgunstudio.com/page/project_overview?project_id={project_id}",
            )

        except Exception as error:
            return False, str(error)
