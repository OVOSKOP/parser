import lexer

NAME           = 'NAME'
STYLE          = 'STYLE'
VALUE          = 'VALUE'

token_exprs = [
    (r'[ \n\t}]+',        None),
    (r'(/\*)[^$]*(\*/)',  None),
    (r'([\w]+|\*)( )*({)',     NAME),
	(r'[\w]+( )*(:)( )?', STYLE),
	(r'[\w]+(;)?',        VALUE),
      
]

def imp_lex_css(characters):
    return lexer.lex(characters, token_exprs)