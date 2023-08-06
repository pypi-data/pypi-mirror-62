import pathlib

from flask_admin.contrib import fileadmin
from flask_admin.form import FormOpts

from . import Views
from .MyBaseView import MyBaseView


@Views.register("Files")
def setup(admin):
    section = "webadmin"
    config = admin.app.config["SHARED"].config.config
    webadmin_config_on = config(section, "config_on", 1)
    webadmin_installationrepo_on = config(section, "installationrepo_on", 1)
    auto_update_on = config("auto_update", "on", 0)
    webadmin_tools_on = config(section, "tools_on", 1)

    repo_folder = str(pathlib.Path("./installation_repo").absolute())
    upload_folder = str(pathlib.Path("./config").absolute())

    if webadmin_config_on:
        admin.add_view(Files(upload_folder, name="Config Files"))

    # upgraderepo legges ikke til i hovedmenyen. den skal åpnes fra egen plassering
    repo_exists = repo_folder and pathlib.Path(repo_folder).is_dir()
    if (
        webadmin_installationrepo_on
        and webadmin_tools_on
        and auto_update_on
        and repo_exists
    ):
        repo_view = InstallationRepo(repo_folder, name="Installation Repo")
        admin.app.register_blueprint(repo_view.create_blueprint(admin))
        admin.app.config["MANAGE_REPO"] = 1
    else:
        admin.app.config["MANAGE_REPO"] = 0


class Files(MyBaseView, fileadmin.FileAdmin):
    allowed_extensions = (
        "txt",
        "conf",
        "csv",
        "der",
        "pam",
        "key",
        "zip",
        "gz",
        "7z",
        "py",
        "ini",
        "yaml",
    )
    editable_extensions = ("txt", "conf", "csv", "py", "ini", "yaml")
    can_download = True

    # har overstyrt list_row_actions for å legge til en download-knapp.
    list_template = "admin/filelist.html"
    edit_template = "admin/fileedit.html"

    def get_edit_form(self):
        ef = super().get_edit_form()
        ef.FormOpts = FormOpts
        return ef

    def is_accessible_path(self, path):
        # skjuler alle filer som slutter med .lock
        # brukes for å låse konfiger utenfor webadmin
        return not path.endswith(".lock")

    def is_accessible(self):
        return self.has_role("admin")


class InstallationRepo(MyBaseView, fileadmin.FileAdmin):
    allowed_extensions = ("zip", "whl", "gz")
    can_download = True
    can_rename = (
        False
    )  # man kan laste opp et ugyldig format og rename til gyldig format

    # har overstyrt list_row_actions for å legge til en download-knapp.
    list_template = "admin/filelist.html"

    def is_accessible(self):
        return self.has_role("admin")
