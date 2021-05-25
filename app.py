import time
from io import BytesIO

from flask import Flask, render_template, request, redirect, flash, send_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rehegrjvfdn.weroro4h3dhio2ue3wfhergvdfkljcsk./jwqe3iru4t5gg'

timeout = 10 * 60
upload_time = -1
payload = None
payload_name = None

footer = '<br><br><button type="button" onclick="location.href=\'/\'" class="btn btn-primary">Back</button>'


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    global upload_time, payload, payload_name
    if time.time() - upload_time > timeout:
        payload, payload_name = None, None

    if request.method == 'GET':
        return render_template('home.html')

    if request.files['file']:
        payload = request.files['file'].read()
        payload_name = request.files['file'].filename
        upload_time = time.time()
        flash(f'File upload successful, available for {timeout / 60} mins')
    elif request.form['msg']:
        payload = request.form['msg']
        upload_time = time.time()
        flash(f'Msg upload successful, available for {timeout / 60} mins')
    else:
        flash('Enter a file or msg')

    return redirect('/')


@app.route('/recv')
def send():
    global payload, payload_name

    if time.time() - upload_time > timeout:
        payload, payload_name = None, None

    if type(payload) == bytes:
        return send_file(BytesIO(payload), attachment_filename=payload_name, as_attachment=True)
    else:
        if payload:
            return payload + footer
        else:
            flash('No file or msg found')
            return redirect('/')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
