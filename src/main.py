from lexer import LangLexer
from parser import LangParser
from interpreter import Process
from extend_comb_parser import WhileCheckCorr
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
    #with open(file_path) as opened_file:
    try:
        tokens = lexer.tokenize(text_file2line(file_path))
    except:
        print('LEXER ERROR')

    # for token in tokens:
    #     print(token)

    tree = parser.parse(tokens)

    print(type(tree))
    #print(tree[0])

    program = Process(tree)
    program.run()
    # print(program.env)


def text_file2line(path):
    with open(path, 'r') as f:
        return " ".join([line[:-1] for line in f.readlines()])

def get_errors(path):

    checker = WhileCheckCorr()
    prog_in_lines = text_file2line(path)
    result_of_test = checker.parse_obj(prog_in_lines)

    if result_of_test == True:
        print('Code is correct')

    else:
        print(result_of_test)
        with open (path, 'r') as f:
            list_of_lens = [len(line[:-1]) for line in f.readlines()]
        result_of_test = str(result_of_test)
        number = int(result_of_test.split(':')[-1])

        itera = 1
        while number > 0:
            number -= list_of_lens[itera-1] + 1
            itera += 1
        
        err_num = list_of_lens[itera-1] + number
        
        print('Code is incorrect')
        print('Expected brace at {}:{}'.format(itera, err_num))

        

    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    else:
        if mode == "CF":
            print("Using standard context-free parser")
            exec_file(file_path)
        elif mode == "CS":
            print("Using experimental context sensitive parser")
            '''checker = WhileCheckCorr()
            prog_in_lines = text_file2line(file_path)
            result_of_test = checker.parse_obj(prog_in_lines)
            if result_of_test == True:
                print("Code is correct")
                # exec_file(file_path)
            else:
                print("Some problems occurred")
                print(result_of_test)'''
            get_errors(file_path)
        else:
            print('Mode name is incorrect, using the default one (CF)')
            exec_file(file_path)
