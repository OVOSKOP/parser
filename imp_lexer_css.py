import lexer

NAME           = 'NAME'
ITEM           = 'ITEM'
VALUE          = 'VALUE'

token_exprs = [
    (r'[ \n\t}]+',        None),
    (r'(/\*)[^$]*(\*/)',  None),
    (r'([\w]+|\*)( )*({)',NAME),
	(r'[\w]+( )*(:)( )?', ITEM),
	(r'[\w]+(;)?',        VALUE),
      
]

def imp_lex_css(characters):
    return lexer.lex(characters, token_exprs)