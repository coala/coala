# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json

from coalib.coala_main import run_coala
from coalib.output.JSONEncoder import create_json_encoder
from coalib.output.printers.ListLogPrinter import ListLogPrinter
from coalib.parsing.DefaultArgParser import default_arg_parser


def main():
    # Note: We parse the args here once to find the log printer to use.
    #       Also, commands like -h (help) and -v (version) are executed here.
    #       The args are again parsed later to find the settings and configs
    #       to use during analysis.
    arg_parser = default_arg_parser()
    args = arg_parser.parse_args()

    log_printer = None if args.text_logs else ListLogPrinter()
    results, exitcode, _ = run_coala(log_printer=log_printer, autoapply=False)

    retval = {"results": results}
    if not args.text_logs:
        retval["logs"] = log_printer.logs
    JSONEncoder = create_json_encoder(use_relpath=args.relpath)
    if args.output:
        filename = str(args.output)
        with open(filename, 'w+') as fp:
            json.dump(retval, fp,
                      cls=JSONEncoder,
                      sort_keys=True,
                      indent=2,
                      separators=(',', ': '))
    else:
        print(json.dumps(retval,
                         cls=JSONEncoder,
                         sort_keys=True,
                         indent=2,
                         separators=(',', ': ')))

    return exitcode
