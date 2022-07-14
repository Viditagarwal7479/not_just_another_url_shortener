import os
import time
import config
from flask import Flask, redirect, render_template, request, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='', static_folder=config.UPLOAD_FOLDER, template_folder=config.TEMPLATE_FOLDER)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
data = {}


def clean():
    # day = time.gmtime().tm_mday
    # month = time.gmtime().tm_mon
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))


@app.route('/')
def aux():
    return redirect(url_for('.forms'))


@app.route('/main', methods=['GET', 'POST'])
def forms():
    if request.method == 'POST':
        a = request.form.get("Enter original url").strip().strip('/')
        b = request.form.get("Enter short version").strip()
        if a == "" or b == "":
            return render_template('index.html', warning=1)
        elif b in data:
            return render_template('index.html', warning=2)
        elif a.split(':')[0] not in ['https', 'http']:
            return render_template('index.html', warning=3)
        elif not b.isalnum():
            return render_template('index.html', warning=4)
        else:
            data[b] = {
                'url': a,
                'vis': {},
                'count': 0
            }
        return render_template('index.html', a=request.base_url[:-4] + 'q=' + b, saved=True)
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and request.form.get('key').strip() == config.MASTER_KEY:
        file = request.files['file']
        file.filename = file.filename.strip()
        if not file or file.filename == '':
            return render_template('upload.html', warning=1)
        if file.filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
            return render_template('upload.html', warning=2)
        filename = secure_filename(file.filename)
        filename, extension = filename.rsplit('.', maxsplit=1)
        fid = ''.join(map(str, list(time.gmtime())[1:-3]))
        filename += '.' + fid + '.' + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('upload.html', warning=-1, link=request.base_url[:-6] + 'f=' + fid)
    if request.method == 'POST' and request.form.get('key').strip() == config.CLEAN_KEY:
        clean()
    return render_template('upload.html', warning=0)


@app.route('/f=<name>')
def showit(name: str):
    name = str(name).strip()
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in files:
        if file.find(name) != -1:
            # if file.endswith('.pdf'):
            # return send_from_directory(app.config['UPLOAD_FOLDER'], file, as_attachment=True)
            # elif file.endswith('.txt'):
            #     text = ''
            #     with open(file, 'r') as f:
            #         for t in f:
            #             text += t
            #     return t
            # else:
            return render_template('showfile.html', image=not file.endswith('.pdf'),
                                   path=file)
    return render_template('showfile.html', path=-1)


@app.route('/d=<name>')
def download(name: str):
    name = str(name).strip()
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in files:
        if file.find(name) != -1:
            return send_from_directory(app.config['UPLOAD_FOLDER'], file, as_attachment=True)
    return render_template('showfile.html', path=-1)


@app.route('/q=<url>')
def redirect_page(url):
    url = url.strip()
    if url not in data:
        return render_template('index.html', warning=5)
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if ip in data[url]['vis']:
        data[url]['vis'][ip] = data[url]['vis'][ip] + 1
    else:
        data[url]['vis'][ip] = 1
    data[url]['count'] = data[url]['count'] + 1
    return redirect(data[url]['url'])


@app.route('/stat', methods=['GET', 'POST'])
def get_count():
    if request.method == 'POST':
        url = request.form.get('URL')
        if url.split('q=')[0] == request.base_url[:-4] and len(url.split('q=')) == 2:
            return render_template('stats.html', data=data, url=url.split('q=')[1], basic=False, warning=False)
        else:
            return render_template('stats.html', basic=True, warning=True)
    return render_template('stats.html', basic=True)


@app.route('/detailed?surl=<surl>')
def detailed(surl):
    surl = surl.strip()
    return render_template('detail.html', surl=surl, data=data, visitors=len(data[surl]['vis']))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route(f'/{config.MASTER_KEY}')
def sudo():
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
