#!/usr/bin/env python3
import sys
import re

register_map = {
    "zero": 0, "at": 1, "v0": 2, "v1": 3,
    "a0": 4, "a1": 5, "a2": 6, "a3": 7,
    "t0": 8, "t1": 9, "t2": 10, "t3": 11, "t4": 12, "t5": 13, "t6": 14, "t7": 15,
    "s0": 16, "s1": 17, "s2": 18, "s3": 19, "s4": 20, "s5": 21, "s6": 22, "s7": 23,
    "t8": 24, "t9": 25, "k0": 26, "k1": 27, "gp": 28, "sp": 29, "fp": 30, "s8": 30, "ra": 31,
}

opcodes = {
    "addi": "001000",  
    "lw":   "100011",  
    "sw":   "101011",  
    "li":   "001000",  
    "bne":  "000101",
    "beq":  "000100",
    "j":    "000010",
    "jal": "000011",
    "lui": "001111",
    "ori": "001101"
}

functs = {
    "add":  "100000",  
    "div": "011010",
    "slt": "101010",
    "mfhi": "010000",
    "jr": "001000",
    "syscall": "001100"
}

labels = {
    "Main": 4194304,
    "Loop": 4194312,
    "PrintFizzBuzz": 4194400,
    "PrintFizz": 4194484,
    "PrintBuzz": 4194536,
    "Exit": 4194588,

}

def compute_branch_offset(label_addr: int, current_addr: int) -> int:
    return (label_addr -(current_addr+4)) // 4
    

def compute_jump(label_addr: int) -> int:
    return label_addr >>2

def to_bits(value: int, width: int) -> str:
    mask = (1 << width) - 1
    return format(value & mask, f"0{width}b")

def parse_register(token: str) -> int:
    if not token.startswith("$"):
        raise ValueError(f"Invalid register: {token}")
    name = token[1:].lower()
    if name.isdigit():
        num = int(name)
        if 0 <= num <= 31:
            return num
        raise ValueError(f"Register out of range: {token}")
    if name in register_map:
        return register_map[name]
    raise ValueError(f"Unknown register: {token}")

def strip_comments(line: str) -> str:
    return line.split("#", 1)[0].strip()

def parse_mem_operand(token: str) -> tuple[int, int]:
    m = re.fullmatch(r"([+-]?(?:0x[0-9a-fA-F]+|\d+))\(\s*(\$\w+)\s*\)", token)
    if not m:
        raise ValueError(f"Bad memory operand: {token}")
    offset_str, base_reg = m.groups()
    return int(offset_str, 0), parse_register(base_reg)

def translate_line(line: str, current_addr: int) -> str:
    line = strip_comments(line)
    if not line or line.endswith(":"):
        return ""
    tokens = line.replace(",", " ").split()
    mnemonic = tokens[0].lower()

    if mnemonic == "addi" and len(tokens) == 4 :
        _, rt_tok, rs_tok, imm_tok = tokens
        opcode = opcodes[mnemonic]
        rs_bits = to_bits(parse_register(rs_tok), 5)
        rt_bits = to_bits(parse_register(rt_tok), 5)
        imm_bits = to_bits(int(imm_tok, 0), 16)
        return f"{opcode}{rs_bits}{rt_bits}{imm_bits}\n"
    
    if mnemonic == "li" and len(tokens) == 3:
        _, rt_tok, imm_tok = tokens
        opcode = opcodes[mnemonic]
        rs_bits = "00000"
        rt_bits = to_bits(parse_register(rt_tok), 5)
        imm_bits = to_bits(int(imm_tok, 0), 16)
        return f"{opcode}{rs_bits}{rt_bits}{imm_bits}\n"
    
    if mnemonic in ("lw", "sw") and len(tokens) == 3:
        _, rt_tok, mem_tok = tokens
        offset, base_reg = parse_mem_operand(mem_tok)
        opcode = opcodes[mnemonic]
        rs_bits = to_bits(base_reg, 5)
        rt_bits = to_bits(parse_register(rt_tok), 5)
        imm_bits = to_bits(offset, 16)
        return f"{opcode}{rs_bits}{rt_bits}{imm_bits}\n"
    
    if mnemonic == "bne" and len(tokens) == 4:
        _, rs_tok, rt_tok, label_tok = tokens
        opcode = opcodes[mnemonic]
        rs_bits = to_bits(parse_register(rs_tok), 5)
        rt_bits = to_bits(parse_register(rt_tok), 5)
        offset= compute_branch_offset(labels[label_tok], current_addr)
        imm_bits = to_bits(offset,16)
        return f"{opcode}{rs_bits}{rt_bits}{imm_bits}\n"

    if mnemonic == "beq" and len(tokens) == 4:
        _, rs_tok, rt_tok, label_tok = tokens
        opcode = opcodes[mnemonic]
        rs_bits = to_bits(parse_register(rs_tok),5)
        rt_bits = to_bits(parse_register(rt_tok),5)
        offset= compute_branch_offset(labels[label_tok], current_addr)
        imm_bits = to_bits(offset, 16)
        return f"{opcode}{rs_bits}{rt_bits}{imm_bits}\n"

    if mnemonic == "j" and len(tokens) == 2:
        _, label_tok = tokens
        opcode = opcodes[mnemonic]
        addr_bits = to_bits(compute_jump(labels[label_tok]),26)
        return f"{opcode}{addr_bits}\n"
    
    if mnemonic == "jal" and len(tokens) == 2:
        _, label_tok = tokens
        opcode = opcodes[mnemonic]
        addr_bits = to_bits(compute_jump(labels[label_tok]),26)
        return f"{opcode}{addr_bits}\n"
    
    if mnemonic == "la" and len(tokens) == 3:
        _, rt_tok, label_tok = tokens
        rt_bits= to_bits(parse_register(rt_tok),5)
        rs_bits = "00000"
        addr_bits = labels[label_tok]
        upper_val = (addr_bits>>16) & 0xFFFF
        lower_val = addr_bits & 0xFFFF
        upper_bits = to_bits(upper_val,16)
        lower_bits = to_bits(lower_val,16)
        opcode_lui = opcodes["lui"]
        opcode_ori = opcodes["ori"]
        lui_bin = f"{opcode_lui}{rs_bits}{rt_bits}{upper_bits}\n"
        ori_bin = f"{opcode_ori}{rt_bits}{rt_bits}{lower_bits}\n"
        return lui_bin+ori_bin


    if mnemonic == "add" and len(tokens) == 4:
        _, rd_tok, rs_tok, rt_tok = tokens
        opcode = "000000"
        rs_bits = to_bits(parse_register(rs_tok), 5)
        rt_bits = to_bits(parse_register(rt_tok), 5)
        rd_bits = to_bits(parse_register(rd_tok), 5)
        shamt_bits = "00000"
        funct_bits = functs[mnemonic]
        return f"{opcode}{rs_bits}{rt_bits}{rd_bits}{shamt_bits}{funct_bits}\n"
    
    if mnemonic == "div" and len(tokens) == 3:
        _, rt_tok, rs_tok, = tokens 
        opcode = "000000" 
        rs_bits = to_bits(parse_register(rs_tok),5)
        rt_bits = to_bits(parse_register(rt_tok),5)
        rd_bits = "00000"
        shamt_bits = "00000"
        funct_bits = functs[mnemonic]
        return f"{opcode}{rs_bits}{rt_bits}{rd_bits}{shamt_bits}{funct_bits}\n"

    if mnemonic == "slt" and len(tokens) == 4:
        _, rd_tok, rs_tok, rt_tok = tokens
        opcode = "000000"
        rs_bits = to_bits(parse_register(rs_tok), 5)
        rt_bits = to_bits(parse_register(rt_tok),5)
        rd_bits = to_bits(parse_register(rd_tok),5)
        shamt_bits = "00000"
        funct_bits = functs[mnemonic]
        return f"{opcode}{rs_bits}{rt_bits}{rd_bits}{shamt_bits}{funct_bits}\n"
    
    if mnemonic == "mfhi" and len(tokens) == 2:
        _, rd_tok = tokens
        opcode = "000000"
        rs_bits = "00000"
        rt_bits = "00000"
        rd_bits = to_bits(parse_register(rd_tok),5)
        shamt_bits = "00000"
        funct_bits = functs[mnemonic]
        return f"{opcode}{rs_bits}{rt_bits}{rd_bits}{shamt_bits}{funct_bits}\n"

    if mnemonic == "jr" and len(tokens) == 2:
        _, rs_tok = tokens
        opcode = "000000"
        rs_bits = to_bits(parse_register(rs_tok),5)
        rt_bits = "00000"
        rd_bits = "00000"
        shamt_bits = "00000"
        funct_bits = functs[mnemonic]
        return f"{opcode}{rs_bits}{rt_bits}{rd_bits}{shamt_bits}{funct_bits}\n"
    
    if mnemonic == "syscall" and len(tokens) == 1:
        _ = tokens
        opcode = "000000"
        rs_bits = "00000"
        rt_bits = "00000"
        rd_bits = "00000"
        shamt_bits = "00000"
        funct_bits = functs[mnemonic]
        return f"{opcode}{rs_bits}{rt_bits}{rd_bits}{shamt_bits}{funct_bits}\n"
    
    return "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"

def main(argv):
    if len(argv) < 3:
        print("Usage: assembler.py <input.asm> <output.mc>")
        sys.exit(1)
    in_path, out_path = argv[1], argv[2]
    try:
        with open(in_path, "r") as fin, open(out_path, "w") as fout:
            for line_number, line in enumerate(fin, start=1):
                try:
                    current_addr = 4194304 + 4 * (line_number - 1)
                    fout.write(translate_line(line,current_addr))
                except Exception as exc:
                    fout.write("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
                    sys.stderr.write(f"[Line {line_number}] {exc}\n")
    except FileNotFoundError as exc:
        print(f"File error: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
