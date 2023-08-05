from llvmlite import ir, binding as ll
import numba as nb
from numba import jit
import numpy as np
from os import listdir
from pathlib import Path
import cffi
import sys
import os

ffi = cffi.FFI()
#if getattr(sys, 'frozen', False):
#   ll_path = Path(sys._MEIPASS).resolve() / "ll"
#else:
ll_path = Path(__file__).resolve().parent/"ll"/ os.name
    # ll code is binded to the path of the py file

def compile_library(context, asm, libname='compiled_module'):
    library = context.codegen().create_library(libname)
    ll_module = ll.parse_assembly(asm)
    ll_module.verify()
    library.add_llvm_module(ll_module)
    return library


def link_global(name, do_get=True, type=nb.int64):
    llvm_global_get = """
    @test = external global i64, align 8
    define i64 @test_get() #0 {
      %1 = load i64, i64* @test, align 8
      ret i64 %1
    }
    attributes #0 = { alwaysinline nounwind uwtable  }
    """
    llvm_global_set = """
    @test = external global i64, align 8
    define i64 @test_set(i64) #0 {
      %2 = alloca i64, align 8
      store i64 %0, i64* %2, align 8
      %3 = load i64, i64* %2, align 8
      store i64 %3, i64* @test, align 8
      %4 = load i64, i64* @test, align 8
      ret i64 %4
    }
    attributes #0 = { alwaysinline nounwind uwtable }
    """

    @nb.extending.intrinsic
    def BytesofRecords_get(typingctx):
        sig = nb.typing.signature(nb.int64)

        def codegen(context, builder, sig, args):
            library = compile_library(
                context, llvm_global_get.replace("test", name))
            context.active_code_library.add_linking_library(library) # no more weird hack to get the library linked
            argtypes = [context.get_argument_type(aty) for aty in sig.args]
            restype = context.get_argument_type(sig.return_type)
            fnty = ir.FunctionType(restype, argtypes)
            fn = nb.cgutils.insert_pure_function(
                builder.module, fnty, name=name + "_get")
            retval = context.call_external_function(
                builder, fn, sig.args, args)
            # print(fn)
            return retval

        return sig, codegen

    def BytesofRecords_set(typingctx, param1):
        sig = nb.typing.signature(nb.int64, param1)

        def codegen(context, builder, sig, args):
            code = llvm_global_set.replace("test", name)
            library = compile_library(
                context, code)
            context.active_code_library.add_linking_library(library) # no more weird hack to get the library linked
            argtypes = [context.get_argument_type(aty) for aty in sig.args]
            restype = context.get_argument_type(sig.return_type)
            fnty = ir.FunctionType(restype, argtypes)
            fn = nb.cgutils.insert_pure_function(
                builder.module, fnty, name=name + "_set")
            retval = context.call_external_function(
                builder, fn, sig.args, args)
            # print(fn)
            return retval

        return sig, codegen

    if do_get:
        return BytesofRecords_get
    else:
        return BytesofRecords_set


@nb.extending.intrinsic
def link_libs(typingctx):
    sig = nb.typing.signature(nb.int32)

    def codegen(context, builder, sig, args):
        # print("===== linking =====")
        
        for f in listdir(ll_path):
            lib_path = Path(ll_path)/ f
            if lib_path.is_file() and f.find(".ll")>=0:
                # print(lib_path)
                with open(lib_path, "r") as fio:
                    assembly = fio.read()
                    assembly = assembly.replace("""!llvm.linker.options = !{!0}""","")# hack: remove useless linker options for LLVM7 
                    library = compile_library(context, assembly, str(lib_path.resolve()))
                context.active_code_library.add_linking_library(library) # no more weird hack to get the library linked

        # print("===== done =====")
        return context.get_constant(nb.int32, 42)

    return sig, codegen


def link_function(func_name="", param=1, i64ret=False):
    typer = "int32"
    if (i64ret):
        typer = "int64"
    code = """
def ARB_PARAM_MAKER():
    def codegen(context, builder, sig, args):
        argtypes = [context.get_argument_type(aty) for aty in sig.args]
        restype = context.get_argument_type(sig.return_type)
        fnty = ir.FunctionType(restype, argtypes)
        fn = nb.cgutils.insert_pure_function(
            builder.module, fnty, name="{func_name}")
        retval = context.call_external_function(builder, fn, sig.args, args)
        #print(fn)
        return retval
    @nb.extending.intrinsic
    def ARB_PARAM(typingctx, {para}):
        sig = nb.typing.signature(nb.{typer}, {para})
        return sig, codegen
    return ARB_PARAM
""".format(para=",".join(["a{}".format(i) for i in range(0, param)]), func_name=func_name, typer=typer)
    exec(code, globals(), locals())
    return locals()["ARB_PARAM_MAKER"]()


def link_jit_code(code):
    glb = {
        "jit": jit, "ffi": ffi, "nb": nb, "np": np,
        "link_libs": link_libs,
        
        "pop_signal_from_file": link_function("pop_signal_from_file", 2, i64ret=True),
        "FileReader_init": link_function("FileReader_init", 2),

        "VFILE_init": link_function("VFILE_init", 5),
        "POOL_update": link_function("POOL_update", 3),
        "POOL_init": link_function("POOL_init", 6),
        "VCHN_init": link_function("VCHN_init", 5),
        "VCHN_put": link_function("VCHN_put", 3),
        "VCHN_next": link_function("VCHN_next", 2, i64ret=True),
    }
    loc = {}

    exec(code, glb, loc)

    return loc
