from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


RESPONSES_KEY = 'responses'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'its-a-secret'
debug = DebugToolbarExtension(app)



@app.route('/')
def show_survey():
    """ Let user select a survey """

    return render_template('survey_start.html', survey=survey)


@app.route('/begin', methods=["POST"])
def start_survey():
    """ Shows the next Question for the user to answer """

    session[RESPONSES_KEY] = []

    return redirect('/questions/0')


@app.route('/answer', methods=['POST'])
def handle_question():

    """ Saves the answer and directs user to next question """

    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    
    else:
        return redirect(f"/questions/{len(responses)}")
    


@app.route('/questions/<int:qid>')
def show_question(qid):
    """ Will show the current question """

    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    
    if(len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("questions.html", question_num=qid, question=question)



@app.route("/complete")
def complete():
    """ You have completed the survey! """

    return render_template('complete.html')