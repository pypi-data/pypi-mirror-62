import argparse
import sys
import logging

import wexpect.console_reader as console_reader
import wexpect.wexpect_util as wexpect_util


logger = logging.getLogger('wexpect')
logger.info('Hello')

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser(description='Wexpect: executable automation for Windows.')

    parser.add_argument('--console_reader_class', type=str,
                        help='Class name of the console reader class.')

    parser.add_argument('command', type=str, nargs='+', help='Command to be run with its arguments')
    parser.add_argument('--host_pid', type=int, help='Host process process ID')
    parser.add_argument('--codepage', type=str, help='Codepage')
    parser.add_argument('--window_size_x', type=int, help='Width of the console window', default=80)
    parser.add_argument('--window_size_y', type=int, help='Height of the console window', default=25)
    parser.add_argument('--buffer_size_x', type=int, help='Width of the console buffer', default=80)
    parser.add_argument('--buffer_size_y', type=int, help='Height of the console buffer',
                        default=16000)
    parser.add_argument('--local_echo', type=str, help='Echo sent characters', default=True)
    parser.add_argument('--interact', type=str, help='Show console window', default=False)
    args = parser.parse_args()
    logger.info(f'Starter arguments: {args}')

    if args.console_reader_class == 'ConsoleReaderSocket':
        conole_reader_class = console_reader.ConsoleReaderSocket
    elif args.console_reader_class == 'ConsoleReaderPipe':
        conole_reader_class = console_reader.ConsoleReaderPipe

    command = wexpect_util.join_args(args.command)

    cons = conole_reader_class(
        path=command, host_pid=args.host_pid, codepage=args.codepage,
        window_size_x=args.window_size_x, window_size_y=args.window_size_y,
        buffer_size_x=args.buffer_size_x, buffer_size_y=args.buffer_size_y,
        local_echo=str2bool(args.local_echo), interact=str2bool(args.interact))

    sys.exit(cons.child_exitstatus)

if __name__ == "__main__":
    main()
