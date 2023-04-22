from collections import defaultdict




knowledge_base = defaultdict(list)

def parse_prolog_file(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces

            if not line or line.startswith('%'):
                # Skip empty lines and comments
                continue

            words = line.split()
            if ':-' in words:
                # Parse rules
                head = words[0]
                body = words[2:]
                knowledge_base[head].append(body)
            else:
                # Parse facts
                predicate = words[0]
                arguments = words[1:]
                knowledge_base[predicate].append(arguments)


# Function to evaluate queries and perform substitution
def evaluate_query(query):
    answers = []
    if query in knowledge_base:
        for arguments in knowledge_base[query]:
            answers.append(','.join(arguments))
    elif query.endswith(')') and '(' in query:
        predicate, arguments = query.split('(', 1)
        if not predicate:
            # Handle case where query has no predicate
            return answers
        arguments = arguments[:-1].split(',')
        if len(arguments) == 1 and arguments[0] == '':
            # Handle case where query has no arguments
            arguments = []
        if len(arguments) >= 2:
            for rule in knowledge_base[predicate]:
                substitution = {}
                for i, arg in enumerate(arguments):
                    if arg.startswith('_'):
                        # Skip anonymous variables
                        continue
                    if arg not in substitution:
                        substitution[arg] = arguments[i]
                    elif substitution[arg] != arguments[i]:
                        # If there is a conflict in substitution, skip this rule
                        break
                else:
                    # If all arguments can be substituted, evaluate the rule
                    for sub_query in rule:
                        answers.extend(evaluate_query(sub_query))
    return answers



def forward_reasoning(kb, query):
    global knowledge_base
    knowledge_base = kb
    return evaluate_query(query)


if __name__ == '__main__':
    file_path = 'KBEngland.pl'
    parse_prolog_file(file_path)
    query = 'married(prince_phillip,queen_elizabeth_II)'
    answers = forward_reasoning(knowledge_base, query)
    if answers:
        print(
            f'The system inferred the following answers for the query "{query}":')
        for answer in answers:
            print(answer)
    else:
        print(
            f'The system could not infer any answer for the query "{query}" based on existing knowledge.')
    print("Inferred Knowledge Base:")
    for predicate, arguments in knowledge_base.items():
        # print(predicate + ":")
        for arg in arguments:
            print(", ".join(arg))

