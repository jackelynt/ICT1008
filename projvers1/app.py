from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def hello():
    return render_template('login.html')

@app.route('/success/<startloc> <endloc>')
def success(startloc, endloc):
    return (f'Start search for {startloc} to {endloc}')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        start_loc = request.form['start']
        end_loc = request.form['end']
        return redirect(url_for('success', startloc = start_loc, endloc = end_loc))
    else:
        start_loc = request.args.get('start')
        end_loc = request.args.get('end')
        return redirect(url_for('success', startloc = start_loc, endloc = end_loc))



if __name__ == '__main__':
    app.run(debug=True)