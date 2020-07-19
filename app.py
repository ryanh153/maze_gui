from flask import Flask, render_template, request
from pathlib import Path

app = Flask(__name__)


@app.route('/')
def index():
    print("Entering home")
    return render_template('main/index.html')


@app.route('/instructions')
def instructions():
    print("Entering instructions")
    return render_template('main/instructions.html')


@app.route('/enter_code')
def enter_code():
    return render_template('main/enter_code.html')


@app.route('/code_entered', methods=['POST'])
def code_entered():
    if request.method == 'POST':
        print(request.form['user_code'])
        return render_template('main/enter_code.html', text="Codes not implemented yet. Sorry.")


@app.route('/test_level')
def test_level():
    print("Entering test_level")
    im_path = Path('static/img/my_image.png').absolute()
    print(str(im_path))
    return render_template('levels/test_level.html', im_path=im_path)


if __name__ == '__main__':
    app.run()
