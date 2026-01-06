import sys

def sleeplang_to_brainfuck(sleeplang_code):
    tokens = sleeplang_code.split()
    brainfuck = []
    
    for token in tokens:
        if token == 'zzZ':
            brainfuck.append('>')
        elif token == 'Zzz':
            brainfuck.append('<')
        elif token == 'ZZZ':
            brainfuck.append('+')
        elif token == 'zzz':
            brainfuck.append('-')
        elif token == 'zZz':
            brainfuck.append('.')
        elif token == 'ZzZ':
            brainfuck.append('[')
        elif token == 'zZZ':
            brainfuck.append(']')
    
    return ''.join(brainfuck)

def execute_brainfuck(code, show_bf=False):
    if show_bf:
        print("\n[Brainfuck]:", code)
    
    tape = [0] * 30000
    ptr = 0
    output = []
    loop_stack = []
    ip = 0
    
    while ip < len(code):
        cmd = code[ip]
        
        if cmd == '>':
            ptr += 1
        elif cmd == '<':
            ptr -= 1
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.':
            output.append(chr(tape[ptr]))
        elif cmd == '[':
            if tape[ptr] == 0:
                depth = 1
                while depth > 0:
                    ip += 1
                    if ip >= len(code):
                        raise SyntaxError("The loop needs to have a closure.")
                    if code[ip] == '[':
                        depth += 1
                    elif code[ip] == ']':
                        depth -= 1
            else:
                loop_stack.append(ip)
        elif cmd == ']':
            if tape[ptr] != 0:
                ip = loop_stack[-1]
            else:
                loop_stack.pop()
        
        ip += 1
    
    return ''.join(output)

def main():
    if len(sys.argv) != 3:
        print("--SleepLanguage--")
        print("| exec/e - execute | exec/d - simple debug | exec/t - only BrainF###k code |")
        print("\nUse: More about in the README file.")
        return
    
    command = sys.argv[1]
    source = sys.argv[2]
    
    if source.endswith('.slee'):
        with open(source, 'r') as f:
            sleeplang_code = f.read().strip()
    else:
        sleeplang_code = source
    
    bf_code = sleeplang_to_brainfuck(sleeplang_code)
    
    if command == 'exec/t':
        print("\n[T Mode]:")
        print(bf_code)
    
    elif command == 'exec/d':
        print("\n[Debug - D Mode BrainF###K]:")
        print(bf_code)
        print("\n[Execution]:")
        result = execute_brainfuck(bf_code, show_bf=False)
        print(result)
    
    elif command == 'exec/e':
        result = execute_brainfuck(bf_code, show_bf=False)
        print(result)
    
    else:
        print("Invalid command.")

if __name__ == "__main__":
    main()
