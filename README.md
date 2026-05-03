# ByteLens — Python Bytecode & Memory Analyzer

> A low-level CLI tool that exposes what Python is actually doing — bytecode structure, memory allocations, and reference cycles — using nothing but Python internals.

---

## Overview

Most Python developers treat the runtime as a black box. `ByteLens` breaks that box open. It gives you a structured view of how your code compiles to bytecode, where memory is being allocated line by line, and whether your program is leaking objects through reference cycles.

Built entirely using Python's own introspection modules — no external analysis dependencies.

---

## Commands

### `ByteLens analyze <file>`

Disassembles a Python file into a structured JSON tree of bytecode instructions, organized by function.

```bash
uv run main.py analyze main.py
```

**Output:**
```json
{
  "name": "<module>",
  "instructions": [
    {
      "offset": 8,
      "opcode": "RETURN_CONST",
      "argument": 1,
      "arg_type": "NoneType",
      "arg_value": null
    }
  ],
  "children": [
    {
      "name": "outer_function",
      "instructions": [...],
      "children": [
        {
          "name": "inner_function",
          "instructions": [...],
          "children": []
        }
      ]
    }
  ]
}
```

**What it does:**
- Reads and compiles the source file using `compile()`
- Disassembles every code object using `dis.get_instructions()`
- Recursively walks `co_consts` to find nested functions and lambdas
- Returns a tree where each node is a function with its full bytecode listing
- Each instruction includes offset, opcode name, argument, argument type, and resolved argument value

---

### `ByteLens trace <file>`

Executes a Python file and captures memory allocations line by line, plus reference cycle detection.

```bash
uv run main.py trace trace.py
```

**Output:**
```
The status after tracing is -->C:\path\to\file.py:12: size=256 B, count=1, average=256 B
The GC reference cycles are: 13
```

**What it does:**
- Compiles and executes the target file using `exec()`
- Wraps execution with `tracemalloc` to capture per-line memory allocation stats
- Sets `gc.DEBUG_SAVEALL` before execution so the garbage collector saves all cycle candidates
- Calls `gc.collect()` after execution to force a full GC pass
- Reads `gc.garbage` to report how many reference cycles were detected during execution

---

## How It Works Internally

### Bytecode Analysis Pipeline

```
source file
    ↓ pathlib.Path.read_text()
raw source string
    ↓ compile(source, filename, "exec")
code object
    ↓ dis.get_instructions(code)
instruction stream
    ↓ recursive co_consts traversal
structured JSON tree
```

### Memory + Cycle Detection Pipeline

```
source file
    ↓ compile()
code object
    ↓ gc.set_debug(gc.DEBUG_SAVEALL)  ← flag set before execution
    ↓ tracemalloc.start()
    ↓ exec(code)                      ← program runs here
    ↓ tracemalloc.take_snapshot()     ← memory captured immediately after
    ↓ gc.collect()                    ← GC runs, saves cycles to gc.garbage
    ↓ cycles = gc.garbage             ← snapshot of what was found
memory stats + cycle count
```

---

## Tech Stack

| Module | Role |
|---|---|
| `dis` | Bytecode disassembly |
| `types.CodeType` | Code object type detection for recursive traversal |
| `compile()` | Source → code object compilation |
| `tracemalloc` | Per-line memory allocation tracking |
| `gc` | Garbage collector cycle detection |
| `json` | Structured output formatting |
| `pathlib` | File reading |
| `typer` | CLI interface |

---

## Installation

```bash
git clone https://github.com/yourusername/ByteLens
cd ByteLens
uv sync
```

---

## Usage Examples

Analyze your own project files:
```bash
uv run main.py analyze src/app.py
uv run main.py trace src/app.py
```

Test cycle detection with a known cycle:
```python
# cycle_test.py
a = {}
b = {}
a['ref'] = b
b['ref'] = a
```
```bash
uv run main.py trace cycle_test.py
# The GC reference cycles are: 13
```

---

## Project Structure

```
ByteLens/
├── main.py           # CLI entrypoint — analyze + trace commands
├── pyproject.toml    # uv package config
├── .python-version
├── README.md
└── .gitignore
```

---



## 📌 Notes

This project intentionally dives into **Python internals**, so some parts may feel low-level or experimental.


