from flask import Flask, render_template, request, redirect, url_for, flash, session
from surveys import satisfaction_survey, personality_quiz, surveys, Question, Survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = '05/01/23_surveys'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug_toolbar = DebugToolbarExtension(app)

responses = []

@app.route("/")
def start_page():
    survey = surveys["satisfaction"]  # Change to the desired survey
    return render_template("start.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_survey():
    session["responses"] = []
    return redirect(url_for("question", question_number=0))

@app.route("/questions/<int:question_number>")
def question(question_number):
    responses = session.get("responses")
    
    if len(responses) == len(surveys["satisfaction"].questions):
        return redirect(url_for("complete"))
    elif question_number != len(responses):
        flash("You are trying to access an invalid question. Redirecting you to the correct question.")
        return redirect(url_for("question", question_number=len(responses)))
    else:
        question = surveys["satisfaction"].questions[question_number]
        return render_template("question.html", question=question, question_number=question_number)

@app.route("/answer", methods=["POST"])
def answer():
    choice = request.form["option"]
    
    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses
    
    if len(responses) < len(surveys["satisfaction"].questions):
        return redirect(url_for("question", question_number=len(responses)))
    else:
        return redirect(url_for("complete"))


@app.route("/complete")
def complete():
    return render_template("complete.html")

if __name__ == "__main__":
    app.run(debug=True)



