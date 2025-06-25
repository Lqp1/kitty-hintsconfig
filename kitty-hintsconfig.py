import re
import os
try:
    import yaml
except:
    # FIXME: Ugly hack on NixOS where it does not seem possible to override the Python interpreter used from Kitty
    # Maybe I'm just bad to Nix things, any help appreciated here!
    import subprocess
    import sys
    potential_packages = filter(lambda x: len(x) > 0,
                                subprocess.check_output(['/run/current-system/sw/bin/python', '-c' ,'import sys; print("\\n".join(sys.path))'])\
                                        .decode('utf8').split("\n"))
    sys.path.extend(potential_packages)
    import yaml



def config(file='~/.config/kitty/hints.yaml'):
    file = os.path.expanduser(file)
    if os.path.isfile(file):
        with open(file, 'r') as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(f"=> {exc}")
    else:  # simple default config
        return {
            'links': [
                {'regexp': r'((www|http:|https:)+[^\s]+[\w])', 'link': '{}'},
                {'regexp': r'file://([^\s]*)', 'process': 'xdg-open {}'},
            ],
            'markers': [
                {'regexp': 'error', 'marker': 3},
                {'regexp': 'warning', 'marker': 2},
                {'regexp': 'info', 'marker': 1}
            ]
        }


def config_links():
    return config()['links']


def config_markers():
    return config()['markers']


def mark(text, args, Mark, extra_cli_args, *a):
    marks = [ m for m in _mark(text) ]
    sorted_marks = sorted(marks, key=lambda m: m['start'])
    return [Mark(idx, m['start'], m['end'], m['text'], m['data']) for idx, m in enumerate(sorted_marks)]


def _mark(text):
    for rule in config_links():
        for m in re.finditer(rule['regexp'], text):
            start, end = m.span()
            mark_text = m.group(1).replace('\n', '').replace('\0', '')
            if 'link' in rule:
                link = rule['link'].format(mark_text)
                data = {'link': link}
            if 'process' in rule:
                process = rule['process'].format(mark_text)
                data = {'process': process}
            yield {'start': start, 'end': end, 'text': m.group(0), 'data': data}


def handle_result(args, data, target_window_id, boss, extra_cli_args, *a):
    matches, groupdicts = [], []
    for m, g in zip(data['match'], data['groupdicts']):
        if m:
            matches.append(m), groupdicts.append(g)
    for match_data in groupdicts:
        if 'link' in match_data:
            boss.open_url(match_data['link'])
        elif 'process' in match_data:
            os.system(match_data['process'])


def marker(text):
    for rule in config_markers():
        for m in re.finditer(rule['regexp'], text, re.IGNORECASE):
            start, end = m.span()
            yield start, end, rule['marker']
