from pylint import epylint as lint
from threading import get_native_id
from os import makedirs, remove
from sys import argv

makedirs('sandbox', exist_ok=True)

def scan(code):
    id = get_native_id()
    with open(f'sandbox/{id}.py', 'w') as f:
        f.write(code)
    out, _ = lint.py_run(f"sandbox/{id}.py " + "--errors-only --msg-template='{msg}'", 
        return_std=True)
    remove(f'sandbox/{id}.py')
    return out.getvalue().replace(f"************* Module {id}", '').replace('\n', '')[1:]

if __name__ == "__main__":
    print(scan(argv[1]) if len(argv) > 1 else "Use 'python PreEngine <code for test>'")