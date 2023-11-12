import compiler

def AssignExpression(tokens):
    root, remains = BinaryExpression(tokens)
    if remains[0]['type'] == 'operator' and remains[0]['value'] in ('='):
        op, remains = remains[0], remains[1:]
        node = {
            'type': 'AssignExpression',
            'op': op,
            'left': root,
            'right': BinaryExpression(remains),
        }
        return node
    return BinaryExpression(tokens)


def BinaryExpression(tokens):
    root, remains = UnaryExpression(tokens)
    if remains[0]['type'] == 'operator' and remains[0]['value'] in ('+'):
        op, remains = remains[0], remains[1:]
        node = {
            'type': 'BinaryExpression',
            'op': op,
            'left': root,
            'right': UnaryExpression(remains),
        }
        return node
    return BinaryExpression(tokens)

def UnaryExpression(tokens):
    if tokens[0]['type'] == 'operator' and tokens[0]['value'] in ('+'):
        op, remains = tokens[0], tokens[1:]
        node = {
            'type': 'UnaryExpression',
            'op': op,
            'argument': PrimaryExpression(remains)
        }
        return node

def MemberExpression(tokens):
    pass

def CallExpression(tokens):
    pass

def PrimaryExpression(tokens):
    if tokens[0]['type'] == 'identifier' or tokens[0]['type'] == 'number_literal':
        node = {
            'type': tokens[0]['type'],
            'value': tokens[0]['value'],
        }
        return node

print(tokens := compiler.tokenizer('a = 1')[0]['line_tokens'])
print(AssignExpression(tokens))