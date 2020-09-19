from lexer import LangLexer
from parser import LangParser
from interpreter import Process
import sys

import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-m", "--mode", required=True,
                help="Mode of parsing the grammar")

ap.add_argument("-f", "--file", required=True,
                help="Path to file with code of program")

args = vars(ap.parse_args())

mode = args['mode']
file_path = args['file']

def repl():
    lexer = LangLexer()
    parser = LangParser()
    env = {}
    program = Process((), env=env)
    while True:
        try:
            text = input('>> ')
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        if text:
            tokens = lexer.tokenize(text)

            try:
                tree = parser.parse(tokens)
                program.tree = tree
                program.run()
            except TypeError as e:
                if str(e).startswith("'NoneType' object is not iterable"):
                    print("Syntax Error")
                else:
                    print(e)


def exec_file(file_path):
    lexer = LangLexer()
    parser = LangParser()
    with open(file_path) as opened_file:
        tokens = lexer.tokenize(opened_file.read())

        # for token in tokens:
        #     print(token)

        tree = parser.parse(tokens)
        # print(tree)

        program = Process(tree)
        program.run()
        # print(program.env)



if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    else:
        if mode == "CF":
            print("Using standard context-free parser")
            exec_file(file_path)
        elif mode == "CS":
            print("Using experimental context sensitive parser")
            print('Not ready yet :)')
        else:
            print('Mode name is incorrect, using the default one (CF)')
            exec_file(file_path)
