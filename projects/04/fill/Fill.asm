// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
    @24575
    D=A
    @n
    M=D             // n=24575 (Last Screen Memory)
    @SCREEN
    D=A
    @current
    M=D             // addresses to current screen Memory in loop
    @prev_key
    M=0             // {0: not pressed, -1: pressed}, default to 0

(MAIN_LOOP)
    @KBD
    D=M
    @CHECK_0    
    D;JEQ           // check if key is pressed
    @prev_key 
    D=M
    @CHANGE
    D;JEQ           // check if previously key was not pressed
    @MAIN_LOOP
    0;JMP

    (CHECK_0)
        @prev_key
        D=M
        @MAIN_LOOP
        D;JEQ           // check if previously key was pressed
        @CHANGE
        0;JMP

    (CHANGE)
        @current
        D=M
        @n
        D=M-D
        @KEY_CHANGE
        D;JLT
        @current
        A=M
        M=!M                // toggle current screen Memory
        @current
        M=M+1               // current address increment
        @CHANGE
        0;JMP
        (KEY_CHANGE)
            @prev_key       // toggle if change occured
            M=!M
            @SCREEN
            D=A
            @current        // current address Reset
            M=D

(STOP)
    @MAIN_LOOP
    0;JMP