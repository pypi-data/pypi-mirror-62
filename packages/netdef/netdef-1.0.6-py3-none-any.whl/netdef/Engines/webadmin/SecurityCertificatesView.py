import configparser
import functools
import glob

import flask_login
from flask import current_app, flash, request
from flask_admin import expose
from flask_admin.form import FormOpts, rules
from wtforms import (
    Form,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    validators,
)

from .. import utils
from . import Views
from .MyBaseView import MyBaseView


@Views.register("SecurityCertificatesView")
def setup(admin, view=None):
    config = admin.app.config["SHARED"].config.config
    security_certificates_on = config("webadmin", "security_certificates_on", 1)

    if security_certificates_on:
        admin.app.config["tools_panels"]["security_panel_on"] = 1
        admin.app.config["tools_panels"]["security_certificates_on"] = 1

        if not view:
            view = SecurityCertificatesView(
                name="Certificates", endpoint="security_certificates"
            )
        admin.app.register_blueprint(view.create_blueprint(admin))


_pem_cert = utils.default_pem_file
_pem_key = utils.default_key_file
_der_cert = utils.default_der_file
_der_key = utils.default_derkey_file

_form_rules = (
    rules.Header("Certificate"),
    rules.Field("cn"),
    rules.Field("days"),
    rules.Field("pem_cert"),
    rules.Field("pem_key"),
    rules.Field("der_cert"),
    rules.Field("der_key"),
    rules.Field("extend_opcua"),
    rules.Header("Confirmation"),
    rules.Field("current_password"),
    rules.Text("Confirm changes by entering webadmin password"),
)
_widget_args = {"current_password": {"column_class": "col-md-2"}}


class SecurityCertificatesForm(Form):
    form_opts = FormOpts(widget_args=_widget_args, form_rules=_form_rules)

    cn = StringField(
        "Common name",
        validators=[
            validators.Regexp(
                "^[a-zA-Z0-9._-]*$", message="valid chars: a-z, A-Z, 0-9, ._-"
            )
        ],
        render_kw={"placeholder": "Hostname, DNS, IP-address or leave it blank"},
    )
    days = IntegerField("Days valid", default=3650)
    pem_cert = SelectField(
        "PEM cert", default=_pem_cert, choices=[(_pem_cert, _pem_cert)]
    )
    pem_key = SelectField("PEM key", default=_pem_key, choices=[(_pem_key, _pem_key)])
    der_cert = SelectField(
        "DER cert", default=_der_cert, choices=[(_der_cert, _der_cert)]
    )
    der_key = SelectField("DER key", default=_der_key, choices=[(_der_key, _der_key)])

    extend_opcua = SelectField(
        "Add OPCUA extension", default="0", choices=[("0", "Off"), ("1", "On")]
    )

    current_password = PasswordField("Current password")

    @staticmethod
    def validate_current_password(form, field):
        validators.DataRequired()(form, field)
        if not utils.check_user_and_pass(
            current_app, flask_login.current_user.id, field.data
        ):
            raise validators.ValidationError("Invalid password")


class SecurityCertificatesView(MyBaseView):
    @expose("/", methods=["GET", "POST"])
    def index(self):
        conf_ok = utils.can_generate_certs()
        form = SecurityCertificatesForm(request.form)

        if request.method == "POST" and form.validate():
            res = utils.generate_overwrite_certificates(
                _pem_cert,
                _pem_key,
                _der_cert,
                _der_key,
                form.cn.data,
                form.days.data,
                int(form.extend_opcua.data),
            )
            if res:
                flash(res, category="warning")
            else:
                flash("New certs generated successfully", category="success")

        return self.render("security/certificates.html", conf_ok=conf_ok, form=form)

    def is_accessible(self):
        return self.has_role("admin")
