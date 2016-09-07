#!/usr/bin/python

# assembler for tramelblaze
# revision 1.1
# revision 1.2
# revision 1.3
# revision 1.4
# revision 1.5 (3/4/16)
# revision 1.6 (3/21/16 - 10:57AM)
# revision 2.0  8/29/16)
#
# john tramel 13 February 2016
# john tramel 17 February 2016 - cleaned up three token statements
# john tramel 18 February 2016 - changes to work with IDLE
# john tramel 19 February 2016 - changes to work with IDLE
#              1) Script now prompts for tba filename
#              2) Solved window 10 problem with not opening file ("\n")
#              3) Run under 2.7 and 3.4.3
# john tramel 20 February 2016 - adding file output for coe file
# john tramel 23 February 2016 - fixed recognition of END to drop last word
# john tramel 24 February 2016 - fixed comment only lines not starting col 0
#                                fixed generation of SHIFT/ROTATE codes
# john tramel 01 March 2016 - added FETCH/STORE for scratchpad ram
# john tramel 03 March 2016 - comments at end of line ";comment" caused problems
# john tramel 18 March 2016 - unmatched labels entering code - need to flag as error
# john tramel 19 March 2016 - error on bad opcodes/bad registers - need labels next
# john tramel 20 March 2016 - error on bad labels inserted
# john tramel 21 March 2016 - cleaned up lst file output
#                             removed .sim file (we simulate with built memory)
#                             created log file for assembler messages
#
# john tramel 29 August 2016 - renamed to trambler2.0
#
# Python's Integrated DeveLopment Environment
# https//docs.python.org/3.4/library/idle.html
# Python version 3.4.3
#
# written for csulb cecs 460
# architecture emulates xilinx picoblaze with 16 bit data paths

# code is case insensitive - assembler converts all to upper case
# any reference to a number is assumed to be hexadecimal

# limitations
#   do not place a label on same line as assembler directive ADDRESS
#   do not declare label to be R0..RF or r0..rf

#########################################################################################
#                      file management operations
# *.tba - source code extension (expected - not enforced()
# *.lst output - list file combining source code with machine code
# *.coe output - file format for feeding Xilinx memory builds
#########################################################################################

import os, sys

print ("Python Version: ",sys.version)

#########################################################################################
# check if source code (.tba) included in command line - if so extract name
#  if source code not included then prompt the user to enter the file name
#########################################################################################

if not (len(sys.argv) < 2):
   filename = sys.argv[1]
   print ("supplied: ",filename)
else:
   print ("Enter Filename: "),
   filename = sys.stdin.readline()
   print ("Prompted: ",filename)
filename = filename.replace("\n","")     

#########################################################################################
# open up the files created in the assembly process
#  if not able to open files notify user and exit the assembly
#########################################################################################

pos = filename.find('.')
base = filename[0:pos]

logfile = base+".log"
logf = open(logfile,"w")
if logf.closed:
   print ("Could not open file: ",logfile)
   print("Terminating assembly")
   sys.exit()

lstfile = base+".lst"
lstf = open(lstfile,"w")
if lstf.closed:
   print ("Could not open file: ",lstfile)
   logf.write("File: "+filename+ " does not exist"+'\n')
   print("Terminating assembly")
   logf.write("Terminating assembly")
   sys.exit()

tmpfile = base+".tmp"
tmpf = open(tmpfile,"w")
if tmpf.closed:
   print ("Could not open file: ",tmpfile)
   logf.write("File: "+filename+ " does not exist"+'\n')
   print("Terminating assembly")
   logf.write("Terminating assembly")
   sys.exit()

#########################################################################################
# verify that the file name entered exists
#  if not - notify user that file not found and exit the assembly
#########################################################################################

if not (os.path.isfile(filename)):
   print     ("File: ",filename, " does not exist")
   logf.write("File: "+filename+ " does not exist"+'\n')
   print     ("Terminating assembly")
   logf.write("Terminating assembly")
   logf.close()
   sys.exit()

#########################################################################################
#           Begin by setting up tables for look ups
#########################################################################################

#########################################################################################
#    set up array with all supported opcodes and their hex values
#    first hex value - immediate operand -- second hex value reg operand
#    list_size identifies # of elements - adjust if you add opcodes
#########################################################################################

list_size = 135
list_size_check = list_size - 1

list =         ['NOP',      '0000','0000']
list = list +  ['ADD',      '8200','0400']
list = list +  ['ADDC',     '8600','0800']
list = list +  ['AND',      '8A00','0C00']
list = list +  ['CALL',     '8E00','0000']
list = list +  ['CALLC',    '9000','0000']
list = list +  ['CALLNC',   '9200','0000']
list = list +  ['CALLZ',    '9400','0000']
list = list +  ['CALLNZ',   '9600','0000']
list = list +  ['COMP',     '9800','1A00']
list = list +  ['DISINT',   '1C00','0000']
list = list +  ['ENINT',    '1E00','0000']
list = list +  ['INPUT',    'A200','2000']
list = list +  ['JUMP',     'A400','0000']
list = list +  ['JUMPC',    'A600','0000']
list = list +  ['JUMPNC',   'A800','0000']
list = list +  ['JUMPZ',    'AA00','0000']
list = list +  ['JUMPNZ',   'AC00','0000']
list = list +  ['LOAD',     'AE00','3000']
list = list +  ['OR',       'B200','3400']
list = list +  ['OUTPUT',   'B800','3600']
list = list +  ['RETURN',   '3A00','0000']
list = list +  ['RETURNC',  '3C00','0000']
list = list +  ['RETURNNC', '3E00','0000']
list = list +  ['RETURNZ',  '4000','0000']
list = list +  ['RETURNNZ', '4200','0000']
list = list +  ['RETDIS',   '4400','0000']
list = list +  ['RETEN',    '4600','0000']
list = list +  ['RL',       '4800','0000']
list = list +  ['RR',       '4A00','0000']
list = list +  ['SL0',      '4C00','0000']
list = list +  ['SL1',      '4E00','0000']
list = list +  ['SLA',      '5000','0000']
list = list +  ['SLX',      '5200','0000']
list = list +  ['SR0',      '5400','0000']
list = list +  ['SR1',      '5600','0000']
list = list +  ['SRA',      '5800','0000']
list = list +  ['SRX',      '5A00','0000']
list = list +  ['SUB',      'DC00','5E00']
list = list +  ['SUBCY',    'E000','6200']
list = list +  ['TEST',     'E400','6600']
list = list +  ['XOR',      'E800','6A00']
list = list +  ['END',      '0000','0000']
list = list +  ['FETCH',    'F000','7200']
list = list +  ['STORE',    'F400','7600']

#########################################################################################
#            set up array with register replacement values
#          16 registers with 4 bits designating each register    
#########################################################################################

regs =         ['R0', '0']
regs = regs +  ['R1', '1']
regs = regs +  ['R2', '2']
regs = regs +  ['R3', '3']
regs = regs +  ['R4', '4']
regs = regs +  ['R5', '5']
regs = regs +  ['R6', '6']
regs = regs +  ['R7', '7']
regs = regs +  ['R8', '8']
regs = regs +  ['R9', '9']
regs = regs +  ['RA', 'A']
regs = regs +  ['RB', 'B']
regs = regs +  ['RC', 'C']
regs = regs +  ['RD', 'D']
regs = regs +  ['RE', 'E']
regs = regs +  ['RF', 'F']

#########################################################################################
#            define functions to assist in processing source code
#########################################################################################

#########################################################################################
# items entered into symbol table come from either EQU or LABELs
# an EQU is a string replacement whereas a label is an address reference
#########################################################################################
# function to search for symbol table entry
#    input:  string of symbol searching for 
#    output: 1) string of symbol searching for
#    output: 2) boolean 1:found, 0:not found
#    output: 3) string: EQU / number: LABEL
#########################################################################################

def findsymbol(str):

   index = 0
   found = 0
   foundval = ""
   while (index < len(symboltable)):
      if (symboltable[index] == str): 
         found = 1
         foundval = symboltable[index+1]
         index = index + 2
      else:
         index = index + 2
   return (str,found,foundval)

#########################################################################################
# function to search for opcode encoding
#    input:  string of opcode searching for 
#    output: 1) string of symbol searching for
#    output: 2) boolean 1:found, 0:not found
#    output: 3) opcode for immediate data
#    output: 4) opcode for register data
#########################################################################################

def findcode(str):

   index = 0
   found = 0
   foundCodeI = '0000'
   foundCodeR = '0000'

   while (index < list_size_check) and not(found):
      
      if (list[index] == str): 
         found = 1
         foundCodeI = list[index+1]
         foundCodeR = list[index+2]
      else:
         index = index + 3
   return (str,found,foundCodeI,foundCodeR)

#########################################################################################
# function to search for register encoding
#    input:  string of register searching for {R0, R1, ..., RE, RF}
#    output: 1) string of symbol searching for
#    output: 2) boolean 1:found, 0:not found
#    output: 3) number for register {0, 1, ..., 14, 15}
#########################################################################################

def findregs(str):

   index = 0
   found = 0
   foundval = '  '
   while not (found) and (index < 32):
      if (regs[index] == str): 
         found = 1
         foundval = regs[index+1]
      else:
         index = index + 2
   return (str,found,foundval)

#########################################################################################
# function to verify a label 
#   already failed findsymbol
#   so see if it is an opcode
#   then see if it is a register
#   then check if it is a four digit hex val
#   if not - then error out
#########################################################################################

def checksymbol(str):

   badsymbol = 1
   Valid = '0''1''2''3''4''5''6''7''8''9''A''B''C''D''E''F''a''b''c''d''e''f'

   (cksymb,ckfound,dum1,dum2) = findcode(str)
   if (ckfound):
      badsymbol = 0
   else:
      (cksymb,ckfound,dum1) = findregs(str)
      if (ckfound):
         badsymbol = 0
      else:
         badsymbol = 0
         if (len(str) == 4):
            for x in range(0,len(str)):
               if not (str[x] in Valid):
                  badsymbol = 1
         else:
            badsymbol = 1
   if (badsymbol):
      print     ("Error in Label Reference: ",str," not valid label")
      logf.write("Error in Label Reference: "+str+" not valid label"+'\n')
      print     ("Terminating assembly")
      logf.write("Terminating assembly")
      logf.close()
      sys.exit()
   return(badsymbol)

#########################################################################################
# function to convert integer to 4 digit hex
#    input:  integer value to convert to hex
#    output: 1) string of 4 digit hex value
#########################################################################################

def inttohex(str):

   s = hex(str)
   s = s[2:]
   if (len(s) == 1): s = "000"+s
   elif (len(s) == 2): s = "00"+s
   elif (len(s) == 3): s = "0"+s
   return(s)

#########################################################################################
#                      two pass assembler 
#########################################################################################

#########################################################################################
#    PASS 1 -- PASS 1 -- PASS 1 -- PASS 1 -- PASS 1 -- PASS 1 -- PASS 1 
#########################################################################################

#########################################################################################
#    resolve the symbol table
#    all labels are identified by their address
#########################################################################################

linenum = 0
symboltable = []

#########################################################################################
#    open the source file supplied by the user
#########################################################################################

srcf = open(filename,"r")

#########################################################################################
#   process the file one line at a time
#    read in the entire line and convert to all upper case
#    clear flags that identify if line has a label or is a comment
#########################################################################################

for line in srcf:
   line = line.upper()
   isalabel = 0
   isacomment = 0
   firstchar = line[0]

#########################################################################################
#  look for labels and comment only lines
#   labels must start in column 1 (first column)
#   check if entire line is a comment - regardless of column comment starts
#########################################################################################

   if (firstchar >= "A" and firstchar <= "Z"):
      isalabel = 1
   elif (";" in line):
      charpos = len(line) - len(line.lstrip())
      if (line[charpos] == ";"):
         isacomment = 1
   
   dotheloop = 1

#########################################################################################
#  remove parenthesis and comments so each token stands alone
#########################################################################################

   if not(isacomment):
      line = line.replace("(","")
      line = line.replace(")","")
      line = line.replace(",","")
      if (";" in line):
         sp = line.index(";") + 1
         line = line[:sp]+" "+line[sp:]    # no ;comment -> ; comment

#########################################################################################
#  split the line read up into tokens for processing
#   depending on the type of instruction there will be different # of tokens
#   remove any comments embedded at the end of a line with label/code
#########################################################################################

   cols = line.split()

   if (";" in cols):
      posi = cols.index(";")
      last = len(cols)
      del cols[posi:last]

#########################################################################################
#  while building symbol table exclude comments
#   first process lines with label and equates
#   if address directive then change the line number count (code address)
#   if there are no tokens (cols==0) then ignore the line
#########################################################################################

   if (isacomment): dotheloop = 0
   if (isalabel and 'EQU' in line): 
      symboltable = symboltable + [cols[0],cols[2]]
      dotheloop = 0
   if not (isacomment) and "ADDRESS" in cols: 
      linenum = int(cols[1],16)
      dotheloop = 0
   if not (cols):
      dotheloop = 0

#########################################################################################
#  iterative loop to process each of the lines with instructions
#   still pass 1 so only function is to create symbol table and
#   identify any errors that may be detected
#########################################################################################

   if (dotheloop):

#########################################################################################
#  instructions with a label
#   parse the symbols according to the number of symbols in the line
#    len(cols) == symbol count 
#      2: label and a single word instruction
#      3: label and a double word instruction
#      4: label and a triple word instruction
#
#    first enter the label into the symbol table                              <<<<<<<<<<<<<<<<<<<< check if already in table first
#     entry into table consists of the label and the instruction address
#
#   continued processing is for adjusting the instruction address only
#########################################################################################

      if (isalabel): 
         symboltable = symboltable + [cols[0],linenum]
         if len(cols) == 2:
            linenum = linenum + 1
         elif len(cols) == 3:
            if (cols[1][0:4] == 'JUMP' or cols[1][0:4] == 'CALL'):
               linenum = linenum + 2
            else:
               linenum = linenum + 1
         elif len(cols) == 4:
            (symb,foundit,newval)=findsymbol(cols[3])
            if (foundit):
               value = newval
            else:
               value = symb
            if (value in regs):
               linenum = linenum + 1
            else:
               linenum = linenum + 2

#########################################################################################
#  instructions without a label
#   parse the symbols according to the number of symbols in the line
#    len(cols) == symbol count 
#      1: a single word instruction
#      2: a double word instruction
#      3: a triple word instruction
#
#   continued processing is for adjusting the instruction address only
#########################################################################################

      else:
         if len(cols) == 1:
            linenum = linenum + 1
         elif len(cols) == 2:
            if (cols[0][0:4] == 'JUMP' or cols[0][0:4] == 'CALL'):
               linenum = linenum + 2
            else:
               linenum = linenum + 1
         elif len(cols) == 3:
            (symb,foundit,newval)=findsymbol(cols[2])
            if (foundit):
               value = newval
            else:
               value = symb
            if (value in regs):
               linenum = linenum + 1
            else:
               linenum = linenum + 2

#########################################################################################
# close the source file so we can open it again for the second pass
#########################################################################################

srcf.close()

#########################################################################################
#    PASS 2 -- PASS 2 -- PASS 2 -- PASS 2 -- PASS 2 -- PASS 2 -- PASS 2 
#########################################################################################

#########################################################################################
#    generate the machine code
#     this involves
#       1: converting assembly code into correct machine instruction
#       2: inserting register references into assembly code
#       3: all referenced addresses appear correctly in machine code
#########################################################################################

nextlinenum = 0
linenum = nextlinenum

#########################################################################################
#    open the source file supplied by the user
#########################################################################################

srcf = open(filename,"r")

#########################################################################################
#   process the file one line at a time
#    read in the entire line and convert to all upper case
#    clear flags that identify if line has a label or is a comment
#
#  source code input as 'line' - this echoed to lst file with machine code
#########################################################################################

for line in srcf:
   linep = line
   labelonly = 0
   isacomment = 0
   line = line.upper()
   if (";" in line):
      charpos = len(line) - len(line.lstrip())
      if (line[charpos] == ";"):
         isacomment = 1

#########################################################################################
#  remove parenthesis and comments so each token stands alone
#########################################################################################

   if not (isacomment):
      line = line.replace("(","")
      line = line.replace(")","")
      line = line.replace(",","")
      if (";" in line):
         sp = line.index(";") + 1
         line = line[:sp]+" "+line[sp:]

   cols = line.split()

   if (";" in cols):
      posi = cols.index(";")
      last = len(cols)
      del cols[posi:last]

#########################################################################################
#  identify lines that only have a label
#########################################################################################

   labelonly = len(cols)==1 and line[0]>='A'

#########################################################################################
#  send line just read to the list file
#########################################################################################

   lstf.write("               "+linep)

#########################################################################################
#  generate hex version of address and prepare to write to list file
#   all address references should be upper case for (A..F)
#########################################################################################

   hexval = inttohex(linenum)
   adrs   = hexval.upper()

#########################################################################################
#  process the tokens contained in cols
#   first adjust the line number when address directive encountered
#########################################################################################

   if not (isacomment):
      if "ADDRESS" in cols: 
         nextlinenum = int(cols[1],16)
         hexval = inttohex(nextlinenum)
         hexval = hexval.upper()

#########################################################################################
#  when an address directive is encountered fill the space with zeros
#########################################################################################

         loopit = linenum
         while (loopit < nextlinenum):
            tmpf.write('0000')
            loopit = loopit + 1

      if not ('EQU' in cols or 'ADDRESS' in cols or labelonly):
         if (cols):

#########################################################################################
#  replace any definition made in instruction
#   all symbols must be replaced by the referenced address 
#   walk through every token in the line replacing when found
#   symb: looked for symbol, foundit then replace it
#   continue error checking on labels 
#########################################################################################

            index = 0
            while (index < len(cols)):
               (symb,foundit,newval) = findsymbol(cols[index])
               if (foundit): 
                  cols[index] = newval
               else:
                  checksymbol(cols[index])
               index = index + 1

#########################################################################################
#  first strip any line that is a comment or empty
#   findcode returns the machine code for the instruction
#   at this point cols just tokens - regs replaced, labels replaced
#########################################################################################

#########################################################################################
#  find opcode for lines with single token
#########################################################################################

            if (len(cols) == 1) and (line[0] < 'A'):    # only opcode
               (str,foundit,foundCodeI,foundCodeR)=findcode(cols[0])
               if not foundit:
                  print     ("Error in Opcode Reference: ",str," not valid opcode")
                  logf.write("Error in Opcode Reference: "+str+" not valid opcode"+'\n')
                  print     ("Terminating assembly")
                  logf.write("Terminating assembly")
                  logf.close()
                  sys.exit()
               nextlinenum = linenum + 1

#########################################################################################
#  find opcode for lines with two tokens
#########################################################################################

            elif (len(cols) == 2) and (line[0] < 'A'):   # jump/call/r/s
               (str,foundit,foundCodeI,foundCodeR)=findcode(cols[0])
               if not foundit:
                  print     ("Error in Opcode Reference: ",str," not valid opcode")
                  logf.write("Error in Opcode Reference: "+str+" not valid opcode"+'\n')
                  print     ("Terminating assembly")
                  logf.write("Terminating assembly")
                  logf.close()
                  sys.exit()
               if ('JUMP' in line or 'CALL' in line):
                  nextlinenum = linenum + 2
               else:
                  nextlinenum = linenum + 1
            elif (len(cols) == 2) and (line[0] >= 'A'):  # label and opcode
               (str,foundit,foundCodeI,foundCodeR)=findcode(cols[1])
               if not foundit:
                  print     ("Error in Opcode Reference: ",str," not valid opcode")
                  logf.write("Error in Opcode Reference: "+str+" not valid opcode"+'\n')
                  print     ("Terminating assembly")
                  logf.write("Terminating assembly")
                  logf.close()
                  sys.exit()
               cols.pop(0)                               # loose label
               nextlinenum = linenum + 1

#########################################################################################
#  find opcode for lines with three tokens
#########################################################################################

            elif (len(cols) == 3) and (line[0] < 'A'):   # opcode r/r | r/k
               (str,foundit,foundCodeI,foundCodeR)=findcode(cols[0])
               if not foundit:
                  print     ("Error in Opcode Reference: ",str," not valid opcode")
                  logf.write("Error in Opcode Reference: "+str+" not valid opcode"+'\n')
                  print     ("Terminating assembly")
                  logf.write("Terminating assembly")
                  logf.close()
                  sys.exit()
               if not (cols[2][0] == 'R'):
                  nextlinenum = linenum + 2
               else:
                  nextlinenum = linenum + 1
                  foundCodeI = foundCodeR
            elif (len(cols) == 3) and (line[0] >= 'A'):  # label jump/call/r/s
               (str,foundit,foundCodeI,foundCodeR)=findcode(cols[1])
               if not foundit:
                  print     ("Error in Opcode Reference: ",str," not valid opcode")
                  logf.write("Error in Opcode Reference: "+str+" not valid opcode"+'\n')
                  print     ("Terminating assembly")
                  logf.write("Terminating assembly")
                  logf.close()
                  sys.exit()
               if ('JUMP' in line or 'CALL' in line):
                  nextlinenum = linenum + 2
               else:
                  nextlinenum = linenum + 1
               cols.pop(0)                               # loose label

#########################################################################################
#  find opcode for lines with four tokens
#########################################################################################

            elif (len(cols) == 4):                       # label opcode r/r | r/k
               (str,foundit,foundCodeI,foundCodeR)=findcode(cols[1])
               if not foundit:
                  print     ("Error in Opcode Reference: ",str," not valid opcode")
                  logf.write("Error in Opcode Reference: "+str+" not valid opcode"+'\n')
                  print     ("Terminating assembly")
                  logf.write("Terminating assembly")
                  logf.close()
                  sys.exit()
               if not (cols[3][0]=='R'):
                  nextlinenum = linenum + 2
               else:
                  nextlinenum = linenum + 1
                  foundCodeI = foundCodeR
               cols.pop(0)                               # loose label

#########################################################################################
#  build the output data
#   line still has the original line from the source code
#   cols has been parsed all symbols have been substituted
#   all labels have been removed from parsed code - no longer needed
#########################################################################################

#########################################################################################
#  single word instructions: DISINT --  ENINT --  RETURN(s)
#########################################################################################

            if ((len(cols)==1) and cols[0] != 'END'):
               tmpf.write(foundCodeI)
               lstf.write(adrs+" ")
               lstf.write(foundCodeI)

#########################################################################################
#  double word instructions: CALL(s) AAA --  JUMP(s) AAA --  Rotates --  Shifts
#########################################################################################

            if (len(cols)==2):
               if (("JUMP" in cols[0]) or ("CALL" in cols[0])):
                  
#########################################################################################
#  process JUMP(s) and CALL(s) - double word instructions
#########################################################################################

                  tmpf.write(foundCodeI)
                  lstf.write(adrs+" ")
                  lstf.write(foundCodeI+" ")
                  symb = cols[1]
                  tmpf.write(inttohex(symb))
                  lstf.write(inttohex(symb)+'\n')
                  
#########################################################################################
#  process SHIFT(s) and ROTATES(s) - double word instructions
#########################################################################################

               else:
                  (sent,foundit,letter) = findregs(cols[1])
                  if not foundit:
                     print     ("Error in Register Reference: ",sent," not in range 0..F")
                     logf.write("Error in Register Reference: "+sent+" not in range 0..F"+'\n')
                     print     ("Terminating assembly")
                     logf.write("Terminating assembly")
                     logf.close()
                     sys.exit()
                  built = foundCodeI[0:3]+letter
                  tmpf.write(built)         # send opcode with 1st R
                  lstf.write(adrs+" ")
                  lstf.write(built+'\n')    # send opcode with 1st R
                  
#########################################################################################
#  process ALUOP RA, RB --  ALUOP RA, KKK  INPUT RA, (RB) ---  INPUT RA, KKK
#   - triple word instructions  
#########################################################################################

            if (len(cols)==3):
               (sent,foundit,letter) = findregs(cols[1])
               if not foundit:
                     print     ("Error in Register Reference: ",sent," not in range 0..F")
                     logf.write("Error in Register Reference: "+sent+" not in range 0..F"+'\n')
                     print     ("Terminating assembly")
                     logf.write("Terminating assembly")
                     logf.close()
                     sys.exit()
               built = foundCodeI[0:3]+letter
               if (cols[2][0]=='R'):
                  (sent,foundit,letter) = findregs(cols[2])
                  if not foundit:
                     print     ("Error in Register Reference: ",sent," not in range 0..F")
                     logf.write("Error in Register Reference: "+sent+" not in range 0..F"+'\n')
                     print     ("Terminating assembly")
                     logf.write("Terminating assembly")
                     logf.close()
                     sys.exit()
                  sent = built[0:2]+letter+built[3]
                  tmpf.write(sent)         # send opcode with 1st R and 2nd R
                  lstf.write(sent+'\n')    # send opcode with 1st R and 2nd R
               else:
                  tmpf.write(built)         # send opcode with 1st R
                  lstf.write(adrs+" ")
                  lstf.write(built+" ")     # send opcode with 1st R
                  tmpf.write(cols[2])       # here send the kkkk
                  lstf.write(cols[2]+'\n')  # here send the kkkk

      linenum = nextlinenum

#########################################################################################
#  end of iterative loop performing pass two
#########################################################################################

#########################################################################################
#  clean up files
#########################################################################################

tmpf.close()
lstf.close()
srcf.close()
logf.write("Successful assembly"+'\n')
logf.close()

#########################################################################################
#  create .coe file with text expected by Xilinx memory generator
#########################################################################################

fr  = open(base+".tmp","r")
fw = open(base+".coe","w")

fw.write("memory_initialization_radix = 16;\n")
fw.write("memory_initialization_vector = \n")
linecount = 0
count = 0
while True:
   ch = fr.read(1)
   if not ch: break
   fw.write(ch)
   count = count + 1
   if (count % 4 == 0):
      fw.write(' ')
   if (count == 64):
      count = 0
      linecount = linecount + 1
      if (linecount == 64*4): break
      fw.write('\n')

fw.write(";")
fr.close()
fw.close()
#os.remove(base+".tmp")


