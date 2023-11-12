# input -> token
def tokenizer(input):

    def add_tokens(type, value):
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
    
    def is_identifier(char):
        nonlocal current
        if is_id_start(char):
            value = ''
            
            while is_id_continue(char):
                value += char
                current += 1
                if not current < len(input):
                    break
                char = input[current]
            
            # check value is keyword
            if is_keyword(value):    
                tokens.append({
                    'type': 'keyword',
                    'value': value
                })
            else:
                tokens.append({
                'type': 'identifier',
                'value': value
            })

    def is_id_start(char):
        return char == '_' or is_lc_letter(char) or is_uc_letter(char)
    
    def is_id_continue(char):
        return char == '_' or is_lc_letter(char) or is_uc_letter(char) or is_digit(char)
    
    def is_keyword(value):
        keywords = ["if", "eles", "while", "for", "continue", "break", "func", "return", "and", "or", "pass"]
        return value in keywords
        if not is_string_literal(char):
            is_number_literal(char)

    def is_string_literal(char):
        return char == '"'

    def is_number_literal(char):
        return is_digit(char)
        return
        if is_digit(char):
            value = ''
            while is_digit(char):
                value += char
                current += 1
                char = input[current]

            tokens.apppend({
                    'type': 'number_literal',
                    'value': value
                })
            return True
        return False

    def is_operator(char):
        nonlocal current
        operators = ["+", "-", "*", "/", "%", "<", ">", "<=", ">=", "==", "!=", "="]
        return value in operators
        value = ''
        next_char = ''
        
        # second char of operator is always "="
        if current < len(input) and input[current+1] == '=':
            next_char = '='
            
        value = char + next_char
        return value in operators

    def is_delimiter(char):
        delimiters = ["(", ")", "[", "]", "{", "}", ",", ".", "\t"]
        return char in delimiters

    def is_whitespace(char):
        return char == ' ' or char == '\n'

    # initialization
    current = 0
    tokens = []

    # loop while input
    while current < len(input):
        char = input[current]

        # check whitespace
        if is_whitespace(char):
            current += 1
            continue
        
        # check delimiter
        if is_delimiter(char):
            add_tokens('delimiter', char)
            
            current += 1
            continue
        
        # check operator
        # if is_operator(char):
        value = ''
        next_char = ''
        
        # second char of operator is always "="
        if current < len(input) and input[current+1] == '=':
            next_char = '='
            
        value = char + next_char
        add_tokens('operator', value)
        current += len(value)
        
        # check string literal
        if is_string_literal(char):
            value =''
            current += 1
            char = input[current]
            
            while char != '"':
                value += char
                current += 1
                if not current < len(input):
                    break
                char = input[current]
            
            current += 1
            add_tokens('string_literal', value)
            
        # check number literal
        if is_number_literal(char):
            value = ''
            
            while is_digit(char):
                value += char
                current += 1
                if not current < len(input):
                    break
                char = input[current]

            add_tokens('number_literal', value)
            
        # check identifier, keyword
        if is_identifier(char):
            if is_id_start(char):
                value = ''
                
                while is_id_continue(char):
                    value += char
                    current += 1
                    if not current < len(input):
                        break
                    char = input[current]
                
                # check keyword
                add_tokens('keyword' if is_keyword(value) else 'identifier', value)
        
        

def parser(tokens):
    pass

input = 'hi'
tokens = tokenizer(input)
ast = parser(parser)
print(tokens)
