# from gevent.wsgi import WSGIServer
# from gevent.wsgi import WSGIServer

import subprocess, os, re, argparse
from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)
pattern = None
dev_list = None



@app.route("/")
def net():
    rules = get_active_rules()
    return render_template('net.html', rules=rules)


@app.route('/new_rule/<interface>', methods=['POST'])
def new_rule(interface):
    delay = request.form['Delay']
    loss = request.form['Loss']
    duplicate = request.form['Duplicate']
    reorder = request.form['Reorder']
    corrupt = request.form['Corrupt']
    rate = request.form['Rate']

    # # # remove old setup
    command = 'tc qdisc del dev %s root netem' % interface
    command = command.split(' ')
    proc = subprocess.Popen(command)
    proc.wait()

    # apply new setup
    command = 'tc qdisc add dev %s root netem' % interface
    # command = 'tc qdisc change dev %s root netem' % interface
    if rate != '':
        command += ' rate %smbit' % rate
    if delay != '':
        command += ' delay %sms' % delay
    if loss != '':
        command += ' loss %s%%' % loss
    if duplicate != '':
        command += ' duplicate %s%%' % duplicate
    if reorder != '':
        command += ' reorder %s%%' % reorder
    if corrupt != '':
        command += ' corrupt %s%%' % corrupt
    print(command)
    command = command.split(' ')
    proc = subprocess.Popen(command)
    proc.wait()
    return redirect(url_for('net'))


@app.route('/remove_rule/<interface>', methods=['POST'])
def remove_rule(interface):
    # remove old setup
    command = 'tc qdisc del dev %s root netem' % interface
    command = command.split(' ')
    proc = subprocess.Popen(command)
    proc.wait()
    return redirect(url_for('net'))


def get_active_rules():
    proc = subprocess.Popen(['tc', 'qdisc'], stdout=subprocess.PIPE)
    output = proc.communicate()[0].decode()
    lines = output.split('\n')[:-1]
    rules = []
    dev = set()
    for line in lines:
        arguments = line.split(' ')
        rule = parse_rule(arguments)
        if rule['name'] and rule['name'] not in dev:
            rules.append(rule)
            dev.add(rule['name'])
    return rules


def parse_rule(splitted_rule):
    rule = {'name': None,
            'rate': None,
            'delay': None,
            'loss': None,
            'duplicate': None,
            'reorder': None,
            'corrupt': None}
    i = 0
    for argument in splitted_rule:
        if argument == 'dev':
            if pattern is None and dev_list is None:
                rule['name'] = splitted_rule[i + 1]
            if pattern:
                if pattern.match(splitted_rule[i + 1]):
                    rule['name'] = splitted_rule[i + 1]
            if dev_list:
                if splitted_rule[i + 1] in dev_list:
                    rule['name'] = splitted_rule[i + 1]
        elif argument == 'rate':
            rule['rate'] = splitted_rule[i + 1].split('Mbit')[0]
        elif argument == 'delay':
            rule['delay'] = splitted_rule[i + 1]
        elif argument == 'loss':
            rule['loss'] = splitted_rule[i + 1]
        elif argument == 'duplicate':
            rule['duplicate'] = splitted_rule[i + 1]
        elif argument == 'reorder':
            rule['reorder'] = splitted_rule[i + 1]
        elif argument == 'corrupt':
            rule['corrupt'] = splitted_rule[i + 1]
        i += 1
    return rule


if __name__ == "__main__":
    app.debug = True
    # app.secret_key = ''
    #app.run(host='127.0.0.1', port=5500)
    app.run(host='192.168.56.101', port=5500)
    # http_server = wsgiserver(('192.168.56.101', 5000), app)
    # http_server.serve_forever()
