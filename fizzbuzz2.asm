Main:
li $t0,1
li $t1,100
Loop:
slt $at, $t1, $t0
bne $at, $zero, offset 63
li $t2,15
div $t0, $t2
mfhi $t4
beq $t4, $zero, offset 9
li $t2,3
div $t0, $t2
mfhi $t5
beq $t5, $zero, offset 23
li $t2,5
div $t0, $t2
mfhi $t6
beq $t6, $zero, offset 29
add $a0, $t0, $zero
li $v0,1
syscall
li $v0,11
li $a0,10
syscall
addi $t0, $t0, 1
j Loop
PrintFizzBuzz:
li $v0,11
li $a0,70
syscall
li $a0,105
syscall
li $a0,122
syscall
li $a0,122
syscall
li $a0,66
syscall
li $a0,117
syscall
li $a0,122
syscall
li $a0,122
syscall
li $a0,10
syscall
addi $t0, $t0, 1
j Loop
PrintFizz:
li $v0,11
li $a0,70
syscall
li $a0,105
syscall
li $a0,122
syscall
li $a0,122
syscall
li $a0,10
syscall
addi $t0, $t0, 1
j Loop
PrintBuzz:
li $v0,11
li $a0,66
syscall
li $a0,117
syscall
li $a0,122
syscall
li $a0,122
syscall
li $a0,10
syscall
addi $t0, $t0, 1
j Loop
Exit:
li $v0,10
syscall
