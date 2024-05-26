from python_parser import program_node
from code_generator import generate_rust

def main():
    rust_code = generate_rust(program_node)
    print("Generated Rust code:")
    print(rust_code)

if __name__ == "__main__":
    main()
