#!/usr/bin/env python3
import sys
import re

register_map = {
    0: "zero", 1: "at", 2: "v0", 3: "v1",
    4: "a0", 5:"a1" , 6: "a2", 7: "a3" ,
    8: "t0" , 9: "t1", 10: "t2", 11: "t3", 12: "t4", 13: "t5", 14: "t6", 15: "t7",
    16: "s0", 17:"s1", 18: "s2", 19:"s3", 20:"s4", 21: "s5", 22:"s6", 23:"s7",
    24:"t8", 25:"t9", 26:"k0", 27:"k1", 28:"gp", 29:"sp", 30:"fp", 30:"s8", 31:"ra" 
}

def translate_line():
    print("testing")
    

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
