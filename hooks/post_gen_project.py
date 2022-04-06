import json
import os
import shutil

from path import Path
cloud = "Azure"
project_slug = "{{cookiecutter.project_slug}}"
project_name = "{{cookiecutter.project_name}}"
environment = "default"
profile = "{{cookiecutter.profile}}"
workspace_dir = "{{cookiecutter.workspace_dir}}"
artifact_location = "{{cookiecutter.artifact_location}}"

PROJECT_FILE_CONTENT = {
    "environments": {
        environment: {
            "profile": profile,
            "workspace_dir": workspace_dir,
            "artifact_location": artifact_location,
        },
        "staging": {
           "profile": "DEFAULT",
           "workspace_dir": workspace_dir,
           "artifact_location": artifact_location,
        },
        "production": {
            "profile": "DEFAULT",
            "workspace_dir": workspace_dir,
            "artifact_location": artifact_location,
        }
    }
}

DEPLOYMENT = {
    "Azure": {
        "staging": {
            "jobs": [
                {
                    "name": "%s" % project_name,
                    "new_cluster": {
                        "spark_version": "7.3.x-cpu-ml-scala2.12",
                        "node_type_id": "Standard_F4s",
                        "num_workers": 2
                    },
                    "libraries": [],
                    "email_notifications": {
                        "on_start": [],
                        "on_success": [],
                        "on_failure": []
                    },
                    "max_retries": 0,
                    "notebook_task": {
                        "notebook_path": "/Repos/Staging/%s/{{cookiecutter.project_slug}}_notebooks/{{cookiecutter.default_notebook}}" % project_name
                    }
                }
            ]
        },
        "production": {
            "jobs": [
                {
                    "name": "%s" % project_name,
                    "new_cluster": {
                        "spark_version": "7.3.x-cpu-ml-scala2.12",
                        "node_type_id": "Standard_F4s",
                        "num_workers": 2
                    },
                    "libraries": [],
                    "email_notifications": {
                        "on_start": [],
                        "on_success": [],
                        "on_failure": []
                    },
                    "max_retries": 0,
                    "notebook_task": {
                        "notebook_path": "/Repos/Staging/%s/{{cookiecutter.project_slug}}_notebooks/{{cookiecutter.default_notebook}}" % project_name
                    }
                }
            ]
        }
    }
}


def replace_vars(file_path: str):
    _path = Path(file_path)
    content = _path.read_text().format(
        project_name=project_name, environment=environment, profile=profile
    )
    _path.write_text(content)


class PostProcessor:
    @staticmethod
    def process():

        deployment = json.dumps(DEPLOYMENT[cloud], indent=4)
        deployment_file = Path("conf/deployment.json")
        if not deployment_file.parent.exists():
            deployment_file.parent.mkdir()
        deployment_file.write_text(deployment)
        project_file = Path(".dbx/project.json")
        if not project_file.parent.exists():
            project_file.parent.mkdir()
        deployment_file.write_text(deployment)
        project_file.write_text(json.dumps(PROJECT_FILE_CONTENT, indent=2))
        Path(".dbx/lock.json").write_text("{}")
        os.system("git init")


if __name__ == "__main__":
    post_processor = PostProcessor()
    post_processor.process()
