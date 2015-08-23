from flask import Flask, render_template, request, make_response
import json
import os
from copy import copy

DEFAULT_DATABASE = {
    'spiders': [],
}
GLOBAL = {
    'database_path': None,
    'spiders': {},
}
ROOT = os.path.dirname(__file__)
app = Flask(__name__, template_folder=os.path.join(ROOT, 'templates'))


@app.route('/')
def home():
    spiders = []
    for spider in GLOBAL['spiders'].values():
        spider = copy(spider)
        if spider['pid']:
            spider['pid_live'] = psutil.pid_exists(spider['pid'])
        else:
            spider['pid_live'] = None
        spiders.append(spider)
    return render_template('home.html', spiders=spiders)


@app.route('/api/spider/register')
def api_spider_register():
    project_name = request.args.get('project_name', None)
    spider_name = request.args.get('spider_name', None)
    project_dir = request.args.get('project_dir', None)
    virtualenv_dir = request.args.get('virtualenv_dir', None)

    sid = '%s:%s' % (project_name, spider_name)
    if sid in GLOBAL['spiders']:
        spider = GLOBAL['spiders'][sid]
        if spider['state'] != 'stopped':
            error_data = {
                'error': {
                    'id': 'could-not-register-active-spider',
                    'status': '405',
                    'detail': 'Could not re-register existing spider that'\
                              ' is already arunning',
                },
            }
            res = make_response(json.dumps(error_data), 405)
            res.headers['Content-Type'] = 'application/json'
            return res

    spider = {
        'id': sid,
        'project_name': project_name,
        'spider_name': spider_name,
        'project_dir': project_dir, 
        'virtualenv_dir': virtualenv_dir,
    }
    GLOBAL['spiders'][sid] = normalize_spider_object(spider)
    save_database()

    res_data = {
        'data': {
            'type': 'spider',
            'id': sid,
        },
    }
    res = make_response(json.dumps(res_data))
    res.headers['Content-Type'] = 'application/json'
    return res


@app.route('/api/spider/<sid>/start')
def api_spider_start(sid):
    spider = GLOBAL['spiders'][sid]


def normalize_spider_object(spider):
    default = {
        'state': 'stopped',
        'pid': None,
        'host': 'localhost',
        'port': None,
    }
    for key, val in default.items():
        spider.setdefault(key, val)
    return spider


def load_database():
    try:
        db = json.load(open(GLOBAL['database_path']))
    except IOError:
        pass
    else:
        for key, val in db['spiders'].items():
            GLOBAL['spiders'][key] = normalize_spider_object(val)


def save_database():
    with open(GLOBAL['database_path'], 'w') as out:
        json.dump({
            'spiders': GLOBAL['spiders'],
        }, out)


def run_web_daemon(host, port, debug, database):
    GLOBAL['database_path'] = database
    load_database()
    app.run(host=host, port=port, debug=debug)
