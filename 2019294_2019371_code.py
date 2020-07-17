#COMPUTER ORGANIZATION
#CSE112
#ASSEMBLER PYTHON
#AMAN PRIYADARSHI 2019294
#MEDHAVI SABHERWAL 2019371



ec=0 #for counting no. of errors
errors=False
#FUNCTION FOR BINARY CONVERSION
def tobin(instr):
    return "{0:012b}".format(int(instr))
#LIST OF OPCODES PROVIDED
oplist=[
    "CLA", 
    "LAC", 
    "SAC", 
    "ADD", 
    "SUB", 
    "BRZ", 
    "BRN", 
    "BRP", 
    "INP", 
    "DSP", 
    "MUL", 
    "DIV", 
    "STP", 
]

opdict= {"CLA":'0000',
        "LAC":'0001',
        "SAC":'0010',
        "ADD":'0011',
        'SUB':'0100',
        'BRZ':'0101',
        'BRN':'0110',
        'BRP':'0111',
        'INP':'1000',
        'DSP':'1001',
        'MUL':'1010',
        'DIV':'1011',
        'STP':'1100',
        'LOOP':'1101',
        'DW':'1111'
         
        }

ifil=open("input.txt", "r")
instr=ifil.read().splitlines()


#INPUT FILE SHOULD BE NAMED "input.txt"
def pass1(instr):
    opcodes=[]
    global ec
    symbols=[]
    literals=[]
    global errors
    #flags for error checcking

    
    #stop=False
    end=False
    start=False
    location=0
    loc=[]
    
    for i in instr:
        if i=="START":
            start=True
            continue
        elif i=="END":
            end=True
            continue
        else:
            location=location+12
        binloc=tobin(location)
        reqmore=8-len(binloc)
        temp=""
        for p in range(reqmore):
            temp+="0"
            binloc=temp+binloc
        loc.append(i+" "+binloc)
        #print(binloc)

    parts=[]
    for j in loc:
        seg=j.split(" ")
        parts.append(seg)
    #print(parts)

    for k in parts:
        length=len(k)
        #print(length)
        if length==2:
            #possible opcodes:  CLA , STP
            if k[0]=="CLA":
                opcodes.append(k[0])
                continue
            elif k[0]=="STP":
                end=True
                opcodes.append(parts[0])
                continue
            else:
                literals.append(k[0])

        elif length==3:
            #possible cases for length 2
            if k[0]=="START" and k[1].isdigit():
                start=True
                opcodes.append(k[0])
                continue
            elif k[0] in oplist:
                opcodes.append(k[0])
                literals.append(k[1])
                #opcode+operand
                if k[0] in{"SAC", "INP", "STP", "BRZ", "BRN", "BRP"}:
                    if k[1] in literals:
                        print("ERROR: "+k[0]+ " CANNOT BE USED WITH: "+ k[1])
                    else:
                        opcode=k[0]+"    "+k[1]
                        opcodes.append(opcode)
                elif k[0] not in oplist:
                    print("INVALID INSTRUCTION: "+k[0]+"  "+k[1])
            elif k[1] in oplist:
                #label+opcode
                if k[1] in opcodes:
                    opcodes.append(k[1])
                    if k[0] in oplist:
                                   print("ERROR: "+k[0]+" SYMBOL NAME SAME AS OPCODE")
                    else:
                        symbols.append([k[0]])
                else:
                    print("ERROR: WRONG OPCODE"+ k[1])

            else:
                print("ERROR: "+k[0]+k[1]+" IS AN INVALID INSTRUCTION: " )
                errors=True
                ec+=1


        elif length==4:
            #opcode+operand+operand
            if k[0] in oplist:
                errors=True
                ec+=1
                print(k[0]+" PROIVIDED WITH MORE OPERANDS THAN REQUIRED")
                
            
            elif k[1] in oplist:
                
                #label+opcode+operand

                label=k[0]
                symbols.append(label)
                if k[1]=="CLA" or k[1]=="STP":
                    print("ERROR: "+k[1]+ " THIS OPCODE CANNOT BE PROVIDED HERE")
                else:
                    opcode=k[1]+"    "+k[2]
                    opcodes.append(opcode)
            elif k[2]=="DW":
                literal=k[0]+".   "+k[2]
                literals.append(literal)
                symbols.append(k[0])
            else:
                symbol=k[0]+"    "+k[2]
                literals.append(symbol)
                symbols.append(k[0])
        else:
            #if length of instruction is 4 or more, whicch is not possible:
            errors=True
            ec+=1
            print("INSTRUCTION CANNOT BE MORE THAN 3 WORDS LONG\n\n")
    if(start==False):
        errors=True
        ec+=1
        print("ERROR: START STATEMENT NOT FOUND\n\n")
    if(end==False):
        errors=True
        ec+=1
        print("ERROR: END STATEMENT NOT FOUND\n\n")
   #REMOVING REPEATING ELEMENTS FROM THE TABLES
    uopcodes=[]
    usymbols=[]
    uliterals=[]
    for i in opcodes: 
        if i not in uopcodes: 
            uopcodes.append(i) 
    for i in literals: 
        if i not in uliterals: 
            uliterals.append(i)
    for i in symbols: 
        if i not in usymbols: 
            usymbols.append(i)
    print("OPCODE TABLE\n\n", uopcodes, "\n\n")
    print("SYMBOL TABLE\n\n", usymbols, "\n\n")
    print("LITERAL TABLE\n\n", uliterals, "\n\n")
    
#PRINTING PASS 1 FOR TABLE CREATION AND ERROR HANDLING
print(pass1(instr))

ifil.close()

lit = ["0001","0011","0100","1010","1011"] # Opcode where literals and variables can be used
var = ["0001", "0010", "1000", "1001"] # Opcode where only variables can be used
branch = ["0101", "0110", "0111"] # Opcodes where only label can be used
opmust = ["1010", "1011", "1001", "0011", "0100", "0001"] # opcodes whose variables should have value

ofil=open("output.txt", "w")

def pass2(file):
    ctr=0
    y=0
    global end
    global start
    global stop
    global errors
    #flags for error checcking
    e=0
    pt=0
    with open(file) as reader:
        for pointer in reader:
            
            if "END" in pointer:
                end=True
                break
            elif "START" in pointer:
                start=True
                continue
            else:
                ctr=ctr+1
    with open(file) as reader:
        for pointer in reader:
            if "END" in pointer:
                e=y
                end=True
                continue
            elif "START" in pointer:
                start=True
                continue
            else:
                y=y+1
    with open(file) as reader:
        e=ctr
        for pointer in reader:
            if pt<e+2:
                pt=pt+1
                continue

            else:
                c=12*pt
                c=c-12
                #size of each instrucction is defined to be =12 bits
                pt=pt+1
                opdict[str(pointer).strip()]=str(tobin(c))
                
                
    with open(file) as reader:
        pt=0
        for pointer in reader:
            if "END" in pointer:
                end=True
                break

            elif "START" in pointer:
                start=True
                continue
            
            else:
                i=str(pointer).replace(':',' ')
                ele=str(pointer).split(' ')
                #getting space separated words
                if len(ele)==2:
                    #WRITING FINAL MACHINE CODE OUTPUT IN OUTPUT TEXT FILE
                    ofil.write(opdict[ele[0]]+' '+ opdict[ele[1].strip()]+"\n")
                    
                elif len(ele)==3:
                    ofil.write(opdict[ele[0][:4]]+' '+str(str(tobin(pt)))+"\n")
                    
                    ofil.write(opdict[ele[1]]+' '+ opdict[ele[2].strip()]+"\n")
                    
                pt=pt+12

if(errors==True):
        print("\n\nTHE ASSEMBLY CODE CONTAINS ERRORS, NOT PROCEEDING FOR SECOND PASS\n\n")
        print("TOTAL ERRORS= ")
        print(ec)
        
else:
    print("\n\nTHE ASSEMBLY CODE CONTAINS NO ERRORS, PROCEEDING FOR SECOND PASS\n\n ")
    print(pass2(r"input.txt"))
    print("OUTPUT FILE NAMED 'output.txt' CREATED")
    print("output.txt CCONTAINS OBJECT CODE EQUIVALENT TO ASSEMBLY CODE IN input.txt")



ofil.close()

#OUTPUT FILE WILL BE NAMED "output.txt"








