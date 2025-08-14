from flask import Flask, render_template, request, redirect, url_for, flash, session


app = Flask(__name__)

@app.route("/")
def browse():
    # if 'user_id' not in session:
    #     flash("Please log in to access this page.", "warning")
    #     return redirect(url_for('login'))
    return render_template("browse.html")

if __name__ == '__main__':
    app.run(debug=True)
