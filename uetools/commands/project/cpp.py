import json
import os
import shutil
import tempfile
from dataclasses import dataclass

import pkg_resources
from cookiecutter.main import cookiecutter

from uetools.core.arguments import add_arguments
from uetools.core.command import Command, newparser
from uetools.core.conf import find_project


# fmt: off
@dataclass
class Arguments:
    project: str  #: Project name
    no_input: bool = True  #: Disable prompt


# fmt: on


class CPP(Command):
    """Turn a blueprint project into a C++ project

    Attributes
    ----------
    project: str
        Name of the project

    Examples
    --------

    .. code-block:: console

       uecli cpp RTSGame

    """

    name: str = "cpp"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, CPP)
        add_arguments(parser, Arguments)

    @staticmethod
    def execute(args):
        project = find_project(args.project)

        template = pkg_resources.resource_filename(
            __name__, "templates/CPPTemplate/cookiecutter.json"
        )

        template = os.path.dirname(template)

        name = args.project.split(".uproject")
        project_dir = os.path.dirname(project)

        if os.path.exists(os.path.join(project_dir, "Source")):
            raise RuntimeError(
                "Cannot add cpp source file to a project that already has sources"
            )

        # Windows does not like when python holds the file with `with``
        # pylint: disable=consider-using-with
        configfile = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump({"default_context": {"project_name": name[0]}}, configfile)
        configfile.flush()

        assert os.path.exists(template)

        kwargs = dict(
            no_input=args.no_input,
            config_file=configfile.name,
            overwrite_if_exists=True,
            output_dir=os.path.join(project_dir, ".."),
        )

        cookiecutter(
            template,
            **kwargs,
        )

        # Windows have permission issues on reading a temporary files
        configfile.close()
        os.remove(configfile.name)

        print("Please delete itnermediate folder before generating project files")

        # Remove intermediate Folder because it had the previous generated
        # UBT files but they are not necessary anymore and will cause issue later on
        shutil.rmtree(os.path.join(project_dir, "Intermediate"), ignore_errors=True)

        return 0


COMMANDS = CPP
