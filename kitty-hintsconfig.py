import re
import os
import yaml


def config(file='~/.config/kitty/hints.yaml'):
    if os.path.isfile(file):
        with open(file, 'r') as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)
    else:  # simple default config
        return {
            'links': [
                {'regexp': r'(https?://[^\s]*)', 'link': '{}'},
                {'regexp': r'file://([^\s]*)', 'process': 'xdg-open {}'},
            ],
            'markers': [
                {'regexp': 'error', 'marker': 1},
                {'regexp': 'warning', 'marker': 2},
                {'regexp': 'info', 'marker': 3}
            ]
        }


def config_links():
    return config()['links']


def config_markers():
    return config()['markers']


def mark(text, args, Mark, extra_cli_args, *a):
    idx = 0
    for rule in config_links():
        for m in re.finditer(rule['regexp'], text):
            start, end = m.span()
            print(m)
            mark_text = m.groups()[0].replace('\n', '').replace('\0', '')
            if 'link' in rule:
                link = rule['link'].format(mark_text)
                data = {'link': link}
            if 'process' in rule:
                process = rule['process'].format(mark_text)
                data = {'process': process}

            yield Mark(idx, start, end, mark_text, data)
            idx += 1


def handle_result(args, data, target_window_id, boss, extra_cli_args, *a):
    matches, groupdicts = [], []
    for m, g in zip(data['match'], data['groupdicts']):
        if m:
            matches.append(m), groupdicts.append(g)
    for match, match_data in zip(matches, groupdicts):
        if 'link' in match_data:
            boss.open_url(match_data['link'])
        elif 'process' in match_data:
            os.system(match_data['process'])


def marker(text):
    for rule in config_markers():
        for m in re.finditer(rule['regexp'], text, re.IGNORECASE):
            start, end = m.span()
            yield start, end, rule['marker']
