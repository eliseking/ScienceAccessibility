

import inspect
import types
import pandas as pd
import inspect, radon, pprint
from radon.complexity import cc_rank, cc_visit
class CodeComplexity(object):
    def __init__(self):
        pass
def ccomplexity_rater(other_function):
    '''
    This function calculates the radian cyclomatic complexity of other functions.
    Radian complexity is used as a proxy for cognitive complexity, ie how hard is a code block to understand.
    Inputs: Other Python functions.
    Outputs: A positive integer value that is located in the interval 1-41. The scalar is used in conjunction
    with a printed legend.

    The program first uses introspection to convert other_function to a string representation of the
    source code that the function was originally expressed in.
    Subsequently another module radon that calculates cognitive complexity is called.
    Dependencies: If the radon module is not installed consider executing ```pip install radon```
    From:   http://radon.readthedocs.io/en/latest/api.html
    https://www.guru99.com/cyclomatic-complexity.html

    '''
    f_source_code = "".join(inspect.getsourcelines(other_function)[0])
    results = radon.complexity.cc_visit(f_source_code)
    ranking = radon.complexity.sorted_results(results)
    pp = pprint.PrettyPrinter(indent=4)
    ranking_guide = '''
    1 - 5 A (low risk - simple block)
    ...
    41+ F (very high risk - error-prone, unstable block)
    '''
    pp.pprint(ranking_guide)
    actual_value = ranking[0][-1]
    pp.pprint('cognitive complexity of function {0} is: {1}'.format(other_function,actual_value))
    #df = pd.DataFrame(['cognitive complexity of function: '+str(other_function),actual_value])

    if actual_value > 10:
        pp.pprint('Consider rewriting your code it might be hard for you and others to understand, and therefore maintain')
    return actual_value

def is_function(object):
    return isinstance(object, types.FunctionType) 

def rank_all_sub_module_functions(provided_module):
    sc_objects = [v for k,v in inspect.getmembers(provided_module) ]
    ranks = []
    for sc in sc_objects:
        if is_function(sc):
            ranks.append(ccomplexity_rater(sc))
    return ranks
