import time
import sys

def slow_type(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_banner():
    banner = """
    \033[1;32m===============================
        NEO-TERMINAL CALCULATOR
    ===============================\033[0m
    """
    print(banner)

def get_input():
    try:
        num1 = float(input("\033[1;36mEnter first number: \033[0m"))
        op = input("\033[1;36mChoose operation (+, -, *, /): \033[0m")
        num2 = float(input("\033[1;36mEnter second number: \033[0m"))
        return num1, op, num2
    except ValueError:
        slow_type("\033[1;31mInvalid input. Numbers only.\033[0m")
        return get_input()

def calculate(num1, op, num2):
    if op == '+':
        return num1 + num2
    elif op == '-':
        return num1 - num2
    elif op == '*':
        return num1 * num2
    elif op == '/':
        if num2 == 0:
            slow_type("\033[1;31mYou just tried to divide by zero...\033[0m", 0.05)
            slow_type("\033[1;33mEven the universe doesn't allow that.\033[0m", 0.05)
            return None
        return num1 / num2
    else:
        slow_type("\033[1;31mUnknown operation. Are you trying to break the matrix?\033[0m")
        return None

def main():
    show_banner()
    slow_type("Booting Neo-Terminal Calculator...\n", 0.02)
    num1, op, num2 = get_input()
    result = calculate(num1, op, num2)
    
    if result is not None:
        slow_type(f"\n\033[1;32mResult: {num1} {op} {num2} = {result}\033[0m", 0.04)

if __name__ == "__main__":
    main()
