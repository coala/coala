import os
import sys
import json

# Start ignoring PycodestyleBear* as those imports may raise
# import warnings
sys.path.append(os.path.join(os.path.dirname(__file__),
                             '..', '..', '..', '..'))

from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange
from coalib.output.JSONEncoder import create_json_encoder
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
# Stop ignoring

if __name__ == '__main__':

    line = sys.stdin.read()
    args = json.loads(line)
    settings = args['settings']

    results = [
        Result(
            origin='TestBear',
            message='This is wrong',
            affected_code=(SourceRange.from_values(args['filename'], 1),),
            severity=RESULT_SEVERITY.MAJOR),
        Result(
            origin='TestBear',
            message='This is wrong too',
            affected_code=(SourceRange.from_values(args['filename'], 3),),
            severity=RESULT_SEVERITY.INFO)]

    if settings['set_normal_severity']:
        for res in results:
            res.severity = RESULT_SEVERITY.NORMAL

    if settings['set_sample_dbg_msg']:
        results[0].debug_msg = 'Sample debug message'

    if not settings['not_set_different_msg']:
        results[1].message = 'Different message'

    out = {}
    out['results'] = results

    JSONEncoder = create_json_encoder()

    json_dump = json.dumps(out, cls=JSONEncoder)
    sys.stdout.write(json_dump)
