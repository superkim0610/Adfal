# input -> token
def tokenizer(input):

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

    def is_literal(char):
        if not is_string_literal(char):
            is_number_literal(char)

    def is_string_literal(char):
        if char == '"':
            value =''
            current += 1
            char = input[current]
            while char != '"':
                value += char
                current += 1
                char = input[current]
            
            current += 1
            char = input[current]
            tokens.append({
                'type': 'string_literal',
                'value': value
            })
            return True
        return False

    def is_number_literal(char):
        return is_integer(char)

    def is_integer(char):
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
        operators = ["+", "-", "*", "/", "%", "<", ">", "<=", ">=", "==", "!="]
        value = ''
        next_char = input[current+1]
        if next_char == ' ':
            value = char
            current += 1
        else:
            value = char + next_char
            current += 2
        return value in operators

    def is_delimiter(char):
        delimiters = ["(", ")", "[", "]", "{", "}", ",", ".", "\t"]
        return char in delimiters

    # initialization
    current = 0
    tokens = []

    # loop while input
    while current < len(input):
        char = input[current]

        # identifier
        if is_identifier(char):
            pass
        elif is_literal(char):
            pass
        elif is_operator(char):
            pass
        elif is_delimiter(char):
            pass
        

def parser(tokens):
    pass

input = 'hi'
tokens = tokenizer(input)
ast = parser(parser)
print(tokens)
