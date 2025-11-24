# 🧠 Multi-Tape Turing Machine Simulator  
**Author:** Giovanni Carrion  
**Course:** CSc 30100 — Theory of Computation  
**Professor:** Jordan Matuszewski  
**Project:** Midterm — Adapted from Peter Kogge’s multi-tape Turing Machine assignment

---

## 📌 Overview

A **general multi-tape Turing Machine simulator** implemented in Python.

It reads:
- A machine description file (e.g., `TM1.txt`)
- A tape file containing inputs (e.g., `TM1-tape.txt`)

Then dynamically constructs the Turing Machine and executes it step-by-step according to the formal specifications.

This simulator **does not hard-code transitions** and fully supports all valid machine files.

---

## ✨ Features

### ✔️ General Multi-Tape Support
- Supports **1 or more tapes**
- Independent Γ (tape alphabet) per tape
- Independent head positions per tape

### ✔️ Full Machine Specification Parsing
Reads:
- Machine name  
- Number of tapes  
- Maximum tape length  
- Maximum number of steps  
- Input alphabet Σ  
- Tape alphabets Γ per tape  
- All states  
- Start, accept, reject states  
- All transition rules

### ✔️ Wildcard Support (`*`)
- `*` in **read** position → matches any symbol  
- `*` in **write** position → keep original symbol  

Wildcard resolution uses bitmask enumeration.

### ✔️ Step-By-Step Execution Trace
Each step prints:

Step, Rule#, HeadPositions, CurrentState, ReadSymbols, NextState, WriteSymbols, MoveDirections
