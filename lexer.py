import sys
import re

def lex(characters, token_exprs, sub_token_exprs=None):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            #print(token_exprs)
            #print()
            pattern, tag = token_expr
            #print('pattern' + pattern)
            # print('pos = ' + str(pos), 'char ' + characters[pos])
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                #print('match' + match)
                text = match.group(0)
                if tag:
                    if (tag == "TAG" or tag == "CLOSE_TAG" or tag == "OPEN_TAG") and sub_token_exprs:
                        text = lex(text, sub_token_exprs[0], sub_token_exprs)
                    if tag == "ATRIBUTE" and sub_token_exprs:
                        text = lex(text, sub_token_exprs[1], sub_token_exprs)
                    if tag == "SCRIPT" and sub_token_exprs:
                        text = lex(text, sub_token_exprs[2], sub_token_exprs)

                    token = (text, tag)
                    # print('tag ' + tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: "%s" ' % (characters[pos] + characters[pos + 1] + characters[pos + 2] + characters[pos + 3]) + 'in pos: %s\n' % str(pos))
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens
