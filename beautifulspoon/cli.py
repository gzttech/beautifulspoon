#-*- coding: utf-8 -*-
import sys
import argparse
import bs4


def soup(html):
    return bs4.BeautifulSoup(html, 'html.parser')


def tag(html):
    s = bs4.BeautifulSoup(html, 'html.parser')
    return list(s.children)[0]


METHODS = {
    'set_name': {
        'argument': ['--set_name'],
        'argument_dict': {
            'action': 'store',
            'metavar': 'NAME'
        } ,
        'method': '_set_name',
        'args': [{
            'type': str
        }]
    },
    'set_attr': {
        'argument': ['--set_attr'],
        'argument_dict': {
            'action': 'store',
            'nargs': 2,
            'metavar': 'NAME, VALUE'
        } ,
        'method': '_set_attr',
        'args': [
            {
                'type': str
            },
            {
                'type': str
            }
        ]
    },
    'set_string': {
        'argument': ['--set_string'],
        'argument_dict': {
            'action': 'store',
            'metavar': 'STRING'
        } ,
        'method': '_set_string',
        'args': [{
            'type': str
        }]
    },
    'append': {
        'argument': ['-a', '--append'],
        'argument_dict': {
            'action': 'store',
            'metavar': 'HTML'
        } ,
        'method': 'append',
        'args': [{
            'type': soup
        }]
    },
    'extend': {
        'argument': ['-e', '--extend'],
        'argument_dict': {
            'action': 'store',
            'metavar': 'STRING'
        } ,
        'method': 'extend',
        'args': [{
            'type': str
        }]
    },
    'insert': {
        'argument': ['-i', '--insert'],
        'argument_dict': {
            'action': 'store',
            'nargs': 2,
            'metavar': 'POS, HTML'
        },
        'method': 'insert',
        'args': [
            {
                'type': int
            },
            {
                'type': soup
            },
        ]
    },
    'insert_before': {
        'argument': ['--ib', '--insert_before'],
        'argument_dict': {
            'action': 'store',
            'metavar': 'HTML'
        },
        'method': 'insert_before',
        'args': [{
            'type': soup
        }]
    },
    'insert_after': {
        'argument': ['--ia', '--insert_after'],
        'argument_dict': {
            'action': 'store',
            'metavar': 'HTML'
        },
        'method': 'insert_after',
        'args': [{
            'type': str
        }]
    },
    'clear': {
        'argument': ['-c', '--clear'],
        'argument_dict': {
            'action': 'store_true',
        },
        'method': 'clear',
        'args': []
    },
    'decompose': {
        'argument': ['-d', '--decompose'],
        'argument_dict': {
            'action': 'store_true',
        },
        'method': 'decompose',
        'args': []
    },
    'replace_with': {
        'argument': ['-r', '--replace_with'],
        'argument_dict': {
            'action': 'store',
            'metavar': 'HTML'
        },
        'method': 'replace_with',
        'args': [{
            'type': soup
        }]
    },
    'wrap': {
        'argument': ['-w', '--wrap'],
        'argument_dict': {
            'action': 'store',
        },
        'method': 'wrap',
        'args': [{
            'type': tag
        }]
    },
    'unwrap': {
        'argument': ['-u', '--unwrap'],
        'argument_dict': {
            'action': 'store_true',
        },
        'method': 'unwrap',
        'args': []
    },
}


def _set_name(selected, name):
    selected.name = name


def _set_attr(selected, name, value):
    selected[name] = value


def _set_string(selected, value):
    selected.string = value


def update_method_args(parser):
    for key, info in METHODS.items():
        parser.add_argument(*info['argument'],
                            default=argparse.SUPPRESS,
                            **info['argument_dict'])


def parse_args(parser):
    parser.add_argument("--select", default='')
    parser.add_argument("file", default='', nargs="?")
    update_method_args(parser)
    return parser.parse_known_args()


def execute_methods(selected, args):
    for key, value in args.items():
        info = METHODS.get(key)
        if not info:
            continue
        if info['method'].startswith('_'):
            method = lambda *sub: globals()[info['method']](selected, *sub)
        else:
            method = getattr(selected, info['method'])
        if isinstance(value, str) and info['args']:
            value = info['args'][0].get('type')(value)
            return method(value)
        elif isinstance(value, (tuple, list)) and info['args']:
            value = [f['type'](x) for f, x in zip(info['args'], value)]
            return method(*value)
        else:
            return method()
    return False


def main():
    parser = argparse.ArgumentParser(prog="beautifulsoup", add_help=True)
    args, rest = parse_args(parser)
    if not sys.stdin.isatty():
        source_fd = sys.stdin
    else:
        source_fd = open(args.file)
    doc = bs4.BeautifulSoup(source_fd, 'html.parser')
    ret = doc
    if args.select:
        selected = doc.select_one(args.select)
        handled = execute_methods(selected, vars(args))
        if handled == False:
            ret = selected
    print(ret.prettify())


if __name__ == '__main__':
    main()