# BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

from __future__ import absolute_import

import numpy
import numba

import awkward1.operations.convert
import awkward1._util
import awkward1._numba.layout
import awkward1._numba.arrayview
import awkward1._numba.libawkward

dynamic_addrs = {}
def globalstring(context, builder, pyvalue):
    import llvmlite.ir.types
    if pyvalue not in dynamic_addrs:
        buf = dynamic_addrs[pyvalue] = numpy.array(pyvalue.encode("utf-8") + b"\x00")
        context.add_dynamic_addr(builder, buf.ctypes.data, info="str({0})".format(repr(pyvalue)))
    ptr = context.get_constant(numba.types.uintp, dynamic_addrs[pyvalue].ctypes.data)
    return builder.inttoptr(ptr, llvmlite.llvmpy.core.Type.pointer(llvmlite.llvmpy.core.Type.int(8)))

class FillableArrayType(numba.types.Type):
    def __init__(self, behavior):
        super(FillableArrayType, self).__init__(name="awkward1.FillableArrayType({0})".format(awkward1._numba.repr_behavior(behavior)))
        self.behavior = behavior

@numba.extending.register_model(FillableArrayType)
class FillableArrayModel(numba.datamodel.models.StructModel):
    def __init__(self, dmm, fe_type):
        members= [("rawptr", numba.types.voidptr),
                  ("pyptr", numba.types.pyobject)]
        super(FillableArrayModel, self).__init__(dmm, fe_type, members)

@numba.extending.unbox(FillableArrayType)
def unbox_FillableArray(fillabletype, fillableobj, c):
    inner_obj = c.pyapi.object_getattr_string(fillableobj, "_fillablearray")
    rawptr_obj = c.pyapi.object_getattr_string(inner_obj, "_ptr")

    proxyout = c.context.make_helper(c.builder, fillabletype)
    proxyout.rawptr = c.pyapi.long_as_voidptr(rawptr_obj)
    proxyout.pyptr = inner_obj

    c.pyapi.decref(inner_obj)
    c.pyapi.decref(rawptr_obj)

    is_error = numba.cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return numba.extending.NativeValue(proxyout._getvalue(), is_error)

@numba.extending.box(FillableArrayType)
def box_FillableArray(fillabletype, fillableval, c):
    import awkward1.highlevel
    FillableArray_obj = c.pyapi.unserialize(c.pyapi.serialize_object(awkward1.highlevel.FillableArray))
    behavior_obj = c.pyapi.unserialize(c.pyapi.serialize_object(fillabletype.behavior))

    proxyin = c.context.make_helper(c.builder, fillabletype, fillableval)
    c.pyapi.incref(proxyin.pyptr)

    out = c.pyapi.call_method(FillableArray_obj, "_wrap", (proxyin.pyptr, behavior_obj))

    c.pyapi.decref(FillableArray_obj)
    c.pyapi.decref(behavior_obj)
    c.pyapi.decref(proxyin.pyptr)

    return out

def call(context, builder, fcn, args):
    fcntype = context.get_function_pointer_type(fcn.numbatype)
    fcnval = context.add_dynamic_addr(builder, fcn.numbatype.get_pointer(fcn), info=fcn.name)
    fcnptr = builder.bitcast(fcnval, fcntype)
    err = context.call_function_pointer(builder, fcnptr, args)
    with builder.if_then(builder.icmp_unsigned("!=", err, context.get_constant(numba.uint8, 0)), likely=False):
        context.call_conv.return_user_exc(builder, ValueError, (fcn.name + " failed",))

@numba.typing.templates.infer_global(len)
class type_len(numba.typing.templates.AbstractTemplate):
    def generic(self, args, kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], FillableArrayType):
            return numba.intp(args[0])

@numba.extending.lower_builtin(len, FillableArrayType)
def lower_len(context, builder, sig, args):
    fillabletype, = sig.args
    fillableval, = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    result = numba.cgutils.alloca_once(builder, context.get_value_type(numba.int64))
    call(context, builder, awkward1._numba.libawkward.FillableArray_length, (proxyin.rawptr, result))
    return awkward1._numba.castint(context, builder, numba.int64, numba.intp, builder.load(result))

@numba.typing.templates.infer_getattr
class type_methods(numba.typing.templates.AttributeTemplate):
    key = FillableArrayType

    @numba.typing.templates.bound_function("clear")
    def resolve_clear(self, fillabletype, args, kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return numba.types.none()
        else:
            raise TypeError("wrong number of arguments for FillableArray.clear")

    @numba.typing.templates.bound_function("null")
    def resolve_null(self, fillabletype, args, kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return numba.types.none()
        else:
            raise TypeError("wrong number of arguments for FillableArray.null")

    @numba.typing.templates.bound_function("boolean")
    def resolve_boolean(self, fillabletype, args, kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], numba.types.Boolean):
            return numba.types.none(args[0])
        else:
            raise TypeError("wrong number or types of arguments for FillableArray.boolean")

    @numba.typing.templates.bound_function("integer")
    def resolve_integer(self, fillabletype, args, kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], numba.types.Integer):
            return numba.types.none(args[0])
        else:
            raise TypeError("wrong number or types of arguments for FillableArray.integer")

    @numba.typing.templates.bound_function("real")
    def resolve_real(self, fillabletype, args, kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], (numba.types.Integer, numba.types.Float)):
            return numba.types.none(args[0])
        else:
            raise TypeError("wrong number or types of arguments for FillableArray.real")

    @numba.typing.templates.bound_function("beginlist")
    def resolve_beginlist(self, fillabletype, args, kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return numba.types.none()
        else:
            raise TypeError("wrong number of arguments for FillableArray.beginlist")

    @numba.typing.templates.bound_function("endlist")
    def resolve_endlist(self, fillabletype, args, kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return numba.types.none()
        else:
            raise TypeError("wrong number of arguments for FillableArray.endlist")

    @numba.typing.templates.bound_function("begintuple")
    def resolve_begintuple(self, fillabletype, args, kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], numba.types.Integer):
            return numba.types.none(args[0])
        else:
            raise TypeError("wrong number or types of arguments for FillableArray.begintuple")

    @numba.typing.templates.bound_function("index")
    def resolve_index(self, fillabletype, args, kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], numba.types.Integer):
            return numba.types.none(args[0])
        else:
            raise TypeError("wrong number or types of arguments for FillableArray.index")

    @numba.typing.templates.bound_function("endtuple")
    def resolve_endtuple(self, fillabletype, args, kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return numba.types.none()
        else:
            raise TypeError("wrong number of arguments for FillableArray.endtuple")

    @numba.typing.templates.bound_function("beginrecord")
    def resolve_beginrecord(self, fillabletype, args, kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return numba.types.none()
        elif len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], numba.types.StringLiteral):
            return numba.types.none(args[0])
        else:
            raise TypeError("wrong number or types of arguments for FillableArray.beginrecord")

    @numba.typing.templates.bound_function("field")
    def resolve_field(self, fillabletype, args, kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], numba.types.StringLiteral):
            return numba.types.none(args[0])
        else:
            raise TypeError("wrong number or types of arguments for FillableArray.field")

    @numba.typing.templates.bound_function("endrecord")
    def resolve_endrecord(self, fillabletype, args, kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return numba.types.none()
        else:
            raise TypeError("wrong number of arguments for FillableArray.endrecord")

    @numba.typing.templates.bound_function("append")
    def resolve_append(self, fillabletype, args, kwargs):
        import awkward1.highlevel

        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], (awkward1._numba.arrayview.ArrayViewType, awkward1._numba.arrayview.RecordViewType, numba.types.Boolean, numba.types.Integer, numba.types.Float)):
            return numba.types.none(args[0])
        elif len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], numba.types.Optional) and isinstance(args[0].type, (numba.types.Boolean, numba.types.Integer, numba.types.Float)):
            return numba.types.none(args[0])
        elif len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], numba.types.NoneType):
            return numba.types.none(args[0])
        elif len(args) == 2 and len(kwargs) == 0 and isinstance(args[0], awkward1._numba.arrayview.ArrayViewType) and isinstance(args[1], numba.types.Integer):
            return numba.types.none(args[0], args[1])
        else:
            if len(args) == 1 and fillabletype.behavior is not None:
                for key, lower in fillabletype.behavior.items():
                    if isinstance(key, tuple) and len(key) == 3 and key[0] == "__numba_lower__" and key[1] == awkward1.highlevel.FillableArray.append and (args[0] == key[2] or (isinstance(key[2], type) and isinstance(args[0], key[2]))):
                        numba.extending.lower_builtin("append", FillableArrayType, args[0])(lower)
                        return numba.types.none(args[0])

            raise TypeError("wrong number or types of arguments for FillableArray.append")

    @numba.typing.templates.bound_function("extend")
    def resolve_extend(self, fillabletype, args, kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], awkward1._numba.arrayview.ArrayViewType):
            return numba.types.none(args[0])
        else:
            raise TypeError("wrong number or types of arguments for FillableArray.extend")

@numba.extending.lower_builtin("clear", FillableArrayType)
def lower_clear(context, builder, sig, args):
    fillabletype, = sig.args
    fillableval, = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_clear, (proxyin.rawptr,))
    return context.get_dummy_value()

@numba.extending.lower_builtin("null", FillableArrayType)
def lower_null(context, builder, sig, args):
    fillabletype, = sig.args
    fillableval, = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_null, (proxyin.rawptr,))
    return context.get_dummy_value()

@numba.extending.lower_builtin("boolean", FillableArrayType, numba.types.Boolean)
def lower_boolean(context, builder, sig, args):
    fillabletype, xtype = sig.args
    fillableval, xval = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    x = builder.zext(xval, context.get_value_type(numba.uint8))
    call(context, builder, awkward1._numba.libawkward.FillableArray_boolean, (proxyin.rawptr, x))
    return context.get_dummy_value()

@numba.extending.lower_builtin("integer", FillableArrayType, numba.types.Integer)
def lower_integer(context, builder, sig, args):
    fillabletype, xtype = sig.args
    fillableval, xval = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    x = awkward1._numba.castint(context, builder, xtype, numba.int64, xval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_integer, (proxyin.rawptr, x))
    return context.get_dummy_value()

@numba.extending.lower_builtin("real", FillableArrayType, numba.types.Integer)
@numba.extending.lower_builtin("real", FillableArrayType, numba.types.Float)
def lower_real(context, builder, sig, args):
    fillabletype, xtype = sig.args
    fillableval, xval = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    if isinstance(xtype, numba.types.Integer) and xtype.signed:
        x = builder.sitofp(xval, context.get_value_type(numba.types.float64))
    elif isinstance(xtype, numba.types.Integer):
        x = builder.uitofp(xval, context.get_value_type(numba.types.float64))
    elif xtype.bitwidth < 64:
        x = builder.fpext(xval, context.get_value_type(numba.types.float64))
    elif xtype.bitwidth > 64:
        x = builder.fptrunc(xval, context.get_value_type(numba.types.float64))
    else:
        x = xval
    call(context, builder, awkward1._numba.libawkward.FillableArray_real, (proxyin.rawptr, x))
    return context.get_dummy_value()

@numba.extending.lower_builtin("beginlist", FillableArrayType)
def lower_beginlist(context, builder, sig, args):
    fillabletype, = sig.args
    fillableval, = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_beginlist, (proxyin.rawptr,))
    return context.get_dummy_value()

@numba.extending.lower_builtin("endlist", FillableArrayType)
def lower_endlist(context, builder, sig, args):
    fillabletype, = sig.args
    fillableval, = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_endlist, (proxyin.rawptr,))
    return context.get_dummy_value()

@numba.extending.lower_builtin("begintuple", FillableArrayType, numba.types.Integer)
def lower_begintuple(context, builder, sig, args):
    fillabletype, numfieldstype = sig.args
    fillableval, numfieldsval = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    numfields = awkward1._numba.castint(context, builder, numfieldstype, numba.int64, numfieldsval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_begintuple, (proxyin.rawptr, numfields))
    return context.get_dummy_value()

@numba.extending.lower_builtin("index", FillableArrayType, numba.types.Integer)
def lower_index(context, builder, sig, args):
    fillabletype, indextype = sig.args
    fillableval, indexval = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    index = awkward1._numba.castint(context, builder, indextype, numba.int64, indexval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_index, (proxyin.rawptr, index))
    return context.get_dummy_value()

@numba.extending.lower_builtin("endtuple", FillableArrayType)
def lower_endtuple(context, builder, sig, args):
    fillabletype, = sig.args
    fillableval, = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_endtuple, (proxyin.rawptr,))
    return context.get_dummy_value()

@numba.extending.lower_builtin("beginrecord", FillableArrayType)
def lower_beginrecord(context, builder, sig, args):
    fillabletype, = sig.args
    fillableval, = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_beginrecord, (proxyin.rawptr,))
    return context.get_dummy_value()

@numba.extending.lower_builtin("beginrecord", FillableArrayType, numba.types.StringLiteral)
def lower_beginrecord(context, builder, sig, args):
    fillabletype, nametype = sig.args
    fillableval, nameval = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    name = globalstring(context, builder, nametype.literal_value)
    call(context, builder, awkward1._numba.libawkward.FillableArray_beginrecord_fast, (proxyin.rawptr, name))
    return context.get_dummy_value()

@numba.extending.lower_builtin("field", FillableArrayType, numba.types.StringLiteral)
def lower_field(context, builder, sig, args):
    fillabletype, keytype = sig.args
    fillableval, keyval = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    key = globalstring(context, builder, keytype.literal_value)
    call(context, builder, awkward1._numba.libawkward.FillableArray_field_fast, (proxyin.rawptr, key))
    return context.get_dummy_value()

@numba.extending.lower_builtin("endrecord", FillableArrayType)
def lower_endrecord(context, builder, sig, args):
    fillabletype, = sig.args
    fillableval, = args
    proxyin = context.make_helper(builder, fillabletype, fillableval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_endrecord, (proxyin.rawptr,))
    return context.get_dummy_value()

@numba.extending.lower_builtin("append", FillableArrayType, awkward1._numba.arrayview.ArrayViewType, numba.types.Integer)
def lower_append_array_at(context, builder, sig, args):
    fillabletype, viewtype, attype = sig.args
    fillableval, viewval, atval = args

    viewproxy = context.make_helper(builder, viewtype, viewval)
    atval = awkward1._numba.layout.regularize_atval(context, builder, viewproxy, attype, atval, True, True)
    atval = awkward1._numba.castint(context, builder, numba.intp, numba.int64, atval)

    sharedptr = awkward1._numba.layout.getat(context, builder, viewproxy.sharedptrs, viewproxy.pos)

    proxyin = context.make_helper(builder, fillabletype, fillableval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_append_nowrap, (proxyin.rawptr, builder.inttoptr(sharedptr, context.get_value_type(numba.types.voidptr)), atval))
    return context.get_dummy_value()

@numba.extending.lower_builtin("append", FillableArrayType, awkward1._numba.arrayview.ArrayViewType)
def lower_append_array(context, builder, sig, args):
    fillabletype, viewtype = sig.args
    fillableval, viewval = args

    proxyin = context.make_helper(builder, fillabletype, fillableval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_beginlist, (proxyin.rawptr,))

    lower_extend_array(context, builder, sig, args)

    call(context, builder, awkward1._numba.libawkward.FillableArray_endlist, (proxyin.rawptr,))

    return context.get_dummy_value()

@numba.extending.lower_builtin("append", FillableArrayType, awkward1._numba.arrayview.RecordViewType)
def lower_append_record(context, builder, sig, args):
    fillabletype, recordviewtype = sig.args
    fillableval, recordviewval = args

    recordviewproxy = context.make_helper(builder, recordviewtype, recordviewval)

    arrayviewproxy = context.make_helper(builder, recordviewtype.arrayviewtype, recordviewproxy.arrayview)
    atval = awkward1._numba.castint(context, builder, numba.intp, numba.int64, recordviewproxy.at)

    sharedptr = awkward1._numba.layout.getat(context, builder, arrayviewproxy.sharedptrs, arrayviewproxy.pos)

    proxyin = context.make_helper(builder, fillabletype, fillableval)
    call(context, builder, awkward1._numba.libawkward.FillableArray_append_nowrap, (proxyin.rawptr, builder.inttoptr(sharedptr, context.get_value_type(numba.types.voidptr)), atval))
    return context.get_dummy_value()

@numba.extending.lower_builtin("append", FillableArrayType, numba.types.Boolean)
def lower_append_bool(context, builder, sig, args):
    return lower_boolean(context, builder, sig, args)

@numba.extending.lower_builtin("append", FillableArrayType, numba.types.Integer)
def lower_append_int(context, builder, sig, args):
    return lower_integer(context, builder, sig, args)

@numba.extending.lower_builtin("append", FillableArrayType, numba.types.Float)
def lower_append_float(context, builder, sig, args):
    return lower_real(context, builder, sig, args)

@numba.extending.lower_builtin("append", FillableArrayType, numba.types.Optional)
def lower_append_optional(context, builder, sig, args):
    fillabletype, opttype = sig.args
    fillableval, optval = args

    optproxy = context.make_helper(builder, opttype, optval)
    validbit = numba.cgutils.as_bool_bit(builder, optproxy.valid)

    with builder.if_else(validbit) as (is_valid, is_not_valid):
        with is_valid:
            if isinstance(opttype.type, numba.types.Boolean):
                lower_boolean(context, builder, numba.types.none(fillabletype, opttype.type), (fillableval, optproxy.data))
            elif isinstance(opttype.type, numba.types.Integer):
                lower_integer(context, builder, numba.types.none(fillabletype, opttype.type), (fillableval, optproxy.data))
            elif isinstance(opttype.type, numba.types.Float):
                lower_real(context, builder, numba.types.none(fillabletype, opttype.type), (fillableval, optproxy.data))
            else:
                raise AssertionError(opttype.type)

        with is_not_valid:
            lower_null(context, builder, numba.types.none(fillabletype,), (fillableval,))

    return context.get_dummy_value()

@numba.extending.lower_builtin("append", FillableArrayType, numba.types.NoneType)
def lower_append_none(context, builder, sig, args):
    return lower_null(context, builder, sig.return_type(sig.args[0]), (args[0],))

@numba.extending.lower_builtin("extend", FillableArrayType, awkward1._numba.arrayview.ArrayViewType)
def lower_extend_array(context, builder, sig, args):
    fillabletype, viewtype = sig.args
    fillableval, viewval = args

    viewproxy = context.make_helper(builder, viewtype, viewval)

    sharedptr = awkward1._numba.layout.getat(context, builder, viewproxy.sharedptrs, viewproxy.pos)

    proxyin = context.make_helper(builder, fillabletype, fillableval)
    with numba.cgutils.for_range(builder, viewproxy.stop, viewproxy.start) as loop:
        atval = awkward1._numba.castint(context, builder, numba.intp, numba.int64, loop.index)
        call(context, builder, awkward1._numba.libawkward.FillableArray_append_nowrap, (proxyin.rawptr, builder.inttoptr(sharedptr, context.get_value_type(numba.types.voidptr)), atval))

    return context.get_dummy_value()
