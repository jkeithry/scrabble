import string, math, collections

# import words
minlen = 4
maxlen = 30

sep = '-'

letter_values = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2,
    'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1,
    'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

letters = list(string.ascii_lowercase)


def word_tree(word):
    pass


def author():
    name = 'Keith, Jeffrey'
    return name


def student_id():
    stud_id = 500804619
    return stud_id


def consistent(pattern, assignment, min_len):
    curr = ''
    for pos in range(0, len(pattern)):
        if pattern[pos] != sep and assignment[pos] != pattern[pos]:
            return False
        ch = assignment[pos]
        if ch == '-' or pos == len(pattern):
            if len(curr) == 1:
                break
            if len(curr) < min_len or curr not in wordset:
                return False
            curr = ''
        else:
            curr += ch
    return True


def path_consistency(pattern):
    # edges = [ position, value, position+1, value ]
    edges = [[x, pattern[x], x + 1, pattern[x + 1]] for x in range(0, len(pattern) - 1)]
    # the possible domains of variables d= position of variable in assignment

    # domains of each var
    domains = {d: list(string.ascii_lowercase) for d in range(0, len(pattern)) if pattern[d] == '-'}

    for x in range(len(pattern)):
        if pattern[x] != sep:
            domains[x] = pattern[x]
    queue = collections.deque(edges)

    while len(queue) != 0:
        this_edge = queue.pop()
        variable_i = this_edge[0]
        if _revise(pattern, this_edge, domains):
            # add neighbor edge of variable which is not the one we against checked(X_j)
            if this_edge[0] > 0:
                neighbor_edge = [
                    this_edge[0] - 1,
                    pattern[this_edge[0] - 1],
                    this_edge[0],
                    this_edge[1]
                ]
                queue.append(neighbor_edge)

    return domains


def _revise(pattern, edge, domains):
    variable_i = edge[0]
    variable_m = edge[2]
    variable_j = variable_m + 1
    revised = False

    if variable_j >= len(pattern):
        return False

    domain_i = domains[variable_i]
    domain_m = domains[variable_m]
    domain_j = domains[variable_j]

    if pattern[variable_i] == pattern[variable_m] == pattern[variable_j] == sep:
        revised = False
        return revised

    else:
        for letter_m in domain_m:
            for letter_i in domain_i:
                for letter_j in domain_j:
                    path = letter_i + letter_m + letter_j
                    valid = False
                    for word in wordset:
                        if path in word:
                            valid = True
                            break
                        else:
                            continue
                if not valid:
                    try:
                        domain_i.remove(letter_i)
                    except ValueError:
                        pass
                    except AttributeError:
                        pass

                    try:
                        domain_j.remove(letter_j)
                    except ValueError:
                        pass
                    except AttributeError:
                        pass

                    domains[variable_i] = domain_i

                    domains[variable_j] = domain_j

                    revised = True
    return revised


def partial_consistent(pattern, assignment):
    curr = ''
    if assignment == pattern:
        return True
    for pos in range(0, len(assignment)):
        ch = assignment[pos]
        valid = False
        if ch == '-' or pos == len(assignment):
            for word in wordset:
                if curr in word:
                    curr_idx = word.find(curr)
                    curr_start = pos - len(curr)
                    space_to_end = len(pattern) - curr_idx
                    if curr_idx <= curr_start and len(word) < space_to_end:
                        valid = True
                        break

            if valid:
                curr = ''
            else:
                return False
        else:
            curr += ch
    return True



def order_domain_values(domain):
    """:returns a queue of letters with highest value to create a word"""
    ordered_domain = domain

    for i in range(len(domain)):
        max_idx = i
        i_value = letter_values.get(domain[i])
        for j in range(i + 1, len(domain)):
            j_value = letter_values.get(domain[j])
            if j_value > i_value:
                max_idx = j
        temp = domain[i]
        domain[i] = domain[max_idx]
        domain[max_idx] = temp
    return ordered_domain


def assignment_complete(pattern):



def backtrack(pattern, assignment, variable, domains, min_len):
    if assignment_complete(pattern):
       return assignment

    for value in domains:
        if variable >= len(pattern):
            break
        if pattern[variable] != sep:
            variable += 1
        new_assignment = assignment[:variable] + value + assignment[variable + 1:]
        old_pat = pattern
        if partial_consistent(pattern, new_assignment):
            assignment = new_assignment
            pattern = new_assignment
            result = backtrack(pattern, assignment, variable + 1, domains, min_len)
            if consistent(pattern, result, min_len):
                return result
            else:
                pattern = old_pat
        else:
            assignment = assignment[:variable] + sep + assignment[variable + 1:]

    return pattern


def backtrack_search(pattern, min_len):
    solution = pattern
    var = 0
    domains = order_domain_values(letters)
    # domains = path_consistency(pattern)
    # for domain in domains:
    #     try:
    #         order_domain_values(domains[domain])
    #     except AttributeError:
    #         pass
    #     except TypeError:
    #         pass
    return backtrack(pattern, solution, var, domains, min_len)



def fill_words(pattern, words, scoring_f, min_len, max_len):
    """Maximize score of the pattern by inserting words in pattern

    pattern -- the pattern to solve

    words   -- words from the dictionary

    scoring_f   -- (word x of length k)  =  k*k + sum(letter points of x)

    min_len -- minimum length word

    max_len -- maximum length word

    Returns the pattern with the words filled in
    """
    global wordset
    wordset = set(words)

    solution = backtrack_search(pattern, min_len)

    return solution



def select_unassigned_variable(pattern, assignment):
    """
    Use degree heuristic at first to find the variable involved with the most
    constraint on other variables to prune.

    then uses minimum remaining values to selected variable
    """
    blanks_in_row = 0
    max_len_blanks = 0
    pos = 0

    for x in range(0, len(assignment)):

        if assignment[x] == '-':
            blanks_in_row += 1

            if blanks_in_row > max_len_blanks:
                max_len_blanks = blanks_in_row
                pos = x - (max_len_blanks - 1) + max_len_blanks / 2
        else:
            blanks_in_row = 0

    variable = math.floor(pos)

    return variable
