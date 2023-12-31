# input -> token
def tokenizer(input):

    def add_token(type, value):
        nonlocal tokens
        tokens[-1]['line_tokens'].append({
            # 'loc': {
            #     'start': {
            #         'line': 0,
            #         'column': 0
            #     },
            #     'end': {
            #         'line': 0,
            #         'column': 0
            #     }
            # },
            'type': type,
            'value': value
        })

    def is_lc_letter(char):
        return ord('a') <= ord(char) <= ord('z')
    
    def is_uc_letter(char):
        return ord('A') <= ord(char) <= ord('Z')
    
    def is_digit(char):
        return ord('0') <= ord(char) <= ord('9')

    def is_id_start(char):
        return char == '_' or is_lc_letter(char) or is_uc_letter(char)
    
    def is_id_continue(char):
        return char == '_' or is_lc_letter(char) or is_uc_letter(char) or is_digit(char)
    
    def is_keyword(value):
        keywords = ["if", "eles", "while", "for", "continue", "break", "func", "return", "and", "or", "pass", "var"]
        return value in keywords

    def is_operator_part(char):
        operator_parts = ["+", "-", "*", "/", "%", "<", ">", "!", "=", "&", "|"]
        return char in operator_parts

    def is_operator(value):
        operators = ["+", "-", "*", "/", "%", "<", ">", "<=", ">=", "==", "!=", "=", "&&", "||"]
        return value in operators

    def is_delimiter(char):
        delimiters = ["(", ")", "[", "]", "{", "}", ",", ":", "."]
        return char in delimiters

    def is_whitespace(char):
        return char == ' ' or char == '\n'

    # initialization
    current = 0
    tokens = [{
        'line': 1,
        'indent': 0,
        'line_tokens': [],
    }]
    input += '\x1A' # add EOF char

    # for indent system
    indent_num = 0
    first_of_line = True

    # for loc marking
    line = 1
    column = 0

    # loop while input
    while current < len(input):
        char = input[current]

        # check whitespace
        if char == ' ':
            space_count = 0

            while char == ' ':
                space_count += 1
                current += 1
                char = input[current]

            if first_of_line:
                if indent_num == 0:
                    indent_num = space_count

                # indent validation
                if not space_count % indent_num == 0:
                    raise Exception('Indent Error')
                
                tokens[-1]['indent'] = space_count // indent_num
                # for _ in range(space_count // indent_num):
                #     add_token('delimiter', 'indent')

            # current += space_count
            continue
        else:
            first_of_line = False

        # check linebreak
        if char == '\n':
            # add_token('delimiter', 'EOL')
            tokens.append({
                'line': len(tokens)+1,
                'indent': 0,
                'line_tokens': [],
            })
            
            first_of_line = True
            current += 1
            continue

        # check EOF
        if char == '\x1A':
            # add_token('delimiter', 'EOF')
            break

        # check delimiter
        if is_delimiter(char):
            add_token('delimiter', char)
            
            current += 1
            continue
        
        # check operator
        if is_operator_part(char):
            value = ''
            next_char = ''
            
            if current < len(input) and is_operator_part(input[current+1]):
                next_char = input[current+1]
            value = char + next_char

            if is_operator(value):
                add_token('operator', value)
                current += len(value)
                continue
            elif is_operator_part(char):
                add_token('operator', char)
                current += 1
                continue
        
        # check string literal
        if char == '"' or char == "'":
            string_literal_delimiter = char

            value =''
            current += 1
            char = input[current]
            
            while char != string_literal_delimiter:
                value += char
                current += 1
                if not current < len(input):
                    break
                char = input[current]
            
            current += 1
            add_token('string_literal', value)
            continue
            
        # check number literal
        if is_digit(char):
            value = ''
            
            while is_digit(char):
                value += char
                current += 1
                if not current < len(input):
                    break
                char = input[current]

            add_token('number_literal', value)
            continue
            
        # check identifier, keyword
        if is_id_start(char):
            value = ''
            
            while is_id_continue(char):
                value += char
                current += 1
                if not current < len(input):
                    break
                char = input[current]
            
            # check keyword
            add_token('keyword' if is_keyword(value) else 'identifier', value)
            continue
    
    return tokens
        
# token -> AST
def parser(tokens):
    
    def Expression(tokens):
        
        current = 0
        while current < len(tokens):
            token = tokens[current]
            if token['type'] == 'operator' and token['value'] in ('='):
                node = {
                'type': 'AssignExpression',
                'op': token['value'],
                'left': Expression(tokens[0:current]),
                'right': Expression(tokens[current+1:]),
                }
                return node
            current += 1
            
        current = len(tokens)-1    
        while current >= 0:
            token = tokens[current]
            if token['type'] == 'operator' and token['value'] in ('>', '<', '>=', '<='):
                node = {
                'type': 'BinaryExpression',
                'op': token['value'],
                'left': Expression(tokens[0:current]),
                'right': Expression(tokens[current+1:]),
                }
                return node
            current -= 1
            
        current = len(tokens)-1
        while current >= 0:
            token = tokens[current]
            if token['type'] == 'operator' and token['value'] in ('+', '-'):
                # check UnaryExpr
                if current == 0 or (current-1 >= 0 and tokens[current-1]['type'] == 'operator'):
                    current -= 1
                    continue
                node = {
                'type': 'BinaryExpression',
                'op': token['value'],
                'left': Expression(tokens[0:current]),
                'right': Expression(tokens[current+1:]),
                }
                return node
            current -= 1
            
        current = len(tokens)-1
        while current >= 0:
            token = tokens[current]
            if token['type'] == 'operator' and token['value'] in ('*', '/', '%'):
                node = {
                'type': 'BinaryExpression',
                'op': token['value'],
                'left': Expression(tokens[0:current]),
                'right': Expression(tokens[current+1:]),
                }
                return node
            current -= 1
            
        current = 0
        while current < len(tokens):
            token = tokens[current]
            if token['type'] == 'operator' and token['value'] in ('+', '-'):
                node = {
                'type': 'UnaryExpression',
                'op': token['value'],
                'argument': Expression(tokens[current+1:]),
                }
                return node
            current += 1
        
        start = None
        end = None
        current = 0
        while current < len(tokens):
            token = tokens[current]
            # print(token)
            if token['type'] == 'delimiter' and token['value'] == '(':
                start = current
                break
            current += 1
        print(start)
        if start != None:
            current = len(tokens)-1
            while current >= 0:
                token = tokens[current]
                print(token, 'hi')
                if token['type'] == 'delimiter' and token['value'] == ')':
                    end = current
                    break
                current -= 1
            node = {
            'type': 'CallExpression',
            'callee': Expression(tokens[:start]),
            'arguments': Expression(tokens[start+1:end]),
            }
            
            print(start,end)
            return node
        
        if len(tokens) == 1 and (tokens[0]['type'] == 'number_literal' or tokens[0]['type'] == 'string_literal'):
            node = {
                'type': 'Literal',
                'value': tokens[0]['value'],
            }
            return node
            
        if len(tokens) == 1 and tokens[0]['type'] == 'identifier':
            node = {
                'type': 'Identifier',
                'name': tokens[0]['value'],
            }
            return node
        
        raise Exception("TypeError: Unknown expression")


    def walk():
        # nonlocal current
        current = 0

        token = line_tokens[current]
        # print(token) # ----test
        
        # # check string_literal
        # if token['type'] == 'string_literal':
        #     current += 1
        #     node = {
        #         'type': 'Literal',
        #         'value': token['value'],
        #     }
        #     return node

        # # check number_literal
        # if token['type'] == 'number_literal':
        #     current += 1
        #     node = {
        #         'type': 'Literal',
        #         'value': token['value'],
        #     }
        #     return node
        
        # # check identifier
        # if token['type'] == 'identifier':
        #     current += 1
        #     node = {
        #         'type': 'Identifier',
        #         'name': token['value']
        #     }
        #     return node

        # check keyword
        if token['type'] == 'keyword':
            # check VariableDecl
            if token['value'] == 'var':
                node = {
                    'type': 'VariableDeclaraion',
                    'declarations': Expression(line_tokens[1:])
                }
                current = len(line_tokens)
                return node
            
        return Expression(line_tokens)

                
                # lstart = None
                # lend = None
                # rstart = None
                # rend = None
                
                # current += 1
                # token = line_tokens[current]
                # while not (token['type'] == 'operator' and token['value'] == '='):
                #     token = line_tokens[current]
                #     current += 1
                

                # current += 1

                # while current < len(line_tokens):
                #     node['init'] = walk()

                # print(node)
                # return node
            
            # check FuncDecl

            # check ReturnStmt
            
            # check IfStmt

            # check ForStmt

        # # check operator
        # if token['type'] == 'operator':

        #     # 1st operator

        #     # call function (CallExpr)
        #     if token['value'] == '(':
        #         if current-1 >= 0 and line_tokens[current-1]['type'] == 'identifier':
        #             current -= 1
        #             callee = walk()

        #             current += 1
        #             arguments = []
        #             while not (line_tokens[current]['type'] == 'operator' and line_tokens[current]['value'] == ')'):
        #                 walk_recursion = walk()
        #                 arguments.append(walk())

        #             # node = {
        #             #     'type': 'CallExpression',
        #             #     'id': ,
        #             #     'arguments': walk(),
        #             # }
        #     # indexing (MemberExpr) ---- test 
        #     # reference (MemberExpr) ---- test

        #     # 2nd operator
        #     # + (unary)
        #     # - (unary)

        #     # 3rd operator
        #     # * (binary)
        #     # / (binary)
        #     # % (binary)

        #     # 4th operator
        #     # + (binary)
        #     # - (binary)

        #     # 5th operator
        #     # <
        #     # >
        #     # <=
        #     # >=

        #     # 6th operaotr
        #     # ==
        #     # !=

        #     # 7th operator
        #     # &&
        #     # ||

        #     # 8th operator
        #     # = (assign)

        #     # 9th operator
        #     # , (comma)

        # # check delimiter

        # # --------------- test
        # # check identifier
        
        #     # check PriamaryExpr

        #     # check BinaryExpr

        #     # check AssignExpr

        #     # check CallExpr

        # # check operator

        # # raise TypeError
        raise Exception("TypeError: Unknown Token")

    current = 0
    ast = {
        'type': 'Program',
        'body': [],
    }

    for data in tokens:
        line_tokens = data['line_tokens']
        # current = 0
        # while current < len(line_tokens):
        #     ast['body'].append(walk())
        if len(line_tokens) == 0:
            continue
        ast['body'].append(walk())

    return ast

def test():
#     input = \
# '''
# def foo(a, b='hi'):
#     print(a, b)
#     return b + ' guys'

# def boo():
#     for i in range(3):
#         print('hihi')

# foo()
# if True:
#     boo()
# '''

#     input = """
# var ahi 'hi' '"dds"' 33 
# 00 'hello'

# 'kk'
#     '..??'
#     010100 'dd'
# """

#     input = """
# var a = 1 + 1 * 2 / 4 + 2 / 1
# a = 0
# print(a + 9 / 2)
# 'plz..'
# """
    input = """
print(a+1)    
"""

    tokens = tokenizer(input)

    # print tokens
    for data in tokens:
        for token in data['line_tokens']:
            print('\t'.join([str(data['line']), str(data['indent']), token['type'], token['value']]))

    ast = parser(tokens)

    # print ast 
    print('\n',ast)

if __name__ == '__main__':
    test()
