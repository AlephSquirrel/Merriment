'''
    Interpreter for the language Merriment
    Author: AlephSquirrel
    Version: 0.3
'''

import sys, re, argparse

def err_message(e):
    sys.stderr.write('Error: ' + e)
    sys.exit(1)

class Codebox:
    def __init__(self, name, width, height, entry_col, code):
        self.name = name
        self.width = width
        self.height = height
        self.entry_col = entry_col
        self.code = code

def read_code(filename):
    '''
        Reads code from {filename}.merry.
        Returns a dictionary mapping commands to Codebox objects.
    '''
    try:
        f = open(filename + ".merry", 'r')
        lines = f.readlines()
        f.close()
    except IOError:
        err_message(f"Can't read file {filename}.merry")
    
    codeboxes = dict()
    in_codebox = False
    
    for line_num, line in enumerate(lines):
        line = line.rstrip('\n\r')
        if in_codebox:
            if len(line) != codebox_width:
                err_message(f"Incorrect width: file {filename}, line {line_num + 1}")
            codebox_lines += 1
            if codebox_lines == 2:
                # Parse codebox name
                name_match = re.fullmatch("# *(.*?) *#", line)
                if name_match:
                    name = name_match.group(1)
                else:
                    err_message(f"Bad codebox name: file {filename}, line {line_num + 1}")
            elif codebox_lines == 3:
                # Parse codebox entry line
                entry_match = re.fullmatch("#=*v=*#", line)
                if entry_match:
                    entry_col = entry_match.group(0).find('v') - 1
                else:
                    err_message(f"Bad entry point: file {filename}, line {line_num + 1}")
            elif re.fullmatch("#*", line):
                # Parse bottom border of codebox
                codeboxes[name[:1]] = Codebox(name, codebox_width - 2, len(code), entry_col, code)
                in_codebox = False
            else:
                # Parse any lines inside of the codebox
                row_match = re.fullmatch("#(.*)#", line)
                if row_match:
                    code.append(row_match.group(1))
                else:
                    err_message(f"Bad codebox row: file {filename}, line {line_num + 1}")
        else:
            if re.fullmatch("#+", line):
                # Top border of codebox
                in_codebox = True
                codebox_width = len(line)
                codebox_lines = 1
                code = []
            else:
                # Parse import statement
                import_match = re.fullmatch("{(.*)}", line)
                if import_match: codeboxes.update(read_code(import_match.group(1)))
    return codeboxes

def run_code(codeboxes, stack, vstack, name = ''):
    if name not in codeboxes:
        if name == '':
            err_message("No main codebox found")
        else:
            err_message(f"Command not found: {name}")
    codebox = codeboxes[name]
    x,y = codebox.entry_col, 0
    vx,vy = 0,1
    string_mode = False
    
    while True:
        # Test for out-of-bounds
        if (x < 0) or (x >= codebox.width) or (y < 0) or (y >= codebox.height):
            if name:
                err_message(f"Out of bounds in codebox {codebox.name}")
            else:
                err_message("Out of bounds in main codebox")
        
        command = codebox.code[y][x]
        if string_mode:
            if command == '"':
                string_mode = False
            else:
                stack.append(ord(command))
        elif command == ' ':
            "NOP"
        elif command.isdigit():
            # Digits
            stack.append(int(command))
        elif command == '↊':
            # Push 10
            stack.append(10)
        elif command == '↋':
            # Push 11
            stack.append(11)
        elif command in "+-*,":
            # Arithmetic operations
            a = stack.pop()
            b = stack.pop()
            if command == '+':
                stack.append(a + b)
            elif command == '-':
                stack.append(b - a)
            elif command == '*':
                stack.append(a * b)
            elif command == ',':
                stack.append(b // a)
        elif command == '`':
            # Is positive?
            a = stack.pop()
            stack.append(int(a > 0))
        elif command == ':':
            # Duplicate
            a = stack.pop()
            for _ in range(2): stack.append(a)
        elif command == '.':
            # Pop
            stack.pop()
        elif command == '~':
            # Swap
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)
        elif command == '{':
            # Move value from velocity stack to data stack
            stack.append(vstack.pop())
        elif command == '}':
            # Move value from data stack to velocity stack
            vstack.append(stack.pop())
        elif command == '@':
            # Return
            return
        elif command == '"':
            string_mode = True
        elif command == 'i':
            # Input 1 character from stdin.
            # If at EOF, return -1.
            char = sys.stdin.read(1)
            stack.append(ord(char) if char else -1)
        elif command == 'o':
            # Output character
            print(end=chr(stack.pop()))
        elif command == '!':
            # Debug
            print("! DEBUG !")
            print(f"Codebox: {codebox.name}")
            print(f"Position: {(x, y)}")
            print(f"Velocity: {(vx, vy)}")
            print(f"Data stack: {stack}")
            print(f"Velocity stack: {vstack}")
        else:
            # Push velocity to velocity stack, execute command, pop new velocity from velocity stack.
            vstack.append(vx)
            vstack.append(vy)
            run_code(codeboxes, stack, vstack, command)
            vy = vstack.pop()
            vx = vstack.pop()
        # Update IP position
        x += vx; y += vy

parser = argparse.ArgumentParser(description='Run a Merriment program')
parser.add_argument('progname', metavar='progname', type=str,
    help='the filename of the Merriment program to run')
args = parser.parse_args()

codeboxes = read_code(args.progname)
run_code(codeboxes, [], [])