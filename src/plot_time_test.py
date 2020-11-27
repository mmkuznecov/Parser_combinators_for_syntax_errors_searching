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
import scipy.stats as st

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


def get_stat(file_path, times, comb_times, gen_times, iters):

    # main statistic info

    comb_mean = mean(comb_times)
    comb_stdev = stdev(comb_times)
    comb_range = max(comb_times) - min(comb_times)

    # 95% confidence interval for comb_times

    comb_interval_lower, comb_interval_upper = st.t.interval(0.95, len(comb_times)-1, loc=mean(comb_times), scale=st.sem(comb_times))
    comb_interval_range = comb_interval_upper - comb_interval_lower

    # comb data info for plot

    comb_data = '\n'.join((
    r'comb_stdev: {}'.format(comb_stdev),
    r'comb_mean: {}'.format(comb_mean),
    r'comb_range: {}'.format(comb_range),
    r'comb_interval_lower: {}'.format(comb_interval_lower),
    r'comb_interval_upper: {}'.format(comb_interval_upper),
    r'comb_interval_range: {}'.format(comb_interval_range)))

    print(comb_data)

    gen_mean = mean(gen_times)
    gen_stdev = stdev(gen_times)
    gen_range = max(gen_times) - min(gen_times)

    # 95% confidence interval for gen_times

    gen_interval_lower, gen_interval_upper = st.t.interval(0.95, len(gen_times)-1, loc=mean(gen_times), scale=st.sem(gen_times))
    gen_interval_range = gen_interval_upper - gen_interval_lower

    # gen data info for plot

    gen_data = '\n'.join((
    r'gen_stdev: {}'.format(gen_stdev),
    r'gen_mean: {}'.format(gen_mean),
    r'gen_range: {}'.format(gen_range),
    r'gen_interval_lower: {}'.format(gen_interval_lower),
    r'gen_interval_upper: {}'.format(gen_interval_upper),
    r'gen_interval_range: {}'.format(gen_interval_range)))

    print(gen_data)


    number_of_times = [i+1 for i in range(times)]
    plt.rcParams['figure.figsize'] = (15,15)
    plt.plot(number_of_times, gen_times, 'r', label = 'gen')
    plt.plot(number_of_times, comb_times, 'b', label = 'comb')
    plt.xlabel('Number of executions')
    plt.ylabel('Time of execution, microseconds')
    plt.suptitle('Time test of {}; {} iterations per execution'.format(file_path, str(iters)))
    plt.text(1,1, comb_data, fontsize=10)
    print('comb_stdev: {}'.format(comb_stdev))
    print('comb_mean: {}'.format(comb_mean))
    plt.text(1,1.5, gen_data, fontsize=10)
    print('gen_stdev: {}'.format(gen_stdev))
    print('gen_mean: {}'.format(gen_mean))
    plt.grid()
    plt.legend()
    save_moment = int(time.time())

    # save plot and .combv info

    save_file = 'time_test_result_{}_t_{}_i_{}_{}'.format(times,iters,file_path.split('/')[-1], save_moment)
    plt.savefig(save_file + '.png')

    data = {"comb" : comb_times, "gen" : gen_times}
    df = pd.DataFrame(data)
    df.to_combv(save_file + '.combv')


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
        print('Code is incorrect')

         

if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    else:
        fqqq = 0
        comb_times = []
        gen_times = []

        for i in range(times):
            t_1 = datetime.datetime.now()
            for j in range(iters):
                try:
                    exec_file(file_path)
                except:
                    print('Error')
                fqqq += 1
            t_2 = datetime.datetime.now()
            t_3 = datetime.datetime.now()
            for j in range(iters):
                try:
                    get_errors(file_path)
                except:
                    print('Error')
                fqqq += 1
            t_4 = datetime.datetime.now()
            
            # get time for each type of execution

            gen_times.append((t_2 - t_1).microseconds + (t_2 - t_1).seconds * 1000000)
            comb_times.append((t_4 - t_3).microseconds + (t_4 - t_3).seconds * 1000000)

        get_stat(file_path, times, comb_times, gen_times, iters)
