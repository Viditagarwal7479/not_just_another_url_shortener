from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
data = {}


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


@app.route('/q=<url>')
def redirect_page(url):
    if request.remote_addr in data[url]['vis']:
        data[url]['vis'][request.remote_addr] = data[url]['vis'][request.remote_addr] + 1
    else:
        data[url]['vis'][request.remote_addr] = 1
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
    return render_template('detail.html', surl=surl, data=data, visitors=len(data[surl]['vis']))


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
