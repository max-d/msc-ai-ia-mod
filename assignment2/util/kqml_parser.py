class KQMLParser:
    def get_action(self, message: str):
        # taking message = (ask: (record-exists ?sample [1,2,3]))
        tokens = message[1:-1].split() # tokens are ['ask:', '(record-exists', '?sample', '[1,2,3])']
        action = tokens[0][:-1] # tokens[0] = 'ask:' and 'ask:'[:-1] = 'ask', that is the action.
        return action

    def get_condition(self, message: str):
        # taking message = (ask: (record-exists ?sample [1,2,3]))
        tokens = message[1:-1].split() # tokens are ['ask:', '(record-exists', '?sample', '[1,2,3])']
        condition = tokens[1][1:] # tokens[1] = '(record-exists' and ''(record-exists''[1:] = 'record-exists', that is the condition.
        return condition

    def get_criteria(self, message: str):
        # taking message = (ask: (record-exists ?sample [1,2,3]))
        tokens = message[1:-1].split() # tokens are ['ask:', '(record-exists', '?sample', '[1,2,3])']
        criteria = tokens[2] # criteria is '?sample'
        return criteria

    def get_comparer(self, message: str, separator: str = ""):
        # taking message = (ask: (record-exists ?sample [1,2,3])) and separator = 'sample'
        tokens = message[1:-1].split(separator) # tokens are ['ask: (record-exists ?', '[1,2,3])']
        comparer = tokens[1][1:-1] # tokens[1] = '[1,2,3])' and '[1,2,3])'[1:-1] = [1,2,3]
        return comparer