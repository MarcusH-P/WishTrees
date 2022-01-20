from models import Quiz
import random, copy

wishtrees_questions = {
    #Format is 'question':[options]
    'How much money has WishTrees raised' :['£10 million','£1 billion','£500,000','£250,000'],
    'How many trees have WishTrees help plant' :['1 million','250,000','12 million','700,000'],
    'When was WishTrees founded' :['2012','2020','2015','2008'],
    'countries_planted' :['42 countries','3 countries','18 countries','72 countries'],
    'help' :['All of the above','Donate to charities','Buy our merch','Complete our quizzes']
}

def quiz():
    correct = 0
    for i in
