# BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

from __future__ import absolute_import

import sys

import awkward1.layout
import awkward1.operations.convert
import awkward1._util

def getArguments(names, local_dict=None, global_dict=None):
    """Replaces numexpr.necompiler.getArguments to avoid calling numpy.asarray on Awkward Arrays."""
    call_frame = sys._getframe(2)

    clear_local_dict = False
    if local_dict is None:
        local_dict = call_frame.f_locals
        clear_local_dict = True
    try:
        frame_globals = call_frame.f_globals
        if global_dict is None:
            global_dict = frame_globals

        # If `call_frame` is the top frame of the interpreter we can't clear its 
        # `local_dict`, because it is actually the `global_dict`.
        clear_local_dict = clear_local_dict and not frame_globals is local_dict

        arguments = []
        for name in names:
            try:
                a = local_dict[name]
            except KeyError:
                a = global_dict[name]
            arguments.append(a)    # <--- This is different from NumExpr: don't call numpy.asarray(a)
    finally:
        # If we generated local_dict via an explicit reference to f_locals,
        # clear the dict to prevent creating extra ref counts in the caller's scope
        # See https://github.com/pydata/numexpr/issues/310
        if clear_local_dict:
            local_dict.clear()

    return arguments

def evaluate(expression, local_dict=None, global_dict=None, order="K", casting="safe", **kwargs):
    import numexpr

    context = numexpr.necompiler.getContext(kwargs, frame_depth=1)
    expr_key = (expression, tuple(sorted(context.items())))
    if expr_key not in numexpr.necompiler._names_cache:
        numexpr.necompiler._names_cache[expr_key] = numexpr.necompiler.getExprNames(expression, context)
    names, ex_uses_vml = numexpr.necompiler._names_cache[expr_key]
    arguments = getArguments(names, local_dict, global_dict)

    arrays = [awkward1.operations.convert.tolayout(x, allowrecord=True, allowother=True) for x in arguments]

    def getfunction(inputs):
        if all(isinstance(x, awkward1.layout.NumpyArray) or not isinstance(x, awkward1.layout.Content) for x in inputs):
            return lambda depth: (awkward1.layout.NumpyArray(numexpr.evaluate(expression, dict(zip(names, inputs)), {}, order=order, casting=casting, **kwargs)),)
        else:
            return None

    out = awkward1._util.broadcast_and_apply(arrays, getfunction)
    assert isinstance(out, tuple) and len(out) == 1
    return awkward1._util.wrap(out[0], awkward1._util.behaviorof(arrays))

evaluate.evaluate = evaluate

def re_evaluate(local_dict=None):
    import numexpr

    try:
        compiled_ex = numexpr.necompiler._numexpr_last["ex"]
    except KeyError:
        raise RuntimeError("not a previous evaluate() execution found")
    names = numexpr.necompiler._numexpr_last["argnames"]
    arguments = getArguments(names, local_dict)

    arrays = [awkward1.operations.convert.tolayout(x, allowrecord=True, allowother=True) for x in arguments]

    def getfunction(inputs):
        if all(isinstance(x, awkward1.layout.NumpyArray) or not isinstance(x, awkward1.layout.Content) for x in inputs):

            return lambda depth: (awkward1.layout.NumpyArray(numexpr.re_evaluate(dict(zip(names, inputs)))),)

        return None

    out = awkward1._util.broadcast_and_apply(arrays, getfunction)
    assert isinstance(out, tuple) and len(out) == 1
    return awkward1._util.wrap(out[0], awkward1._util.behaviorof(arrays))

evaluate.re_evaluate = re_evaluate
