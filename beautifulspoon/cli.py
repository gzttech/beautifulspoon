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
            'metavar': 'NAME',
            'help': 'Set the tag name of the selected node.'
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
            'metavar': ('NAME', 'VALUE'),
            'help': 'Set the attribute(i.e., the name/value pair) of the selected node.'
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
            'metavar': 'STRING',
            'help': 'The the string(text) of the selected node.'
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
            'metavar': 'HTML',
            'help': 'Append a node(HTML) inside the selected node.'
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
            'metavar': 'STRING',
            'help': 'Extend the string(text) of the selected node.'
        } ,
        'method': 'extend',
        'args': [{
            'type': lambda x: [str(x)]
        }]
    },
    'insert': {
        'argument': ['-i', '--insert'],
        'argument_dict': {
            'action': 'store',
            'nargs': 2,
            'metavar': ('POS', 'HTML'),
            'help': 'Insert a node(HTML) at the POS position of the seleted node.'
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
        'argument': ['--insert_before', '--ib'],
        'argument_dict': {
            'action': 'store',
            'metavar': 'HTML',
            'help': 'Insert a node(HTML) before the seleted node.'
        },
        'method': 'insert_before',
        'args': [{
            'type': soup
        }]
    },
    'insert_after': {
        'argument': ['--insert_after', '--ia'],
        'argument_dict': {
            'action': 'store',
            'metavar': 'HTML',
            'help': 'Insert a node(HTML) after the seleted node.'
        },
        'method': 'insert_after',
        'args': [{
            'type': soup
        }]
    },
    'clear': {
        'argument': ['-c', '--clear'],
        'argument_dict': {
            'action': 'store_true',
            'help': 'Clear the inner content of the seleted node.'
        },
        'method': 'clear',
        'args': []
    },
    'decompose': {
        'argument': ['-d', '--decompose'],
        'argument_dict': {
            'action': 'store_true',
            'help': 'Remove the node along with its inner content of the seleted node.'
        },
        'method': 'decompose',
        'args': []
    },
    'replace_with': {
        'argument': ['-r', '--replace_with'],
        'argument_dict': {
            'action': 'store',
            'metavar': 'HTML',
            'help': 'Replace the seleted node with HTML.'
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
            'metavar': 'HTML',
            'help': 'Wrap the seleted node with tag provided(HTML).'
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
            'help': 'Unwrap the seleted node.'
        },
        'method': 'unwrap',
        'args': []
    },
    'comment': {
        'argument': ['--comment'],
        'argument_dict': {
            'action': 'store_true',
            'help': 'Comment the seleted node.'
        },
        'method': '_comment',
        'args': []
    },
}


def _set_name(selected, name):
    selected.name = name


def _set_attr(selected, name, value):
    selected[name] = value


def _set_string(selected, value):
    selected.string = value


def _comment(selected):
    selected.replace_with(soup('<!-- %s -->' % str(selected)))


def update_method_args(parser):
    for key, info in METHODS.items():
        parser.add_argument(*info['argument'],
                            default=argparse.SUPPRESS,
                            **info['argument_dict'])


def parse_args(parser):
    parser.add_argument("--select", default='')
    parser.add_argument("--smooth",
                        action='store_true',
                        help='Smooth the seleted node.')
    parser.add_argument("--get_text",
                        action='store_true',
                        help='Get the text of the selected node.')
    parser.add_argument("--output", "-o",
                        default='',
                        help='Output filename, blank for stdout.')
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
    if args.file:
        source_fd = open(args.file)
    elif not sys.stdin.isatty():
        source_fd = sys.stdin
    else:
        parser.print_help()
        sys.exit(0)
    source_content = source_fd.read()
    source_fd.close()
    doc = bs4.BeautifulSoup(source_content, 'html.parser')
    ret = doc
    if args.select:
        selected = doc.select_one(args.select)
        handled = execute_methods(selected, vars(args))
        if handled == False:
            ret = selected
        if selected and args.smooth:
            selected.smooth()
    if ret:
        output_fd = open(args.output, 'w') if args.output else sys.stdout
        if args.get_text:
            print(ret.get_text(), file=output_fd)
        else:
            print(ret.prettify(), file=output_fd)
        output_fd.close()


if __name__ == '__main__':
    main()
