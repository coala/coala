import sys
import json

if __name__ == "__main__":

    line = sys.stdin.read()
    args = json.loads(line)
    settings = args['settings']

    out = [{
            'message': "This is wrong",
            'file': args['filename'],
            'severity': "MAJOR",
            'line': 1
        }, {
            'message': "This is wrong too",
            'file': args['filename'],
            'severity': "INFO",
            'line': 3}]

    if settings['a']:
        for res in out:
            res['severity'] = "NORMAL"

    if settings['b']:
        out[0]['debug_msg'] = "Sample debug message"

    if not settings['c']:
        out[1]['message'] = "Different message"

    json_dump = json.dumps(out)
    sys.stdout.write(json_dump)
