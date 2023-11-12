# input -> token
def tokenizer(input):

    def add_token(type, value):
        nonlocal tokens
        tokens.append({
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
        keywords = ["if", "eles", "while", "for", "continue", "break", "func", "return", "and", "or", "pass"]
        return value in keywords

    def is_operator_part(char):
        operator_parts = ["+", "-", "*", "/", "%", "<", ">", "!", "="]
        return char in operator_parts

    def is_operator(value):
        operators = ["+", "-", "*", "/", "%", "<", ">", "<=", ">=", "==", "!=", "="]
        return value in operators

    def is_delimiter(char):
        delimiters = ["(", ")", "[", "]", "{", "}", ",", ":", "."]
        return char in delimiters

    def is_whitespace(char):
        return char == ' ' or char == '\n'

    # initialization
    current = 0
    tokens = []
    indent_num = 0 # for indent system
    first_of_line = True

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
                
                for _ in range(space_count // indent_num):
                    add_token('delimiter', 'indent')

            # current += space_count
            continue
        else:
            first_of_line = False

        if char == '\n':
            add_token('delimiter', 'EOL')
            first_of_line = True
            current += 1
            continue
        
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
        
def parser(tokens):
    pass

input = '''
def foo(a, b='hi'):
    print(a, b)
    return b + ' guys'

def boo():
    for i in range(3):
        print('hihi')

foo()
if True:
    boo()
'''

tokens = tokenizer(input)
ast = parser(parser)
print(tokens)
for token in tokens:
    print(token['type'], '\t', token['value'])
