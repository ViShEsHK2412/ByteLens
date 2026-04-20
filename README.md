# 🧠 Python Bytecode & Memory Analyzer

> A low-level Python analysis tool that explores **bytecode structure, memory behavior, and reference patterns** using Python internals.

---

## 🚀 Overview

This project aims to build a **deep introspection tool for Python programs**, focusing on:

* 🔍 Bytecode analysis (`dis`)
* 🧠 Code object traversal (`compile`, `co_consts`)
* 📊 Memory tracking (`tracemalloc`)
* ♻️ Reference & GC exploration (`gc`)

Instead of treating Python as a black box, this tool breaks down **how Python actually executes code under the hood**.

---

## ⚙️ Current Features

### ✅ Bytecode Inspection

* Compiles Python source into code objects
* Disassembles bytecode using `dis`
* Understands instruction structure:

  * offset
  * opcode
  * argument

---

### ✅ Code Object Discovery

* Extracts `co_consts` from compiled code
* Detects nested **code objects (functions, lambdas, etc.)**
* Differentiates:

  * executable code objects
  * regular constants (`None`, numbers, strings)

---

### 🚧 Recursive Code Traversal (In Progress)

* Building a recursive analyzer to walk:

```text
module → function → nested function → ...
```

* Goal: represent Python execution as a **tree of code objects**

---

### 🚧 Structured Output (In Progress)

* Moving from raw `dis` output → structured data
* Planned format:

```json
{
  "name": "function_name",
  "instructions": [...],
  "children": [...]
}
```

---

### 🚧 Memory Analysis (Experimental)

* Using `tracemalloc` to:

  * track allocations
  * identify high-memory lines
* Future: correlate bytecode ↔ memory usage

---

### 🔜 Planned: GC & Reference Analysis

* Explore `gc` module
* Detect:

  * reference relationships
  * potential cycles
* Build object graph understanding

---

## 🧠 Key Concepts Learned

This project is heavily focused on understanding:

* Python **code objects**
* `co_consts`, `co_names`, execution model
* Bytecode instruction format:

  ```
  offset | opcode | argument
  ```
* Difference between:

  * structure (code objects)
  * behavior (bytecode)
* Internal execution model (inspired by CPython)

---

## 🛠️ Tech Stack

* Python 3.11+
* `dis` — bytecode inspection
* `types` — code object detection
* `tracemalloc` — memory tracking
* `gc` — garbage collection analysis

---

## 📂 Project Status

> 🟡 **Active Development**

Current focus:

* Recursive traversal of code objects
* Clean structured representation of bytecode
* Building a proper analysis pipeline

---

## 🎯 Roadmap

* [x] Basic disassembly
* [x] Code object detection via `co_consts`
* [ ] Recursive traversal of nested code
* [ ] Structured JSON output
* [ ] Memory + bytecode correlation
* [ ] Reference graph analysis
* [ ] Cycle detection

---

## 💡 Vision

The goal is to evolve this into:

> A **mini Python introspection engine** that explains:
>
> * how code is executed
> * where memory is used
> * why objects stay alive




## 📌 Notes

This project intentionally dives into **Python internals**, so some parts may feel low-level or experimental.


