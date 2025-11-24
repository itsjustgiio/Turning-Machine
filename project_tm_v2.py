#!/usr/bin/env python3

import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python project_tm_v2.py <machine_file> <tape_file>")
        return

    machine_file = sys.argv[1]
    tape_file = sys.argv[2]

    with open(machine_file, "r") as f:
        # Read file into stripped lines
        lines = [line.strip() for line in f if line.strip()]

    # Parse LINE 1
    header = lines[0].split(",")
    name = header[0]
    num_tapes = int(header[1])
    max_tape_length = int(header[2])
    max_steps = int(header[3])

    print("Machine name:", name)
    print("Number of tapes:", num_tapes)
    print("Max tape length:", max_tape_length)  # Testing: verify machine configuration parsed correctly
    print("Max steps:", max_steps)  # Testing: verify machine configuration parsed correctly

    # LINE 2: input alphabet Sigma
    sigma = lines[1].split(",")
    print("Sigma:", sigma)  # Testing: verify input alphabet parsed correctly

    # LINE 3: states
    states = lines[2].split(",")
    print("States:", states)  # Testing: verify states parsed correctly

    start_state = lines[3]
    print("Start state:", start_state)  # Testing: verify start state parsed correctly

    accept_reject = lines[4].split(",")
    accept_state = accept_reject[0]
    reject_state = accept_reject[1]

    print("Accept state:", accept_state)  # Testing: verify accept state parsed correctly
    print("Reject state:", reject_state)  # Testing: verify reject state parsed correctly

    # GAMMA lines begin at index 5
    gamma_lines_start = 5

    gamma = []
    for i in range(num_tapes):
        tape_gamma = lines[gamma_lines_start + i].split(",")
        gamma.append(tape_gamma)

    print("Gamma:", gamma)  # Testing: verify tape alphabets parsed correctly

    transitions = {}
    rule_num = 1

    # Start reading rules after gamma
    transition_start = 5 + num_tapes

    for line in lines[transition_start:]:
        parts = line.split(",")

        curr_state = parts[0]
        
        # Read k symbols (one per tape)
        read_syms = []
        for i in range(num_tapes):
            read_syms.append(parts[1 + i])
        
        next_state = parts[1 + num_tapes]
        
        # Write k symbols (one per tape)
        write_syms = []
        for i in range(num_tapes):
            write_syms.append(parts[2 + num_tapes + i])
        
        # Move k directions (one per tape)
        move_dirs = []
        for i in range(num_tapes):
            move_dirs.append(parts[2 + 2*num_tapes + i])

        key = (curr_state, tuple(read_syms))
        val = (next_state, tuple(write_syms), tuple(move_dirs), rule_num)

        transitions[key] = val
        
        # Print rule as it's read in (spec requirement: echo EXACTLY as read)
        print(f"{rule_num}. {line}")
        
        rule_num += 1

    print()  # Blank line after rules
    print("Loaded transitions:", len(transitions))  # Testing: verify transitions parsed correctly

    # Parse tape file
    with open(tape_file, "r") as f:
        tape_lines = [line.strip() for line in f if line.strip()]

    print("\n=== Processing tape configurations ===")
    
    tape_idx = 0
    line_idx = 0
    
    while line_idx < len(tape_lines):
        tape_idx += 1
        
        # Read k lines for k tapes
        initial_tapes = []
        for i in range(num_tapes):
            if line_idx + i < len(tape_lines):
                initial_tapes.append(tape_lines[line_idx + i])
            else:
                initial_tapes.append("")
        
        line_idx += num_tapes
        
        print(f"\nTest case {tape_idx}:")
        for i, tape_content in enumerate(initial_tapes):
            print(f"  Initial tape {i+1}: {tape_content}")
        
        # Simulate the Turing Machine
        current_state = start_state
        heads = [0] * num_tapes  # head positions for each tape
        tapes = []
        
        # Pad tapes with blanks
        for tape_str in initial_tapes:
            tape_list = list(tape_str) + ['_'] * (max_tape_length - len(tape_str))
            tapes.append(tape_list)
        
        step = 0
        
        # Print initial state
        if num_tapes == 1:
            print(f"  Step {step}: State={current_state}, Tape={''.join(tapes[0]).rstrip('_')}, Head={heads[0]}")
        else:
            tape_str = " | ".join([f"T{i+1}:{''.join(tapes[i]).rstrip('_')}" for i in range(num_tapes)])
            head_str = " | ".join([f"H{i+1}:{heads[i]}" for i in range(num_tapes)])
            print(f"  Step {step}: State={current_state}")
            print(f"    Tapes: {tape_str}")
            print(f"    Heads: {head_str}")
        
        # Simulation loop
        while step < max_steps:
            step += 1
            
            # Check if we reached accept or reject state
            if current_state == accept_state:
                break
            elif current_state == reject_state:
                break
            
            # Read symbols from all tapes at head positions
            read_symbols = tuple(tapes[i][heads[i]] for i in range(num_tapes))
            
            # Check if symbols are legal (in Gamma or blank '_')
            for i in range(num_tapes):
                if read_symbols[i] != '_' and read_symbols[i] not in gamma[i]:
                    print(f"  ERROR: Illegal symbol '{read_symbols[i]}' on tape {i+1}")
                    current_state = "ERROR"
                    break
            
            if current_state == "ERROR":
                break
            
            # Look up transition (handle wildcard *)
            key = (current_state, read_symbols)
            
            if key not in transitions:
                # Try to find wildcard rule: replace each read symbol with '*' and check
                found_wildcard = False
                for wildcard_pattern in range(2**num_tapes):
                    # Generate all possible wildcard combinations
                    test_read = []
                    for i in range(num_tapes):
                        if wildcard_pattern & (1 << i):
                            test_read.append('*')
                        else:
                            test_read.append(read_symbols[i])
                    test_key = (current_state, tuple(test_read))
                    if test_key in transitions:
                        key = test_key
                        found_wildcard = True
                        break
                
                if not found_wildcard:
                    current_state = reject_state
                    break
            
            # Apply transition
            next_state, write_symbols, move_dirs, rule_num = transitions[key]
            
            # Handle wildcard * in write symbols (means "don't change")
            actual_write = []
            for i in range(num_tapes):
                if write_symbols[i] == '*':
                    actual_write.append(read_symbols[i])  # Keep original symbol
                else:
                    actual_write.append(write_symbols[i])
            write_symbols = tuple(actual_write)
            
            # Print step trace in CSV format: Step, Rule#, {TapeIndex}k, CurrentState, {ReadSymbol}k, NextState, {WriteSymbol}k, {Direction}k
            tape_indices_str = ",".join(str(h) for h in heads)
            read_str = ",".join(read_symbols)
            write_str = ",".join(write_symbols)
            move_str = ",".join(move_dirs)
            print(f"  {step},{rule_num},{tape_indices_str},{current_state},{read_str},{next_state},{write_str},{move_str}")
            
            # Write symbols
            for i in range(num_tapes):
                tapes[i][heads[i]] = write_symbols[i]
            
            # Move heads
            for i in range(num_tapes):
                if move_dirs[i] == 'L':
                    heads[i] = max(0, heads[i] - 1)
                elif move_dirs[i] == 'R':
                    heads[i] = min(max_tape_length - 1, heads[i] + 1)
                # 'S' means stay
            
            # Update state
            current_state = next_state
        
        # Print final status (spec requirement)
        print()  # Blank line before status
        if step >= max_steps:
            current_state = reject_state
        
        if current_state == accept_state:
            print("Accepted")
        elif current_state == reject_state:
            print("Rejected")
        elif current_state == "ERROR":
            print("Error")
        else:
            print("Error")
        
        # Print final tape(s) - one per line
        for i in range(num_tapes):
            final_tape = ''.join(tapes[i]).rstrip('_')
            if num_tapes == 1:
                print(final_tape)
            else:
                print(f"Tape {i+1}: {final_tape}")

if __name__ == "__main__":
    main()
