from lexer import LangLexer
from parser import LangParser
from interpreter import Process
from comb_parser import WhileCheckCorr
import sys

import datetime
import time
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean, mode, stdev

import argparse

ap = argparse.ArgumentParser()

# ap.add_argument("-m", "--mode", required=True,
#                 help="Mode of parsing the grammar")

ap.add_argument("-f", "--file", required=True,
                help="Path to file with code of program")

ap.add_argument('-t', '--times', type=int, required = True,
                help="Times of execution")

ap.add_argument('-i', '--iters', type=int, required = True,
                help="Iterations per one execution")


args = vars(ap.parse_args())

# mode = args['mode']
file_path = args['file']
times = args['times']
iters = args['iters']

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

    try:
        tokens = lexer.tokenize(text_file2line(file_path))
    except:
        print('LEXER ERROR')


    tree = parser.parse(tokens)


    program = Process(tree)
    program.run()

# merge all code in 1 string to parser with monadic parser

def text_file2line(path):
    with open(path, 'r') as f:
        return " ".join([line[:-1] for line in f.readlines()])


def get_stat(file_path, times, cs_times, cf_times, iters):
    cs_mean = mean(cs_times)
    cs_stdev = stdev(cs_times)
    cs_range = max(cs_times) - min(cs_times)
    cs_data = '\n'.join((
    r'cs_stdev: {}'.format(cs_stdev),
    r'cs_mean: {}'.format(cs_mean),
    r'cs_range: {}'.format(cs_range)))

    cf_mean = mean(cf_times)
    cf_stdev = stdev(cf_times)
    cf_range = max(cf_times) - min(cf_times)
    cf_data = '\n'.join((
    r'cf_stdev: {}'.format(cf_stdev),
    r'cf_mean: {}'.format(cf_mean),
    r'cf_range: {}'.format(cf_range)))


    number_of_times = [i+1 for i in range(times)]
    plt.rcParams['figure.figsize'] = (15,15)
    plt.plot(number_of_times, cf_times, 'r', label = 'CF')
    plt.plot(number_of_times, cs_times, 'b', label = 'CS')
    plt.xlabel('Number of executions')
    plt.ylabel('Time of execution, microseconds')
    plt.suptitle('Time test of {}; {} iterations per execution'.format(file_path, str(iters)))
    plt.text(1,1, cs_data, fontsize=10)
    print('cs_stdev: {}'.format(cs_stdev))
    print('cs_mean: {}'.format(cs_mean))
    plt.text(1,1, cf_data, fontsize=10)
    print('cf_stdev: {}'.format(cf_stdev))
    print('cf_mean: {}'.format(cf_mean))
    plt.grid()
    plt.legend()
    save_moment = int(time.time())

    save_file = 'time_test_result_{}_t_{}_i_{}_{}'.format(times,iters,file_path.split('/')[-1], save_moment)
    plt.savefig(save_file + '.png')

    data = {"CS" : cs_times, "CF" : cf_times}
    df = pd.DataFrame(data)
    df.to_csv(save_file + '.csv')


# monadic parser checker

def get_errors(path):

    checker = WhileCheckCorr()
    prog_in_lines = text_file2line(path)
    result_of_test = checker.parse_obj(prog_in_lines)

    if result_of_test == True:
        print('Code is correct')
        exec_file(path)

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

        

# running 100 times to see the time difference    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    else:
        fqqq = 0
        cs_times = []
        cf_times = []

        for i in range(times):
            t_1 = datetime.datetime.now()
            for j in range(iters):
                try:
                    exec_file(file_path)
                except:
                    print('Error')
                fqqq += 1
            t_2 = datetime.datetime.now()
            print((t_2 - t_1).microseconds + (t_2 - t_1).seconds * 1000000)
            print('--------------------------------')
            t_3 = datetime.datetime.now()
            for j in range(iters):
                try:
                    get_errors(file_path)
                except:
                    print('Error')
                fqqq += 1
            t_4 = datetime.datetime.now()
            print((t_4 - t_3).microseconds + (t_4 - t_3).seconds * 1000000)
            

            cf_times.append((t_2 - t_1).microseconds + (t_2 - t_1).seconds * 1000000)
            cs_times.append((t_4 - t_3).microseconds + (t_4 - t_3).seconds * 1000000)

        print(fqqq)
        get_stat(file_path, times, cs_times, cf_times, iters)
