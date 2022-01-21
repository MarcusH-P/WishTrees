from flask import Flask, render_template, Blueprint, request, session
from flask_login import current_user, login_required
from app import db_add_commit
import random
import copy

quiz_blueprint = Blueprint('quiz', __name__, template_folder='templates')

# quiz 1 questions and answers
wishtrees_questions = {
    # Format is 'question':[options]
    'How much money has WishTrees raised': ['£10 million', '£1 billion', '£500,000', '£250,000'],
    'How many trees have WishTrees helped plant': ['1 million', '250,000', '12 million', '700,000'],
    'When was WishTrees founded': ['2012', '2020', '2015', '2008'],
    'How many countries has WishTrees planted in': ['42 countries', '3 countries', '18 countries', '72 countries'],
    'What can you do to help': ['All of the above', 'Donate to charities', 'Buy our merch', 'Complete our quizzes']
}

# quiz 2 questions and answers
LifeOnLand_questions = {
    # Format is 'question':[options]
    'What is the aim of the Life on Land sustainable goal': ['All of the above',
                                                             'Protect, restore and promote sustainable use of terrestrial systems',
                                                             'Sustainably manage forests and combat desertification',
                                                             'Halt and reverse land degradation'],
    'How many targets does the UN aim to achieve with this goal': ['12', '4', '9', '20'],
    'By what year does the UN want to end desertification and restore degraded land': ['2030', '2040', '2050', '2025'],
    'How do we protect endangered species': ['All of the above', 'Prevent poaching', 'End trafficking of animals',
                                             'Address the supply and demand of illegal wildlife products'],
    'How is the UN making this goal attractive to key players': ['Incentevise sustainable restructure',
                                                                 'Increasing taxes',
                                                                 'Encouraging unethical consumption',
                                                                 'Raising the prices of raw materials']
}

# quiz 3 questions and answers
PowerPlanters_questions = {
    # Format is 'question':[options]
    'How many acres of forest are destroyed each day': ['80,000', '400', '5,000', '41,000'],
    'How many trees would an average US citizen have to plant to be carbon neutral': ['620', '28', '1300', '370'],
    'How many species of plants, insects and animals are lost each day due to deforestation': ['137', 'None', '32',
                                                                                               '124'],
    'How many trees have been lost since the start of civilisation': ['34%', '8%', '50%', '18%'],
    'Which causes more carbon emissions': ['Deforestation', 'Vehicles', 'Factories', 'household energy']
}


# This function is for shuffling the dictionary elements.
def shuffle(q):
    selected_keys = []
    i = 0
    while i < len(q):
        current_selection = random.choice(list(q.keys()))
        if current_selection not in selected_keys:
            selected_keys.append(current_selection)
            i = i + 1
    return selected_keys


@quiz_blueprint.route('/quiz1')
@login_required
def quiz1():
    questions = copy.deepcopy(wishtrees_questions)
    questions_shuffled = shuffle(questions)
    for i in questions.keys():
        random.shuffle(questions[i])
    session['questions'] = questions
    session['answers'] = wishtrees_questions
    return render_template('quiz.html', q=questions_shuffled, o=questions, quizspeach='WishTrees Quiz')


@quiz_blueprint.route('/quiz2')
@login_required
def quiz2():
    questions = copy.deepcopy(LifeOnLand_questions)
    questions_shuffled = shuffle(questions)
    for i in questions.keys():
        random.shuffle(questions[i])
    session['questions'] = questions
    session['answers'] = LifeOnLand_questions
    return render_template('quiz.html', q=questions_shuffled, o=questions, quizspeach='UN Sustainable Goal 15 - Life on Land Quiz')


@quiz_blueprint.route('/quiz3')
@login_required
def quiz3():
    questions = copy.deepcopy(PowerPlanters_questions)
    questions_shuffled = shuffle(questions)
    for i in questions.keys():
        random.shuffle(questions[i])
    session['questions'] = questions
    session['answers'] = PowerPlanters_questions
    return render_template('quiz.html', q=questions_shuffled, o=questions, quizspeach='PowerPlanters Quiz')


@quiz_blueprint.route('/quiz', methods=['POST'])
def quiz_answers():
    correct = 0
    questions = session['questions']
    answers = session['answers']
    for i in questions.keys():
        answered = request.form[i]
        if answers[i][0] == answered:
            correct = correct + 1
    the_user = current_user
    the_user.points = current_user.points + (correct * 100)
    db_add_commit(the_user)
    return '<h1>Correct Answers: <u>' + str(correct) + "</u></h1> <h3><a href="+'"games"'+">Click here to play again!</a></h3>"
