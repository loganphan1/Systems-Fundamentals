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

opcodes = {
    "001000":"addi" ,  
    "100011":"lw",  
    "101011": "sw",    
    "000101":"bne"  ,
    "000100":"beq"  ,
    "000010":"j"   ,
    "000011":"jal" ,
    "001111":"lui" ,
    "001101":"ori" 
}

functs = {
    "100000":"add"  ,  
    "011010":"div" ,
    "101010":"slt" ,
    "010000":"mfhi" ,
    "001000":"jr" ,
    "001100":"syscall" 
}

labels = {
    4194304:"Main",
    4194312:"Loop" ,
    4194400:"PrintFizzBuzz" ,
    4194484:"PrintFizz" ,
    4194536:"PrintBuzz" ,
    4194588:"Exit" 
}

def sign_extend_16bit(value):
    if value & 0x8000:
        return value - 0x10000
    else:
        return value
    
def disassemble_instruction(bits, current_address):
    bits=bits.strip()
    current_address=current_address
    if len(bits)!=32:
        return "INVALID, NOT 32 BITS\n"
    
    opcode = bits[:6]
    
    if opcode in opcodes:
        rs_bits = int(bits[6:11],2)
        rt_bits = int(bits[11:16],2)
        immediate_value = int(bits[16:],2)
        immediate_bits = sign_extend_16bit(immediate_value)
        mnemonic = opcodes[opcode]

        if mnemonic == "addi":
            if rs_bits == 0:
                return f"li ${register_map[rt_bits]},{immediate_bits}\n"
            else:
                return f"addi ${register_map[rt_bits]}, ${register_map[rs_bits]}, {immediate_bits}\n"
        elif mnemonic == "beq" or mnemonic == "bne":
            label_offset = current_address + 4 + immediate_bits*4
            label = labels.get(label_offset, f"offset {label_offset}")
            return f"{mnemonic} ${register_map[rs_bits]}, ${register_map[rt_bits]}, offset {immediate_bits}\n"
        elif mnemonic == "j":
          addr= int(bits[6:],2)
          label = labels[addr<<2]
          return f"j {label}\n"
        
        return "UNKNOWN INSTRUCTION\n"
    
    elif opcode == "000000":
        rs_bits = int(bits[6:11],2)
        rt_bits = int(bits[11:16],2)
        rd_bits = int(bits[16:21],2)
        shamt = bits[21:26]
        funct = bits[26:]

        if funct not in functs:
            return "UNKNOWN INSTRUCTION\n"
        
        mnemonic = functs[funct]
        if mnemonic == "syscall":
            return "syscall\n"
        elif mnemonic == "mfhi":
            return f"mfhi ${register_map[rd_bits]}\n"
        elif mnemonic == "div":
            return f"div ${register_map[rt_bits]}, ${register_map[rs_bits]}\n"
        elif mnemonic == "jr":
            return f"jr ${register_map[rs_bits]}\n"
        else:
            return f"{mnemonic} ${register_map[rd_bits]}, ${register_map[rs_bits]}, ${register_map[rt_bits]}\n"
    return "UNKNOWN INSTRUCTION \n"

def main(argv):
    if len(argv) < 3:
        print("Usage: assembler.py <input.bin> <output.asm>")
        sys.exit(1)
    in_path, out_path = argv[1], argv[2]

    current_address = 4194304
    try:
        with open(in_path, "r") as fin, open(out_path, "w") as fout:
            for line_number, line in enumerate(fin, start=1):
                try:
                    if current_address in labels:
                        fout.write(f"{labels[current_address]}:\n")
                    fout.write(disassemble_instruction(line, current_address))
                    current_address+=4
                except Exception as exc:
                    fout.write("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
                    sys.stderr.write(f"[Line {line_number}] {exc}\n")
    except FileNotFoundError as exc:
        print(f"File error: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
