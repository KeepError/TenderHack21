from flask import Blueprint, render_template, redirect, make_response, url_for, flash, request

from web.tools.api_requests import ApiGet


blueprint = Blueprint(
    "users",
    __name__,
)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    # form = RegisterForm()
    # form.username.description = _("Length must be between ") + str(
    #     User.min_username_length) + _(" and ") + str(User.max_username_length)
    # title = _("Sign up")
    # if form.validate_on_submit():
    #     user_data = form.data.copy()
    #     for field in ("password_again", "submit", "csrf_token"):
    #         user_data.pop(field)
    #     response = ApiPost.make_request("register", json=user_data)
    #
    #     if response.status_code == 200:
    #         flash(_("Your account has been created. You are now able to log in."), "success")
    #         return redirect(url_for("users.login"))
    #
    #     error = response.json()["error"]
    #     code = error["code"]
    #
    #     if errors.InvalidRequestError.sub_code_match(code):
    #         fields = error["fields"]
    #         for field in fields:
    #             if field in form:
    #                 form[field].errors += fields[field]
    #     elif errors.UserAlreadyExistsError.sub_code_match(code):
    #         flash(_("User already exists."), "danger")
    #     else:
    #         flash(INTERNAL_ERROR_MSG, "danger")

    message = ""

    if request.method == 'POST':
        inn = request.form.get('inn')

        result = ApiGet.make_request("inn", inn)
        if not result:
            message = "Ошибка"
        else:
            return redirect(f"/lk?inn={inn}")

    return render_template("login.html", title="Log in", message=message)


@blueprint.route("/lk", methods=["GET"])
def lk():
    inn = request.args.get("inn")

    message = ""

    periodicity_res = ApiGet.make_request("predictions", "periodicity", inn)
    if periodicity_res.status_code == 404:
        message = periodicity_res.message
        records = []
    else:
        records = periodicity_res.json()["records"]

    return render_template("lk.html", title="Личный кабинет", records=records, message=message)
