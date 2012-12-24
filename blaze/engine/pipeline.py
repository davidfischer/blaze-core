# -*- coding: utf-8 -*-

"""
Defines the Pipeline class which provides a series of transformation
passes on the graph which result in code generation.
"""

from functools import partial
from itertools import ifilter
from collections import Counter

from blaze.plan import BlazeVisitor, InstructionGen

try:
    import numbapro
    have_numbapro = True
except ImportError:
    have_numbapro = False

#------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------

OP  = 0
APP = 1
VAL = 2
FUN = 3

#------------------------------------------------------------------------
# Pipeline Combinators
#------------------------------------------------------------------------

def compose(f, g):
    return lambda *x: g(*f(*x))

# monadic bind combinator <>, is the ``id`` function if pre and post
# condition holds, otherwise terminates is a ``const`` that returns the
# error and misbehaving condition.

def bind(self, f, x):
    if x is None:
        return None
    else:
        if f(x):
            return x
        else:
            return None

# Compose with pre and post condition checks
# pipeline = (post ∘ stl ∘ pre) <> (post ∘ st2 ∘ pre) <> ...
def compose_constrained(f, g, pre, post):
    return lambda *x: post(*g(*f(*pre(*x))))

#------------------------------------------------------------------------
# Pre/Post Conditions
#------------------------------------------------------------------------

# vacuously true condition
Id = lambda x:x

#------------------------------------------------------------------------
# Passes
#------------------------------------------------------------------------
#
#                  Input
#                     |
# +----------------------+
# |          pass 1      |
# +--------|----------|--+
#        context     ast
#          |          |
#   postcondition     |
#          |          |
#   precondition      |
#          |          |
# +--------|----------|--+
# |          pass 2      |
# +--------|----------|--+
#        context     ast
#          |          |
#   postcondition     |
#                     |
#   precondition      |
#          |          |
# +--------|----------|--+
# |          pass 3      |
# +--------|----------|--+
#        context     ast
#          |          |
#   precondition      |
#          |          |
#          +----------+-----> Output


def do_environment(context, graph):
    context = dict(context)

    # manually toggling numba support because it can crash if its not on
    # a test case that matches up with numba

    # ----------------------
    #context['have_numbapro'] = have_numbapro
    # ----------------------

    return context, graph

def do_convert_to_aterm(context, graph):
    """Convert the graph to an ATerm graph
    See blaze/expr/paterm.py

    ::
        a + b

    ::
        Arithmetic(
          Add
        , Array(){dshape("3, int64"), 45340864}
        , Array(){dshape("3, int64"), 45340864}
        ){dshape("3, int64"), 45264432}

    """
    context = dict(context)
    vars = topovals(graph)

    visitor = BlazeVisitor()
    aterm_graph = visitor.visit(graph)
    operands = visitor.operands

    # ----------------------
    context['operands'] = operands
    context['aterm_graph'] = aterm_graph

    # TODO: remove
    context['output'] = aterm_graph
    # ----------------------

    return context, graph

def do_types(context, graph):
    context = dict(context)

    # Resolve TypeVars using typeinference.py, not needed right
    # now because we're only doing simple numpy-like things

    return context, graph

def do_aterm(context, graph):
    aterm_graph = context['aterm_graph']
    return context, aterm_graph

def build_operand_dict(context, aterm_graph):
    operands = context['operands']
    operand_dict = dict((id(op), op) for op in operands)
    context['operand_dict'] = operand_dict
    return context, aterm_graph

def substitute_llvm(context, aterm_graph):
    "Substitute executors for the parts of the graph we can handle"
    from blaze.engine import llvm_execution

    executors = context['executors'] = {}
    aterm_graph = llvm_execution.substitute_llvm_executors(
                aterm_graph, executors, context["operand_dict"])
    return context, aterm_graph

def do_plan(context, aterm_graph):
    """ Take the ATerm expression graph and do inner-most evaluation to
    generate a linear sequence of instructions from that together with
    the table of inputs and outputs, built kernels forms the execution
    plan.

    Example::

    ::
        a + b * c

    ::
        vars %a %b %c
        %0 = Elemwise[np.mul,nogil](%b, %c)
        %0 = Elemwise[np.add,nogil,inplace](%a, %0)
        ret %0

    """
    context = dict(context)

    ivisitor = InstructionGen(context['executors'], have_numbapro=have_numbapro)
    plan = ivisitor.visit(aterm_graph)

    context['instructions'] = ivisitor.result()
    context['symbols'] = ivisitor.symbols

    return context, plan


#------------------------------------------------------------------------
# Pipeline
#------------------------------------------------------------------------

class Pipeline(object):
    """
    Plan generation pipeline is a series of composable pass stages
    which thread a context and graph object through to produce various
    intermediate forms resulting in an execution plan.

    The plan is a sequential series of instructions to concrete
    functions calls ( ufuncs, numba ufuncs, Python functions ) for the
    runtime to execute serially.
    """

    def __init__(self, *args, **kwargs):
        defaults = { 'have_numbapro': False } # have_numbapro }
        self.init = dict(defaults, **kwargs)

        # sequential pipeline of passes
        self.pipeline = [
            do_environment,
            do_convert_to_aterm,
            do_types,
            do_aterm,

            # codegen stages
            build_operand_dict,
            substitute_llvm,
            do_plan,
        ]

    def run_pipeline(self, graph, plan=False):
        """
        Run the graph through the pipeline
        """
        # Fuse the passes into one functional pipeline that is the
        # sequential composition with the intermediate ``context`` and
        # ``graph`` objects threaded through.

        # pipeline = stn ∘  ... ∘  st2 ∘ st1
        pipeline = reduce(compose, self.pipeline)

        context, plan = pipeline(self.init, graph)
        return context, plan

#------------------------------------------------------------------------
# Graph Manipulation
#------------------------------------------------------------------------

def khan_sort(pred, graph):
    """
    See: Kahn, Arthur B. (1962), "Topological sorting of large networks"
    """
    result = []
    count = Counter()

    for node in graph:
        for child in iter(node):
            count[child] += 1

    sort = [node for node in graph if not count[node]]

    while sort:
        node = sort.pop()
        result.append(node)

        for child in iter(node):
            count[child] -= 1
            if count[child] == 0:
                sort.append(child)

    result.reverse()

    # Collect all the nodes thats satisfy the selecter property.
    # For example, all the value nodes or all the op nodes.
    return list(ifilter(pred, result))

def tarjan_sort(pred, graph):
    raise NotImplementedError

def toposort(pred, graph, algorithm='khan'):
    """
    Sort the expression graph topologically to resolve the order needed
    to execute operations.
    """

    #
    #     +
    #    / \
    #   a   +     --> [a, b, c, d]
    #      / \
    #     b   c
    #         |
    #         d
    #

    if algorithm == 'khan':
        return khan_sort(pred, graph)
    if algorithm == 'tarjan':
        return tarjan_sort(pred, graph)
    else:
        raise NotImplementedError

#------------------------------------------------------------------------
# Sorters
#------------------------------------------------------------------------

topovals = partial(toposort, lambda x: x.kind == VAL)
topops   = partial(toposort, lambda x: x.kind == OP)
topfuns  = partial(toposort, lambda x: x.kind == FUN)
