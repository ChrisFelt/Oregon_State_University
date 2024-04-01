TITLE ASCII-Decimal Converter     (Proj6_feltc.asm)

; Author: Christopher Felt
; Last Modified: 09 March 2022
; OSU email address: feltc@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number: 6               Due Date: 13 March 2022
; Description: Displays the program title and instructions to the user, then prompts the user for 10 valid integers
;				from -2^31 to (2^31)-1. If the integer is invalid, displays an error message and prompts the user
;				for a new integer (the invalid integer is thrown away). The valid integer is read as an ASCII input, 
;				converted to decimal, and saved in an array. When filled, the array of integers is then converted 
;				from decimal to ASCII and displayed in a list to the user. Finally, the sum and truncated average 
;				of the integers are also displayed before the program terminates. Note: the sum and average values
;				also must fit in a signed 32-bit integer.

INCLUDE Irvine32.inc


; ---------------------------------------------------------------------------------------------------------------
;	Name: mGetString
;	
;	Displays a prompt to the user, then gets the user's keyboard input and saves it to memory.
;
;	Preconditions: none
;
;	Postconditions:	none
;
;	Receives: The prompt string (by reference) and a buffer by value
;
;	Returns: A byte string of the user's input and the number of bytes input (both by reference)
;
; ---------------------------------------------------------------------------------------------------------------
mGetString MACRO promptString, outString, buffer, bytesRead
; save registers
	push	EDX
	push	ECX
	push	EAX

	mov		EDX, promptString
	call	WriteString

	mov		EDX, outString
	mov		ECX, buffer
	call	ReadString

	; number of characters entered by ReadString is saved in EAX
	; move contents of EAX to bytesRead
	mov		bytesRead, EAX

	; restore registers
	pop		EAX
	pop		ECX
	pop		EDX
ENDM


; ---------------------------------------------------------------------------------------------------------------
;	Name: mDisplayString
;	
;	Displays a byte string to the screen character by character.
;
;	Preconditions: none
;
;	Postconditions:	none
;
;	Receives: The string to display by reference.
;
;	Returns: Nothing. The string is displayed to the screen.
;
; ---------------------------------------------------------------------------------------------------------------
mDisplayString MACRO inString
	; save registers
	push	EDX
	push	EAX
	push	ESI

	; prepare for string primitive instruction
	cld
	mov		ESI, inString

; iterate through the byte array and display each character
_outString:
	lodsb
	cmp		AL, 0
	je		_exitDisplayString
	call	WriteChar
	jmp		_outString

; restore registers and exit
_exitDisplayString:
	pop		ESI
	pop		EAX
	pop		EDX

ENDM


; ---------------------------------------------------------------------------------------------------------------
;	Name: mSignedDiv
;	
;	Finds and returns the signed quotient of the given dividend and divisor.
;
;	Preconditions: divisor cannot be 0!
;
;	Postconditions:	none
;
;	Receives: A dividend and divisor (by value).
;
;	Returns: The quotient (by reference).
;
; ---------------------------------------------------------------------------------------------------------------
mSignedDiv MACRO dividend, divisor, quotient
	push	EDX
	push	EBX
	push	EAX

	; move dividend to EAX
	mov		EAX, dividend
	; find quotient
	mov		EBX, divisor
	cdq
	idiv	EBX

	; store quotient in quotient variable
	mov		quotient, EAX

	pop		EAX
	pop		EBX
	pop		EDX
ENDM


; byte array length and buffer
; since this value is also used as the buffer for ReadString, effective array length is INPUT_MAX - 1
INPUT_MAX = 50

; ASCII decimal value for 0 and 9
ASCII_LO = 48
ASCII_HI = 57

; integer array size and read/write value count **CANNOT BE 0! (loops become infinite)
INT_COUNT = 10

.data
	
	exCred1		BYTE	"**EC: Program numbers each line of user input and displays a running total of the integers entered.",13,10,0
	
	; introduction and instructions
	intro1		BYTE	"ASCII-Decimal Converter  By Christopher Felt",13,10,0
	intro2		BYTE	"Please enter 10 integers.",13,10,0
	intro3		BYTE	"The integers may be positive or negative, but they must not exceed the size of a signed 32-bit integer.",13,10,0
	intro4		BYTE	"After you are done, I will display a list of the integers, their sum, and their average.",13,10,0
	
	; prompts and messages
	promptMsg	BYTE	"Please enter an integer: ",0
	errorMsg	BYTE	"ERROR: You did not enter a valid integer. Please try again: ",0
	runningSum	BYTE	"The running total of your integers is: ",0
	writeValMsg	BYTE	"Here are the valid integers you entered:",13,10,0
	sumMsg		BYTE	"The sum of your integers is: ",0
	avgMsg		BYTE	"The truncated average of your integers is: ",0

	farewell	BYTE	"Thanks for using the ASCII-Decimal Converter! Bye!",13,10,0

	; arrays and numeric variables
	userInput	BYTE	INPUT_MAX DUP(?)
	count		DWORD	0					; holds byte count of user input
	decValue	SDWORD	?
	decArray	SDWORD	INT_COUNT DUP(?)
	sum			SDWORD	0
	avg			SDWORD	0

.code
main PROC
	
	; display introductory messages
	push	OFFSET exCred1
	push	OFFSET intro1
	push	OFFSET intro2
	push	OFFSET intro3
	push	OFFSET intro4
	call	intro

	; prompt loop to call readVal
	; prepare counter and destination array
	mov		ECX, INT_COUNT
	mov		EDI, OFFSET decArray
	mov		EAX, 1					; track line number
	mov		EBX, 0					; track running sum

_prompt:
	; prepare parameters for and call readVal
	push	EAX
	push	OFFSET decValue
	push	OFFSET errorMsg
	push	OFFSET promptMsg
	push	OFFSET userInput
	push	OFFSET count
	call	readVal

	; EC: display running sum
	mov		EDX, OFFSET runningSum
	call	WriteString
	; calculate current sum of integers entered
	mov		EDX, decValue
	add		sum, EDX
	; write sum
	push	sum
	call	writeVal
	call	CrLf
	call	CrLf

	; move converted decimal value into array and increment to next element, then loop
	mov		EDX, decValue
	mov		[EDI], EDX
	add		EDI, TYPE decArray
	inc		EAX						; next line
	loop	_prompt

	call	CrLf

	; display integers message
	mov		EDX, OFFSET writeValMsg
	call	WriteString

	; prepare loop counter and source decArray
	mov		ECX, INT_COUNT
	mov		EDI, OFFSET decArray


; loop through each integer in decArray and call writeVal
_displayDecArray:
	push	[EDI]
	call	writeVal
	
	; write a comma and space after each number written besides the last
	cmp		ECX, 1
	je		_skipFormatting
	mov		AL, 44
	call	WriteChar
	mov		AL, 32
	call	WriteChar

	; point to next element in decArray
	add		EDI, TYPE decArray

_skipFormatting:
	loop	_displayDecArray

	call	CrLf
	call	CrLf

	; display sum
	mov		EDX, OFFSET sumMsg
	call	WriteString
	push	sum
	call	writeVal

	call	CrLf

	; calculate truncated average
	mSignedDiv sum, INT_COUNT, avg

	; display truncated avg
	mov		EDX, OFFSET avgMsg
	call	WriteString
	push	avg
	call	writeVal

	call	CrLf
	call	CrLf

	; display farewell message
	mov		EDX, OFFSET farewell
	call	WriteString


	Invoke ExitProcess,0	; exit to operating system
main ENDP


; ---------------------------------------------------------------------------------------------------------------
;	Name: intro
;	
;	Displays program introduction and instructions to user.
;
;	Preconditions: none
;
;	Postconditions:	none
;
;	Receives: The messages to display - intro1 to intro4 (by reference)
;
;	Returns: Nothing.
;
; ---------------------------------------------------------------------------------------------------------------
intro PROC USES EDX
	; prepare baseline pointer for stack
	push	EBP		
	mov		EBP, ESP

	; display intro1
	mov		EDX, [EBP + 24]
	call	WriteString
	call	CrLf

	; display exCred1
	mov		EDX, [EBP + 28]
	call	WriteString
	call	CrLf

	; display intro2
	mov		EDX, [EBP + 20]
	call	WriteString

	; display intro3
	mov		EDX, [EBP + 16]
	call	WriteString

	; display intro4
	mov		EDX, [EBP + 12]
	call	WriteString
	call	CrLf

	; restore EBP and exit procedure
	pop		EBP
	ret		16
intro ENDP


; ---------------------------------------------------------------------------------------------------------------
;	Name: readVal
;	
;	Invokes mGetString macro to prompt user for input, then converts the user's input byte array from ASCII to 
;	decimal format and saves it in memory. Checks that the input is a valid integer between -2^31 to (2^31)-1, 
;	and displays an error message and prompts the user for new input if it is not. Signs '+' and '-' are allowed 
;	at the beginning of the string.
;
;	Preconditions: requires macro mGetString
;
;	Postconditions:	none
;
;	Receives: Prompt and error messages, user input as a byte string, and count of the bytes entered (all by 
;				reference). Also receives the number of inputs to handle and the decimal value of the ASCII 
;				characters '0' and '9' as global constants.
;
;	Returns: The converted decimal value (passed by reference).
;
; ---------------------------------------------------------------------------------------------------------------
readVal PROC USES EAX EBX ECX EDX ESI EDI
	; prepare base pointer for stack
	push	EBP
	mov		EBP, ESP

	; EC: write line number
	push	[EBP + 52]
	call	writeVal
	mov		AL, 32
	call	WriteChar

	; invoke mGetString macro
	mGetString [EBP + 40], [EBP + 36], INPUT_MAX, [EBP + 32]


_validate:
	; raise error if nothing was entered (count = 0)
	mov		ECX, [EBP + 32]
	cmp		ECX, 0
	je		_errorFlag

	; convert ascii to decimal
	cld
	mov		ESI, [EBP + 36]
	mov		EBX, 0					; running total
	mov		EAX, 0					; clear EAX

	; load first char in userInput into AL and increment ESI
	lodsb
	dec		ECX

	; check first char for sign
	cmp		AL, 45                  ; ASCII 45 = '-'
	je		_setSign
	; if not negative, set sign flag (DL) to false
	mov		DL, 0
	cmp		AL, 43					; ASCII 43 = "+"
	je		_checkAfterSign

; loop through the string
_checkChar:
	; check that current char is 0-9 in ASCII
	cmp		AL, ASCII_LO
	jb		_errorFlag
	cmp		AL, ASCII_HI
	ja		_errorFlag

	; multiply current contents of ebx by 10 - raise error if OF flag set 
	imul	EBX, 10
	jo		_errorFlag

	; find the decimal value of the current char in AL
	sub		EAX, ASCII_LO

	; if integer is negative, subtract from running total
	cmp		DL, 1
	je		_subtract
	
	; otherwise, add current decimal value to running total and check for overflow (n > (2^31)-1)
	add		EBX, EAX
	jo		_errorFlag

; exit loop if ECX is 0. Otherwise prepare ESI, AL and continue loop
_increment:
	cmp		ECX, 0
	je		_saveAndExit
	lodsb
	dec		ECX
	jmp		_checkChar

; if sign is negative, set sign flag in DL to true
_setSign:
	mov		DL, 1

; for any string that begins with a + or -, check that it is not the only char entered
_checkAfterSign:
	cmp		ECX, 0
	je		_errorFlag
	; increment ESI and load next char into AL
	lodsb
	dec		ECX
	jmp		_checkChar  ; return to checkChar loop

; subtract current decimal value from running total
; check if negative value is too small to fit in SDWORD (n < -2^31)
_subtract:
	sub		EBX, EAX
	jo		_errorFlag
	jmp		_increment

; if error raised, reprompt user for new number
_errorFlag:
	; EC: write line number
	push	[EBP + 52]
	call	writeVal
	mov		AL, 32
	call	WriteChar
	; invoke mGetString macro with error msg
	mGetString [EBP + 44], [EBP + 36], INPUT_MAX, [EBP + 32]
	jmp		_validate

; otherwise, store decimal value of integer as decValue
_saveAndExit:
	mov		EDX, [EBP + 48]
	mov		[EDX], EBX

; restore EBP and exit procedure
	pop		EBP
	ret		20
readVal ENDP


; ---------------------------------------------------------------------------------------------------------------
;	Name: writeVal
;	
;	Converts a decimal value in memory to its ASCII equivalent and displays the result using the mDisplayString 
;	macro. Uses local variables to create and modify the byte array until it is displayed.
;
;	Preconditions: requires the mDisplayString macro
;
;	Postconditions:	none
;
;	Receives: The decimal value to be converted (passed by value), and a buffer max and the decimal value of the
;				ASCII character '0' as global constants.
;
;	Returns: Nothing.
;
; ---------------------------------------------------------------------------------------------------------------
writeVal PROC USES EAX EBX ECX EDX ESI EDI
	; declare local variables:
	; asciiString -> the destination string for the ascii equivalent of integer value passed to writeVal
	; tempString -> holds the intermediate reversed ascii equivalent
	; curInt -> track the current quotient after division
	; signFlag -> indicates integer sign. 0 = positive, 1 = negative
	LOCAL	asciiString[INPUT_MAX]:BYTE, tempString[INPUT_MAX]:BYTE, curInt:DWORD, signFlag:BYTE
	mov		signFlag, 0

	; prepare for string primitive stosb
	cld
	; load effective address instruction moves the address of the second operand into the first operand
	; OFFSET can't be used for local variables because the assembler doesn't know their address at assembly-time
	lea		EDI, tempString      
	; ECX counter tracks the number of elements in tempString
	mov		ECX, 0

	; check if integer parameter is negative
	mov		EAX, [EBP + 8]
	cmp		EAX, 0
	jl		_setSign

; generate a REVERSED string of the ascii equivalent of the integer
_decToAscii:
	inc		ECX
	; divide decimal value by 10 and add the remainder to tempString
	mov		EDX, 0
	mov		EBX, 10
	div		EBX

	; store the current quotient 
	mov		curInt, EAX

	; add 48 to remainder to find the ascii equivalent
	mov		EAX, EDX
	add		AL, ASCII_LO

	; store the ascii char in the current element of tempString
	stosb

	; restore current quotient to EAX, if 0, exit loop, otherwise repeat
	mov		EAX, curInt
	cmp		EAX, 0
	je		_reverseString
	jmp		_decToAscii

; set signFlag if integer is negative
_setSign:
	mov		signFlag, 1
	imul	EAX, -1
	jmp		_decToAscii

; store the contents of tempString in asciiString in REVERSE
_reverseString:
	; setup for reverse operation - tempString is now the source
	dec		EDI					; EDI must be decremented to point to last element in the array
	mov		ESI, EDI
	; destination string is asciiString
	lea		EDI, asciiString
	; append '-' first if the integer was negative
	mov		BL, signFlag
	cmp		BL, 1
	je		_appendSign

; read tempString in reverse and write contents to asciiString
_reverseLoop:
	; reverse order FROM tempString
	std
	lodsb
	; normal order TO asciiString
	cld
	stosb
	loop	_reverseLoop
	jmp		_appendNull

; append sign to beginning of asciiString, if necessary
_appendSign:
	mov		AL, 45
	cld
	stosb
	jmp		_reverseLoop

; terminate asciiString
; local variables don't appear to have initialized values in memory
_appendNull:
	; write null terminator to end of asciiString
	cld
	mov		AL, 0
	stosb

	; invoke mDisplayString with asciiString passed by reference
	lea		EAX, asciiString
	mDisplayString EAX

	; all done here
	ret		4
writeVal ENDP


END main
