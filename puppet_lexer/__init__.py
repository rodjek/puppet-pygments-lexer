from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *

# TODO
# regexp strings

class PuppetLexer(RegexLexer):
    name = 'Puppet'
    aliases = ['puppet']
    filenames = ['*.pp']

    tokens = {
        'root': [
            include('comments'),
            (r'(class)(\s+)([\w:]+)(\s+)(\{)', bygroups(Keyword.Declaration, Text, Name.Class, Text, Punctuation)),
            (r'(class|define)(\s+)([\w:]+)(\s*)(\()', bygroups(Keyword.Declaration, Text, Name.Class, Text, Punctuation), 'paramlist'),
            (r'if', Keyword.Reserved, 'conditional'),
            (r'(\})(\s*)(else)(\s*)(\{)', bygroups(Punctuation, Text, Keyword.Reserved, Text, Punctuation)),
            (r'(@{0,2}[\w:]+)(\s*)(\{)(\s*)', bygroups(Name.Class, Text, Punctuation, Text), ('type', 'namevar')),
            (r'\$(::)?(\w+::)*\w+', Name.Variable, 'var_assign'),
            (r'(include)(\s+)', bygroups(Keyword.Namespace, Text), 'include'),
            (r'\}', Punctuation),
            (r'\s', Text),
        ],
        'include': [
            (r'[\w:]+', Name.Class),
            include('value'),
            (r'', Text, '#pop'),
        ],
        'comments': [
            (r'\s*#.*\n', Comment.Singleline),
        ],
        'strings': [
            (r"'.*'", String.Single),
            (r'\w+', String.Symbol),
            (r'"', String.Double, 'dblstring'),
        ],
        'dblstring': [
            (r'\$\{.+?\}', String.Interpol),
            (r'(?:\\(?:[bdefnrstv\'"\$\\/]|[0-7][0-7]?[0-7]?|\^[a-zA-Z]))', String.Escape),
            (r'[^"\\\$]+', String.Double),
            (r'\$', String.Double),
            (r'"', String.Double, '#pop'),
        ],
        'variables': [
            (r'\$(::)?(\w+::)*\w+', Name.Variable),
        ],
        'var_assign': [
            include('value'),
            (r'(\s*)(=)(\s*)', bygroups(Text, Operator, Text)),
            (r'\s', Text, '#pop'),
            (r'', Text, '#pop'),
        ],
        'booleans': [
            (r'(true|false)', Literal),
        ],
        'operators': [
            (r'(==|\*|-|\+|<<|>>|!=|!|>=|<=|<|>|and|or|in)', Operator),
        ],
        'conditional': [
            include('value'),
            include('operators'),
            (r'\(', Punctuation, 'conditional'),
            (r'\{', Punctuation, '#pop'),
            (r'\)', Punctuation, '#pop'),
            (r'\s', Text),
        ],
        'namevar': [
            include('value'),
            (r'\[', Punctuation, 'array'),
            (r'\s', Text),
            (r':', Punctuation, '#pop'),
            (r'\}', Punctuation, '#pop'),
        ],
        'function': [
            (r'\[', Punctuation, 'array'),
            include('value'),
            (r',', Punctuation),
            (r'\s', Text),
            (r'\)', Punctuation, '#pop'),
        ],
        'paramlist': [
            include('value'),
            (r'=', Punctuation),
            (r',', Punctuation),
            (r'\s', Text),
            (r'(\))(\s*)(\{)', bygroups(Punctuation, Text, Punctuation), '#pop'),
        ],
        'type': [
            (r'(\w+)(\s*)(=>)(\s*)', bygroups(Name.Tag, Text, Punctuation, Text), 'param_value'),
            (r'\}', Punctuation, '#pop'),
            (r'\s', Text),
            (r'', Text, 'namevar'),
        ],
        'value': [
            (r'([A-Z]\w+)(\[)', bygroups(Name.Class, Punctuation), 'array'),
            (r'(\w+)(\()', bygroups(Name.Function, Punctuation), 'function'),
            include('strings'),
            include('variables'),
            include('comments'),
            include('booleans'),
        ],
        'param_value': [
            include('value'),
            (r'\[', Punctuation, 'array'),
            (r',', Punctuation, '#pop'),
            (r';', Punctuation, '#pop'),
        ],
        'array': [
            include('value'),
            (r',', Punctuation),
            (r'\s', Text),
            (r'\]', Punctuation, '#pop'),
        ],
    }
