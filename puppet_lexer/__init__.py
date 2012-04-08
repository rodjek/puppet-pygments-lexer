from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *

class PuppetLexer(RegexLexer):
    name = 'Puppet'
    aliases = ['puppet']
    filenames = ['*.pp']

    tokens = {
        'root': [
            include('puppet'),
        ],
        'puppet': [
            include('comments'),
            (r'(class)(\s+)([\w:]+)(\s+)(\{)', bygroups(Keyword.Declaration, Text, Name.Class, Text, Punctuation), 'block'),
            (r'(class|define)(\s+)([\w:]+)(\s*)(\()', bygroups(Keyword.Declaration, Text, Name.Class, Text, Punctuation), ('block','paramlist')),
            (r'node', Keyword.Declaration, ('block', 'node_name')),
            (r'elsif', Keyword.Reserved, ('block', 'conditional')),
            (r'if', Keyword.Reserved, ('block', 'conditional')),
            (r'unless', Keyword.Reserved, ('block', 'conditional')),
            (r'(else)(\s*)(\{)', bygroups(Keyword.Reserved, Text, Punctuation), 'block'),
            (r'case', Keyword.Reserved, ('case', 'conditional')),
            (r'(@{0,2}[\w:]+)(\s*)(\{)(\s*)', bygroups(Name.Class, Text, Punctuation, Text), ('type', 'namevar')),
            (r'\$(::)?(\w+::)*\w+', Name.Variable, 'var_assign'),
            (r'(include)(\s+)', bygroups(Keyword.Namespace, Text), 'include'),
            (r'import', Keyword.Namespace, 'import'),
            (r'(\w+)(\()', bygroups(Name.Function, Punctuation), 'function'),
            (r'\s', Text),
        ],
        'block': [
            include('puppet'),
            (r'\}', Text, '#pop'),
        ],
        'node_name': [
            (r'inherits', Keyword.Declaration),
            (r'[\w\.]+', String),
            include('strings'),
            include('variables'),
            (r',', Punctuation),
            (r'\s', Text),
            (r'\{', Punctuation, '#pop'),
        ],
        'include': [
            (r'[\w:]+', Name.Class),
            include('value'),
            (r'', Text, '#pop'),
        ],
        'import': [
            (r'[\/\w\.]+', String),
            include('value'),
            (r'\s', Text),
            (r'', Text, '#pop'),
        ],
        'case': [
            (r'(default)(:)(\s*)(\{)', bygroups(Keyword.Reserved, Punctuation, Text, Punctuation), 'block'),
            include('case_values'),
            (r'(:)(\s*)(\{)', bygroups(Punctuation, Text, Punctuation), 'block'),
            (r'\s', Text),
            (r'\}', Punctuation, '#pop'),
        ],
        'case_values': [
            include('value'),
            (r',', Punctuation),
        ],
        'comments': [
            (r'\s*#.*\n', Comment.Singleline),
        ],
        'strings': [
            (r"'.*?'", String.Single),
            (r'\w+', String.Symbol),
            (r'"', String.Double, 'dblstring'),
            (r'\/.+?\/', String.Regex),
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
            (r'\[', Punctuation, 'array'),
            (r'(\s*)(=)(\s*)', bygroups(Text, Operator, Text)),
            (r'\s', Text, '#pop'),
            (r'', Text, '#pop'),
        ],
        'booleans': [
            (r'(true|false)', Literal),
        ],
        'operators': [
            (r'(==|=~|\*|-|\+|<<|>>|!=|!~|!|>=|<=|<|>|and|or|in)', Operator),
        ],
        'conditional': [
            include('operators'),
            include('strings'),
            include('variables'),
            (r'\[', Punctuation, 'array'),
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
            (r'([A-Z][\w:]+)+(\[)', bygroups(Name.Class, Punctuation), 'array'),
            (r'(\w+)(\()', bygroups(Name.Function, Punctuation), 'function'),
            include('strings'),
            include('variables'),
            include('comments'),
            include('booleans'),
            (r'(\s*)(\?)(\s*)(\{)', bygroups(Text, Punctuation, Text, Punctuation), 'selector'),
            (r'\{', Punctuation, 'hash'),
        ],
        'selector': [
            (r'default', Keyword.Reserved),
            include('value'),
            (r'=>', Punctuation),
            (r',', Punctuation),
            (r'\s', Text),
            (r'\}', Punctuation, '#pop'),
        ],
        'param_value': [
            include('value'),
            (r'\[', Punctuation, 'array'),
            (r',', Punctuation, '#pop'),
            (r';', Punctuation, '#pop'),
            (r'\s', Text, '#pop'),
            (r'', Text, '#pop'),
        ],
        'array': [
            include('value'),
            (r'\[', Punctuation, 'array'),
            (r',', Punctuation),
            (r'\s', Text),
            (r'\]', Punctuation, '#pop'),
        ],
        'hash': [
            include('value'),
            (r'\s', Text),
            (r'=>', Punctuation),
            (r',', Punctuation),
            (r'\}', Punctuation, '#pop'),
        ],
    }
