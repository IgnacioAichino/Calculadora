;segmenet data
segment .data

segment .text 
    global  asm_mul

asm_mul: 
    enter   0,0
    mov     eax, [ebp + 8]
    mul     DWORD [ebp + 12]
    leave
    ret
