from collections import Counter
from flask import Flask, session, redirect, url_for

import nltk
from flask import Flask, render_template, request, flash
from nltk.corpus import words

app = Flask(__name__)
app.secret_key = "HelloSam3"
word_list = words.words()
Matrix_list=['z','g','n','t','h','b','i','o','m','p','d','a','u','w','y','e']
score=0
vowels = ("a", "e", "i", "o", "u")
warning=""

words= []
w_size=0
visible= ""

@app.route('/')
def index():
   global words
   words=[]
   visible="hidden"
   return render_template('main.html',words=words, w_size=w_size,visible = visible)

@app.route('/endgame', methods = ["POST"])  
def validate():  
    if request.method == 'POST':  
        return redirect("http://localhost:5000/")

@app.route('/submit',methods = ['POST', 'GET'])
def word():
    visible=""
    longest_word_list = ['bigmouthed', 'deutonymph', 'gynephobia', 'hypozeugma', 'impoundage', 'phantomize', 'unbaptized']
    global score,words
    if request.method == 'POST':
      result = request.form['word_value']
      if result in longest_word_list:
          warning="Congratulations!!, You have founded longest word."
          flash(warning)
          words.append(result)
          w_size = len(words)
          return render_template('main.html',words=words,w_size=w_size,visible = visible)
      result = result.lower()
      dict = Counter(result)
      for key in dict.keys():
        if key not in Matrix_list:
            warning="Not matching with above character. "
            flash(warning)
            w_size = len(words)
            return render_template('main.html',words=words,w_size=w_size,visible = visible)

      for value in dict.values():
        if value == 2:
            warning="Same alphabet can't be used twice. "
            flash(warning)
            w_size = len(words)
            return render_template('main.html',words=words,w_size=w_size,visible = visible)

      if result in words :
        warning="You Already entered the word "
        flash(warning)
        w_size = len(words)
        return render_template('main.html',words=words,w_size=w_size,visible = visible)
      if any(v in result for v in vowels):
        if result in word_list:
            dict = Counter(result)
            print(dict)
            flag = 1
            for key in dict.keys():
                if key not in Matrix_list:
                    flag = 0
                if flag == 1 and len(result) >= 3:
                    score=score+len(result)
                    words.append(result)
                    print(words)
                    w_size = len(words)
                    return render_template('main.html',words = words,w_size=w_size,visible = visible)
                else: 
                    warning="Word length should be greater than 2. "
                    flash(warning)
                    w_size = len(words)
                    return render_template('main.html',words=words,w_size=w_size,visible = visible)
        else:
            warning="Entered word does not exist or Entered any foreign language word. "
            flash(warning)
            w_size = len(words)
            return render_template('main.html',words=words,w_size=w_size,visible = visible)
        
      else:
        warning="Not contain any vowel."
        flash(warning)
        return render_template('main.html',words=words,w_size=w_size,visible = visible)

      

if __name__ == '__main__':
   app.run(debug = True)