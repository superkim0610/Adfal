import compiler

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


# def AssignExpression(tokens):
#     root, remains = BinaryExpression(tokens)
#     if remains[0]['type'] == 'operator' and remains[0]['value'] in ('='):
#         op, remains = remains[0], remains[1:]
#         node = {
#             'type': 'AssignExpression',
#             'op': op,
#             'left': root,
#             'right': BinaryExpression(remains),
#         }
#         return node
#     return BinaryExpression(tokens)


# def BinaryExpression(tokens):
#     root, remains = UnaryExpression(tokens)
#     if remains[0]['type'] == 'operator' and remains[0]['value'] in ('+'):
#         op, remains = remains[0], remains[1:]
#         node = {
#             'type': 'BinaryExpression',
#             'op': op,
#             'left': root,
#             'right': UnaryExpression(remains),
#         }
#         return node
#     return BinaryExpression(tokens)

# def UnaryExpression(tokens):
#     if tokens[0]['type'] == 'operator' and tokens[0]['value'] in ('+'):
#         op, remains = tokens[0], tokens[1:]
#         node = {
#             'type': 'UnaryExpression',
#             'op': op,
#             'argument': PrimaryExpression(remains)
#         }
#         return node

# def MemberExpression(tokens):
#     pass

# def CallExpression(tokens):
#     pass

# def PrimaryExpression(tokens):
#     if tokens[0]['type'] == 'identifier' or tokens[0]['type'] == 'number_literal':
#         node = {
#             'type': tokens[0]['type'],
#             'value': tokens[0]['value'],
#         }
#         return node

print(tokens := compiler.tokenizer('a2 = -1 - +2 + -3')[0]['line_tokens'],'\n')
print(Expression(tokens))