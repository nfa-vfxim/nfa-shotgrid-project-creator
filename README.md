# The NFA ShotGrid Project Creator
This standalone application is a GUI rewrite of our [ShotGrid Project Creation script](https://github.com/nfa-vfxim/nfa-shotgrid-project-creation). It is a completely custom tool for properly creating ShotGrid projects so they are correctly configured for use in our ShotGrid pipeline. It was designed to simplify several settings, like:
- Setting the right [ShotGrid configuration](https://github.com/nfa-vfxim/nfa-shotgun-configuration) branch based on the year a student is in.
- Validating project names and codes so no duplicates are created.
- Specific Netherlands Filmacademy settings, like whether we are dealing with a fiction or a documentary project.

![project_creator](https://github.com/nfa-vfxim/nfa-shotgrid-project-creator/assets/63094424/bd8e9849-1542-4401-8465-2185456f49e4)

## Installation instructions
This is a highly specific tool for use at our school, so you will have to customize it to suit your needs. Nevertheless, you can use it like this:
- Use a recent version of Python 3, making sure it supports the correct packages.
- Install the following packages: `PySide2`, `shotgun_api3`.
- Create an enviroment variable called `SHOTGRID_API_KEY` and set the value to your ShotGrid API key. The script name associated with the key should be `project_creation_V2`.
- Run the program with `python main.py`. We recommend packaging it as an executable for installation on artist computers.
