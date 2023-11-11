def tokenizer(input):
    current = 0
    tokens = []

    while current < len(input):
        char = input[current]

        # lparen
        if char == '(':
            tokens.append({
                'type': 'paren',
                'value': '(',
            })
            current += 1
            continue

        # rparen
        if char == ')':
            tokens.append({
                'type': 'paren',
                'value': ')',
            })
            current += 1
            continue

        # whitespace
        if char == ' ':
            current += 1
            continue
        
        # number
        if ord('0') <= ord(char) <= ord('9'):
            value = ''

            while ord('0') <= ord(char) <= ord('9'):
                value += char
                current += 1
                char = input[current]

            tokens.append({
                'type': 'number',
                'value': value,
            })
            continue

        # string
        if char == '"':
            value = ''

            current += 1
            char = input[current]

            while char != '"':
                value += char
                current += 1
                char = input[current]

            current += 1
            char = input[current]
            tokens.append({
                'type': 'string',
                'value': value,
            })
            continue

        if ord('a') <= ord(char) <= ord('z') or ord('A') <= ord(char) <= ord('Z'):
            value = ''

            while ord('a') <= ord(char) <= ord('z') or ord('A') <= ord(char) <= ord('Z'):
                value += char
                current += 1
                char = input[current]

            tokens.append({
                'type': 'name',
                'value': value,
            })
            continue

        raise Exception('TypeError: Unknown character in tokenizing : ' + char)

    return tokens

def parser(tokens):
    global current
    current = 0

    def walk():
        global current
        token = tokens[current]

        # NumberLiteral
        if token['type'] == 'number':
            current += 1

            return {
                'type': 'NumberLiteral',
                'value': token['value'],
            }
        
        # StringLiteral
        if token['type'] == 'string':
            current += 1

            return { 
                'type': 'StringLiteral',
                'value': token['value'],
            }
        
        if token['type'] == 'paren' and token['value'] == '(':
            current += 1
            token = tokens[current]

            node = {
                'type': 'CallExpression',
                'name': token['value'],
                'params': [],
            }

            current += 1
            token = tokens[current]

            while token['type'] != 'paren' or (token['type'] == 'paren' and token['value'] != ')'):
                node['params'].append(walk())
                token = tokens[current]

            current += 1
            return node
        
        raise Exception('TypeError: Unknown token : ' + token['value'])

    ast = {
        'type': 'Program',
        'body': [],
    }

    while current < len(tokens):
        print(ast['body'])
        ast['body'].append(walk())

    return ast

# ---- test -----
input = '''(add 4 2)'''
tokens = tokenizer(input)
for token in tokens:
    print(token)
# print(parser(tokens))