import typer
import pathlib
import dis
from typing import Annotated
import tracemalloc
import types


app = typer.Typer(no_args_is_help=True)

def analyzer_code(code : types.CodeType):
    dis.dis(code)
    for const in code.co_consts:
        if isinstance(const,types.CodeType) :
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



