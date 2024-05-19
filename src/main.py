from src.parser.python_parser import parse_code

def main():
    test_code = """
    x = 10
    if x < 20:
        print(x)
        if x < 15:
            x = 5
    def func(a, b):
        y = a + b
        print(y)
    """
    parse_code(test_code)

if __name__ == "__main__":
    main()
