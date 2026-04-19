import typer
import pathlib
import dis
from typing import Annotated


app = typer.Typer()

def analyze(file:str):
    source = pathlib.Path(file).read_text('utf-8')
    code = compile(source,str(file),"exec")
    dis.dis(code)
    


@app.command()
def main(
    analyzer: Annotated[str,typer.Option()]
):
    if analyzer:
        return analyze(analyzer)
    




if __name__ == "__main__":
    app()



