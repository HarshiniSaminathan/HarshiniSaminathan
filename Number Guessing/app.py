import random
from flask import Flask,request
from response import success_response,failure_response
app = Flask(__name__)

TotalScore = 100
GeneratedNumber = str(random.randint(1, 100))
print(GeneratedNumber,'want to guess')


def clues(GeneratedNumber):
    if int(GeneratedNumber) % 2 == 0 :
        return 'EVEN Number'
    else:
        return 'ODD Number'


@app.route('/', methods=['GET'])
def guess_a_number():
    global GeneratedNumber
    clue=clues(GeneratedNumber)
    return success_response({'CLUES':clue,'message': 'Guess A Number From 1 to 100', 'Score': f'Your Current Score: {TotalScore}'})

def specialClue1(GeneratedNumber):
    LastNumber = int(GeneratedNumber)%10
    return f'Number ends with {LastNumber}'

def clue1(GeneratedNumber,Number):
    if int(GeneratedNumber)>= 75:
        if int(Number) >= 75 :
            return specialClue1(GeneratedNumber)
        return 'Number will be 100<=75'
    if int(GeneratedNumber)>= 50:
        if int(Number)>=50:
            return specialClue1(GeneratedNumber)
        return 'Number will be 75<=50'
    if int(GeneratedNumber)>= 25 :
        if int(Number)>=25:
            return specialClue1(GeneratedNumber)
        return 'Number will be 50<= 25'
    if int(GeneratedNumber) >= 10:
        if int(Number)>=10:
            return specialClue1(GeneratedNumber)
        return 'Number will be 25<=10'
    if int(GeneratedNumber)>=0:
        if int(Number)>=0:
            return specialClue1(GeneratedNumber)
        return 'Number will be from 1 to 9'


def clue2(GeneratedNumber):
    if int(GeneratedNumber) > 1:
        if (int(GeneratedNumber) % 2 == 0 and int(GeneratedNumber) != 2) or (int(GeneratedNumber) % 3 == 0 and int(GeneratedNumber) != 3) or (int(GeneratedNumber) % 5 == 0 and int(GeneratedNumber) != 5):
            if int(GeneratedNumber) % 10 == 0:
                return 'Divisible By 10'
            if int(GeneratedNumber) % 9 == 0:
                return 'Divisible By 9'
            if int(GeneratedNumber) % 8 == 0:
                return 'Divisible By 8'
            if int(GeneratedNumber) % 7 == 0:
                return 'Divisible By 7'
            if int(GeneratedNumber) % 6 == 0:
                return 'Divisible By 6'
            if int(GeneratedNumber) % 5 == 0:
                return 'Divisible By 5'
            if int(GeneratedNumber) % 4 == 0:
                return 'Divisible By 4'
            if int(GeneratedNumber) % 3 == 0:
                return 'Divisible By 3'
            if int(GeneratedNumber) % 2 == 0:
                return 'Divisible By 2'
        else:
            return 'Prime Number'

    else:
        return 'Not a Prime Number'


def clue3(GeneratedNumber,Number):
    if int(GeneratedNumber) > int(Number):
        return f'Number is greater than {Number}'
    else:
        return f'Number is lesser than {Number}'


@app.route('/GuessedNumber', methods=['POST'])
def guessed_number():
    global TotalScore
    global GeneratedNumber
    data = request.get_json()
    Number = data['Number']
    if int(Number) == int(GeneratedNumber):
        return success_response({'message': 'You entered a correct Number', 'Score': f'Your Current Score: {TotalScore}'})
    else:
        while TotalScore > 0:
            if TotalScore == 100:
                clues = clue1(GeneratedNumber,Number)
                TotalScore -= 25
                return failure_response({'CLUES':clues,'message': 'You entered an incorrect Number', 'Score': f'Your Current Score: {TotalScore}'})
            if TotalScore == 75:
                clues = clue2(GeneratedNumber)
                TotalScore -= 25
                return failure_response({'CLUES':clues,'message': 'You entered an incorrect Number', 'Score': f'Your Current Score: {TotalScore}'})
            if TotalScore == 50:
                clues = clue3(GeneratedNumber,Number)
                TotalScore -= 25
                return failure_response({'CLUES':clues,'message': 'You entered an incorrect Number', 'Score': f'Your Current Score: {TotalScore}'})
            if TotalScore == 25:
                TotalScore -= 25
                return failure_response({'message': f'GAME OVER The Number : {GeneratedNumber}', 'Score': f'Your Current Score: {TotalScore}'})
        return failure_response(
            {'message': f'GAME OVER The Number : {GeneratedNumber}', 'Score': f'Your Current Score: {TotalScore}'})

if __name__ == "__main__":
    app.run(debug=True, port=5009)
