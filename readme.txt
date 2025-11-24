# 🧠 Multi-Tape Turing Machine Simulator  
**Author:** Giovanni Carrion  
**Course:** CSc 30100 — Theory of Computation  
**Professor:** Jordan Matuszewski  
**Project:** Midterm — Adapted from Peter Kogge’s multi-tape Turing Machine assignment

---

## 📌 Overview

This project is a **fully general multi-tape Turing Machine simulator** implemented in Python.  
It reads a machine description file (e.g., `TM1.txt`) and a tape input file (e.g., `TM1-tape.txt`), constructs the Turing Machine dynamically, and simulates execution step-by-step according to the formal TM specification.

This simulator **does not hard-code any transitions**; it works for any valid machine file that follows the project specification.

---

## ✨ Features

### ✔️ General Multi-Tape Support
- Handles **1 or more tapes**  
- Independent tape alphabets (Γ) per tape  
- Independent head positions per tape  

### ✔️ Full Machine Specification Parsing
Reads and validates:
- Machine name  
- Number of tapes  
- Maximum tape length  
- Maximum number of steps  
- Input alphabet Σ  
- Tape alphabets Γ per tape  
- States  
- Start, accept, and reject states  
- All transitions from the machine file

### ✔️ Wildcard Support (`*`)
Supports:
- `*` in read position (matches any symbol)  
- `*` in write position (write-back original symbol)

Wildcard matching is implemented using bitmask enumeration across tapes.

### ✔️ Step-By-Step Execution Trace
For every simulated step, prints:

Step#, Rule#, HeadPositions(k), CurrentState, ReadSymbols(k), NextState, WriteSymbols(k), Directions(k)

yaml
Copy code

Matches the required output format from the project specifications.

### ✔️ Error Handling
Simulator halts with:
- `Accepted`
- `Rejected`
- `Error` (illegal symbol or undefined transition)
- Or `Rejected` if maximum steps are exceeded

### ✔️ Final Tape Output
After each test case, the simulator prints each tape’s final contents (with trailing blanks `_` removed).

---

## 📂 File Structure

Project_TM-V2/
│
├── project_tm_v2.py # Main Turing Machine simulator
├── TM1.txt
├── TM1-tape.txt
├── TM1-accept.txt
├── TM1-reject.txt
├── TM1d.txt
├── TM2.txt
├── TM2-tape.txt
├── TM3.txt
├── TM3-tape.txt
├── TMsim.xlsx # Spreadsheet from original Kogge assignment
└── readme.txt # Original assignment instructions

yaml
Copy code

---

## ▶️ How to Run

### **Command line usage**
python project_tm_v2.py <machine_file> <tape_file>

shell
Copy code

### Examples
Run TM1:
python project_tm_v2.py TM1.txt TM1-tape.txt

yaml
Copy code

Run TM3:
python project_tm_v2.py TM3.txt TM3-tape.txt

yaml
Copy code

---

## 📝 Output Format

### 1. Rules are echoed exactly as parsed:
q0,h,q0,H,R

q0,H,q0,h,R
...

shell
Copy code

### 2. Each test case begins with its initial tapes:
Test case 1:
Initial tape 1: helloworld>

shell
Copy code

### 3. Execution trace (CSV-style):
1,12,0,q0,h,q0,H,R
2,8,1,q0,e,q0,E,R

shell
Copy code

### 4. Final status:
Accepted

shell
Copy code

### 5. Final tape output:
HELLOWORLD.

yaml
Copy code

---

## 🛠 Implementation Notes

- Tapes are stored as fixed-length Python lists padded with `_`
- Transition table uses tuples: `(state, (read1, read2, ...))`
- Supports exact-match rules and wildcard-match fallbacks
- Head positions are clamped within bounds `[0, max_tape_length - 1]`
- Simulator follows the specification adapted for this course

---

## 📜 Academic Integrity Notice

This simulator was developed independently from scratch and follows the CCNY CSc 30100 project specifications.  
All Turing Machine behavior is determined purely by the machine description files.

---

## 📧 Contact

For questions or issues, feel free to open a GitHub issue on this repository.
