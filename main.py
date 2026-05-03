import typer
import pathlib
import dis
from typing import Annotated
import tracemalloc
import types
import json
import gc

app = typer.Typer(no_args_is_help=True)

def analyzer_code(code : types.CodeType):
    instructions = dis.get_instructions(code)
    result = []
    for instr in instructions:
        item = {
        "offset": instr.offset,
        "opcode": instr.opname,
        "argument": instr.arg,
        "arg_type": type(instr.argval).__name__,
        "arg_value": instr.argval.co_name if hasattr(instr.argval, "co_name") else instr.argval
    }
    result.append(item)
    # Created another List called Children to create a better structured JSON
    children = []
    for const in code.co_consts:
        if isinstance(const,types.CodeType):
    #Appending the recursive Code Object which is basically another function inside th children List
            children.append(analyzer_code(const))
    # Returning a more Structred JSON which will show use the name of the Code Oject its instructions and the children i.e. its functions inside that instruction
    return {
        "name": code.co_name,
        "instructions": result,
        "children": children
    }

@app.command()
def analyze(file:str):
    source = pathlib.Path(file).read_text('utf-8')
    code = compile(source,str(file),"exec")
    final_result = analyzer_code(code)
    # Instead of printing JSON after every loop shifted it to the CLI Command to print the result all at once
    print(json.dumps(final_result,indent=2))


@app.command()
def trace(file:str):
    source = pathlib.Path(file).read_text('utf-8')
    code = compile(source,str(file),"exec")
    gc.set_debug(gc.DEBUG_SAVEALL)
    tracemalloc.start()
    exec(code)
    snapshot = tracemalloc.take_snapshot()
    gc.collect()
    cycles = gc.garbage
    stats = snapshot.statistics('lineno')
    tracemalloc.stop()
    for stat in stats:
        print(f"The status after tracing is -->{stat}")
    print(f"The GC refrence Cycles are: {len(cycles)}")


if __name__ == "__main__":
    app()



