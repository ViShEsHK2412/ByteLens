import typer
import pathlib
import dis
from typing import Annotated
import tracemalloc
import types
import json

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
    json_output = json.dumps(result ,indent = 2)
    print(json_output)
    for const in code.co_consts:
        if isinstance(const,types.CodeType):
            analyzer_code(const)

@app.command()
def analyze(file:str):
    source = pathlib.Path(file).read_text('utf-8')
    code = compile(source,str(file),"exec")
    analyzer_code(code)


@app.command()
def trace(file:str):
    source = pathlib.Path(file).read_text('utf-8')
    code = compile(source,str(file),"exec")
    tracemalloc.start()
    exec(code)
    snapshot = tracemalloc.take_snapshot()
    stats = snapshot.statistics('lineno')
    tracemalloc.stop()
    for stat in stats:
        print(f"The status after tracing is -->{stat}")


if __name__ == "__main__":
    app()



