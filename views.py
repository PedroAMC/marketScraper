from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from skin_requests import get_skins_bs4
from threading import Timer



views = Blueprint(__name__, "views")

PASSWORD = "aiaiomano"
authenticated = False

weapons = ["AK-47", "AWP", "M4A4", "M4A1-S", "USP-S", "Glock-18", "Desert Eagle", "MP9", "MAC-10", "P250"]
conditions = ["Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred"]

@views.route("/")
def home():
    global authenticated
    if not authenticated:
        return redirect(url_for("views.login"))

    return render_template("index.html", weapons=weapons, conditions=conditions)


@views.route("/login", methods=["GET", "POST"])
def login():
    global authenticated
    authenticated = False
    if authenticated:
        return redirect(url_for("views.home"))

    if request.method == "POST":
        password = request.form.get("password")
        if password == PASSWORD:
            authenticated = True
            return redirect(url_for("views.home"))
        else:
            return render_template("login.html", error="Invalid password")

    return render_template("login.html", error=None)

@views.route("/weapon", methods=["GET"])
def weapon():
    weapon_name = request.args.get("weapon")
    condition = request.args.get("condition")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    skins = get_skins_bs4(weapon_name, condition, min_price, max_price)
    sortedSkins = sorted(skins, key=lambda x: x.profitPercentage, reverse=True)
    sortedSkins = [skin for skin in sortedSkins if skin.profitPercentage <= 55]
    sortedSkins = sortedSkins[:10]

    if not sortedSkins:
        # Skins list is empty, return an appropriate response or redirect
        error_message = "No skins available or search limit reached"

        return render_template("index.html", weapons=weapons, conditions=conditions, error=error_message)

    return render_template("weapon.html", weapon_name=weapon_name, condition=condition, min_price=min_price, max_price=max_price, skins=sortedSkins)


