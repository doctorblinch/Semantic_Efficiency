from flask import Flask, render_template, redirect, url_for, request
from Semantic_Affinity import main

app = Flask(__name__)

sortedText = []

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/unswer')
def unswer():
    sortedText = main()
    return render_template('unswer.html', text = sortedText)

@app.route('/', methods=['POST'])
def my_form_post():
    number = request.form['mainNum']
    text = request.form['text']
    fout = open('in.txt', 'w')
    fout.write(text)
    fout.close()
    fout = open('inNum.txt', 'w')
    fout.write(str(number))
    fout.close()
    sortedText = main()
    return redirect(url_for('unswer', text = sortedText))

if __name__ == '__main__':
    app.run(debug=True)
