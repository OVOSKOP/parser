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
    (r'<!--.*(?=-->)-->',                                     None),
    (r'<script( )?([-\w ]+="[^>]*(?=")")*(( )?/)?>',         SCRIPT),
    (r'<style( )?([-\w ]+="[^>]*(?=")")*(( )?/)?>',          STYLE),
    (r'<\/[\w-]*>',                                           CLOSE_TAG),
    (r'<!DOCTYPE [ \w.:\/\-\"]+>',                     TYPE),
    (r'(([^<>\s])|( ))+',                                     CONTENT),
    (r'<(area|base|br|col|command|embed|hr|img|input|keygen|link|meta|param|' +
    'source|track|wbr)( )?([:a-zA-Z- ]+="[^>]*(?=")")*(( )?/)?>', TAG),
    (r'<([\w-]+)( )?([-\w: ]+="[^>]*(?=")")*(( )?/)?>',       OPEN_TAG),    
]

token_tag = [
	[
		(r'[\s<>/]+',           None),
		(r'[\w:-]+="[^"]*(?=")"', ATRIBUTE),
    	(r'[\w-]+',             TAG_NAME),
    ],
    [
    	(r'[\s=]+',     None),
		(r'[\w:-]+(?==")', ATRIBUTE_NAME),
    	(r'"(?<=")[^"]*(?=")"',     VALUE),
    ],
]

def imp_lex(characters):
    return lexer.lex(characters, token_exprs, token_tag)

# ([('body', 'TAG_NAME')], 'CLOSE_TAG')
# ([('html', 'TAG_NAME')], 'CLOSE_TAG')