from flask import Blueprint, redirect, render_template, request

from app.db.mysql import get_connection

main = Blueprint("main", __name__)


@main.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", users=users)


@main.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]
    email = request.form["email"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/")


@main.route("/delete/<int:user_id>")
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/")


@main.route("/update/<int:user_id>", methods=["POST"])
def update_user(user_id):
    name = request.form["name"]
    email = request.form["email"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/")
