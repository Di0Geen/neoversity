org 0x100                  ; Вказуємо, що це програма .COM

section .data
    a db 5                 ; Значення a = 5
    b db 3                 ; Значення b = 3
    c db 2                 ; Значення c = 2
    resultMsg db 'Result: $'

section .text
_start:
    ; Обчислення виразу b - c + a
    mov al, [b]            ; Завантажуємо b в регістр AL
    sub al, [c]            ; Віднімаємо c
    add al, [a]            ; Додаємо a

    ; Зберігаємо результат перед виведенням тексту
    mov bl, al

    ; Виведення тексту "Result: "
    mov ah, 09h
    lea dx, resultMsg
    int 21h

    ; Перетворення результату в ASCII та його виведення
    mov al, bl
    add al, 30h
    mov dl, al
    mov ah, 02h
    int 21h

    ; Завершення програми
    mov ax, 4c00h
    int 21h