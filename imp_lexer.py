import lexer

TAG           = 'TAG'
OPEN_TAG      = 'OPEN_TAG'
CLOSE_TAG     = 'CLOSE_TAG'
TYPE          = 'TYPE'
CONTENT       = 'CONTENT'
SCRIPT        = 'SCRIPT'

TAG_NAME      = 'TAG_NAME'
ATRIBUTE      = 'ATRIBUTE'
ATRIBUTE_NAME = 'ATRIBUTE_NAME'
VALUE         = 'VALUE'

token_exprs = [
    (r'[ \n\t]+',                                             None),
    (r'<!--[^$]*-->',                                         None),
    (r'<script>[\w\W]*</script>',                             SCRIPT),
    (r'<\/[a-zA-Z0-9]*>',                                     CLOSE_TAG),
    (r'<!DOCTYPE [ a-zA-Z0-9.:\/\-\"]+>',                     TYPE),
    (r'[^<>]+',                                               CONTENT),
    (r'<(area|base|br|col|command|embed|hr|img|input|keygen|link|meta|param|' +
    'source|track|wbr)( )?([-a-zA-Z ]+="([^"])*")*(( )?/)?>', TAG),
    (r'<([a-zA-Z0-9]+)( )?([-a-zA-Z ]+="([^"])*")*(( )?/)?>', OPEN_TAG),    
]

token_tag = [
	[
		(r'[\s<>/]+',             None),
		(r'[a-zA-Z-]+="[^"\n]*"', ATRIBUTE),
    	(r'[\w]+',                TAG_NAME),
    ],
    [
    	(r'[\s=/]+',    None),
		(r'[a-zA-Z-]+', ATRIBUTE_NAME),
    	(r'"[^"\n]*"',  VALUE),
    ],
    [
        (r'<\/[a-zA-Z0-9]*>',                                     CLOSE_TAG),
        (r'<([a-zA-Z0-9]+)( )?([-a-zA-Z ]+="([^"])*")*(( )?/)?>', OPEN_TAG), 
        (r'[\w\W]+',                                               CONTENT),
    ]
]

def imp_lex(characters):
    return lexer.lex(characters, token_exprs, token_tag)

# ([('body', 'TAG_NAME')], 'CLOSE_TAG')
# ([('html', 'TAG_NAME')], 'CLOSE_TAG')