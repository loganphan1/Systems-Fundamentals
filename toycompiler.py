#!/usr/bin/env python3
import sys
import re

register_map = ["$t0","$t1","$t2","$t3","$t4","$t5","$t6"]
next_register = 0
variables = {}

def get_register(variable):
    global next_register
    if variable not in variables:
        variables[variable] = register_map[next_register]
        next_register += 1
    return variables[variable]



def print_string(line):
    output = "li $v0, 11"
    for ch in line:
        ascii = ord(ch)
        output+= f" $li a0, {ascii}\n"
        output+="syscall\n"
    return output
    

def translate_line(line: str):
    original = line.strip()
    
    
    if not original or original.startswith("//") or original.startswith("#"):
        return ""
    
    if original.endswith(":"):
        label = original[:-1]
        return f"{label}:\n"
    if original.startswith("goto "):
        jump = original[len("goto "):].strip().strip(";")
        return f"j {jump}\n"
    if original.startswith("int "):
        instruction = line[4:].strip()
        if "=" in instruction:
            var,value = instruction.split("=")
            var = var.strip()
            value = value.strip().strip(";")
            register = get_register(var)
            return f"li{register}, {value}\n"
        else:
            return "" 
    if original.startswith("int main"):
        return "main:\n"
    if original.startswith("if ") and ">" in line and "goto" in line:
        return "" 
    return "XXXXXXXX\n"
    

def main(argv):
    if len(argv) < 3:
        print("Usage: toycompiler.py <input.c> <output.asm>")
        sys.exit(1)
    in_path, out_path = argv[1], argv[2]
    try:
        with open(in_path, "r") as fin, open(out_path, "w") as fout:
            for line_number, line in enumerate(fin, start=1):
                try:
                    fout.write(translate_line(line))
                except Exception as exc:
                    fout.write("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
                    sys.stderr.write(f"[Line {line_number}] {exc}\n")

    except FileNotFoundError as exc:
        print(f"File error: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
