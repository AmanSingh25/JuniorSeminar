from flask import Flask, render_template, request
from model import retrieve_csv_data, majors_at_fisk

app = Flask(__name__)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    

@app.route('/broucherList')
@app.route('/broucherList', methods=['GET', 'POST'])
def graduation_broucher():
    if request.method == "POST":
        csv_file = request.form['filename']
        if csv_file[-3:] != 'csv':
            return render_template('redirect.html')

        data = retrieve_csv_data(csv_file)
        return render_template('broucherList.html', student_data = data, majors = majors_at_fisk(csv_file))
    return render_template('broucherList.html')

if __name__ == "__main__":
    app.run()