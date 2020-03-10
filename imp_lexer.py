import lexer

TAG           = 'TAG'
OPEN_TAG      = 'OPEN_TAG'
CLOSE_TAG     = 'CLOSE_TAG'
TYPE          = 'TYPE'
CONTENT       = 'CONTENT'
SCRIPT        = 'SCRIPT'
STYLE         = 'STYLE'

TAG_NAME      = 'TAG_NAME'
ATRIBUTE      = 'ATRIBUTE'
ATRIBUTE_NAME = 'ATRIBUTE_NAME'
VALUE         = 'VALUE'

token_exprs = [
    (r'[ \n\t]+',                                             None),
    (r'<!--[^$]*-->',                                         None),
    (r'<script( )?([-a-zA-Z ]+="([^"])*")*(( )?/)?>',         SCRIPT),
    (r'<style( )?([-a-zA-Z ]+="([^"])*")*(( )?/)?>',          STYLE),
    (r'<\/[a-zA-Z0-9]*>',                                     CLOSE_TAG),
    (r'<!DOCTYPE [ a-zA-Z0-9.:\/\-\"]+>',                     TYPE),
    (r'[^<>\s]+',                                             CONTENT),
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
    # [
    #     (r'[ \n\t]+',                                             None),
    #     (r'<\/(script|style)>',                                     None),
    #     (r'<(script|style)( )?([-a-zA-Z ]+="([^"])*")*(( )?/)?>', None), 
    #     (r'(([\s\w\W]))+',                                               CONTENT),
    # ]
]

def imp_lex(characters):
    return lexer.lex(characters, token_exprs, token_tag)

# ([('body', 'TAG_NAME')], 'CLOSE_TAG')
# ([('html', 'TAG_NAME')], 'CLOSE_TAG')