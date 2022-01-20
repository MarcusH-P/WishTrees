from flask import Flask, render_template, Blueprint, request
import random
import copy

quiz_blueprint = Blueprint('quiz', __name__, template_folder='templates')

wishtrees_questions = {
    # Format is 'question':[options]
    'How much money has WishTrees raised': ['£10 million', '£1 billion', '£500,000', '£250,000'],
    'How many trees have WishTrees help plant': ['1 million', '250,000', '12 million', '700,000'],
    'When was WishTrees founded': ['2012', '2020', '2015', '2008'],
    'How many countries has WishTrees planted in': ['42 countries', '3 countries', '18 countries', '72 countries'],
    'What can you do to help': ['All of the above', 'Donate to charities', 'Buy our merch', 'Complete our quizzes']
}

questions = copy.deepcopy(wishtrees_questions)
#  questions = wishtrees_questions


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


@quiz_blueprint.route('/quiz')
def quiz():
    questions_shuffled = shuffle(questions)
    for i in questions.keys():
        random.shuffle(questions[i])
    return render_template('quiz1.html', q=questions_shuffled, o=questions)


@quiz_blueprint.route('/quiz', methods=['POST'])
def quiz_answers():
    correct = 0
    for i in questions.keys():
        answered = request.form[i]
        if wishtrees_questions[i][0] == answered:
            correct = correct + 1
    return '<h1>Correct Answers: <u>' + str(correct) + '</u></h1>'
