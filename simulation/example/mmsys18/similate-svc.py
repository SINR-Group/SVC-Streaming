# Copyright (c) 2018, Kevin Spiteri
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import math
import os
import subprocess
import json
import sys
import threading

# TODO: Clean up to give an easier-to-understand example how to use Sabre!

def load_json(path):
    with open(path) as file:
        obj = json.load(file)
    return obj

def cdf(l, margin = 0.025):
    l = sorted(l)
    range = l[-1] - l[0]
    if range > 0:
        margin *= range
    inc = 1 / len(l)
    c = []
    y = 0
    if range == 0:
        c += [[l[0] - margin, y]]
    for x in l:
        c += [[x, y]]
        y += inc
        c += [[x, y]]
    if range == 0:
        c += [[l[-1] + margin, y]]
    return c

def mean_stddev(l):
    mean = sum(l) / len(l)
    var = sum([(x - mean) * (x - mean) for x in l]) / len(l)
    stddev = math.sqrt(var)
    return (mean, stddev)

def thread_run_sabre(results, command):
    completed = subprocess.run(command, stdout = subprocess.PIPE)
    for line in completed.stdout.decode('ascii').split('\n'):
        l = line.split(':')
        if len(l) != 2:
            continue
        if l[0] in results:
            results[l[0]].append(float(l[1]))

def thread_run_gnuplot(plotting):
    subprocess.run('gnuplot', input = plotting.encode('ascii'))

def do_figure(prefix, subfigs, algorithms, metrics, term = None):
    print(prefix + ' ', end = '')

    plotting_threads = []

    for subfig in subfigs:
        title = subfig[0]
        dir = subfig[1]
        args1 = subfig[2]

        print(title + ' ', end = '')

        # info['metric_name']['algorithm_name'] = (mean, stddev, 'name of .dat file')
        info = {m[0]: {} for m in metrics}
        
        plot_mark_offset = 0
        for algorithm in algorithms:
            plot_mark_offset += 1
            name = algorithm[0]
            args = args1 + algorithm[1]
        
            print(name + ' ', end = '')
        
            results = {m[1]: [] for m in metrics}
        
            cnt = 0
            max_threads = 5
            threads = []
            for trace in os.listdir(dir)[:]: # use this line to limit directory size
                cnt += 1
                print('%d' % cnt, end = '')
                sys.stdout.flush()
        
                if len(threads) >= max_threads:
                    for t in threads:
                        if not t.is_alive():
                            t.join()
                            threads.remove(t)
                            break
        
                if len(threads) >= max_threads:
                    threads[0].join()
                    threads.pop(0)
        
                command = ['python3', './sabre-mmsys18.py', '-n', dir + '/' + trace] + args
                t = threading.Thread(target = thread_run_sabre, args = (results, command))
                threads.append(t)
                t.start()
        
                print('\b' * len(str(cnt)), end = '')
                print(' '  * len(str(cnt)), end = '')
                print('\b' * len(str(cnt)), end = '')
            for t in threads:
                t.join()
        
            print('\b' * (len(name) + 1), end = '')
            print(' '  * (len(name) + 1), end = '')
            print('\b' * (len(name) + 1), end = '')
        
            for metric in metrics:
                config = metric[2] if len(metric) > 2 else {}
                samples = results[metric[1]]
                points = cdf(samples)
                median = (points[(len(points) - 1) // 2][0] + points[len(points) // 2][0]) / 2
                stats = (median, ) + mean_stddev(samples)
                datname = ('tmp/' + prefix + '-' +
                           title.replace(' ', '-') + '-' +
                           metric[0].replace(' ', '-') + '-' +
                           algorithm[0].replace(' ', '-') + '.dat')
                info[metric[0]][algorithm[0]] = stats + (datname, )
                with open(datname, 'w') as f:
                    for l in points:
                        xoffset = config['xoffset'] if 'xoffset' in config else 0
                        f.write('%f %f\n' % (xoffset + l[0], l[1]))
        
                dot_count = 4
                step = math.floor(len(points) / dot_count)
                # plot_mark_offset in [1, len(algorithms)]
                first = math.ceil(plot_mark_offset / (len(algorithms) + 1) * step)
                with open(datname + '.dot', 'w') as f:
                    for l in points[first::step]:
                        xoffset = config['xoffset'] if 'xoffset' in config else 0
                        f.write('%f %f\n\n' % (xoffset + l[0], l[1]))
        
        statname = ('stats/' + prefix + '-' + title.replace(' ', '-') + '.txt')
        delim = ''
        with open(statname, 'w') as f:
            for metric in metrics:
                f.write(delim)
                delim = '\n'
                f.write('%s:\n' % metric[0])
                for algorithm in algorithms:
                    i = info[metric[0]][algorithm[0]]
                    f.write('%s: %f %f %f\n' % (algorithm[0], i[0], i[1], i[2]))

        xranges = subfig[3][:] if len(subfig) > 3 else None
        mi = -1
        for metric in metrics:
            mi += 1
            config = metric[2] if len(metric) > 2 else {}
            pdfname = ('figures/' + prefix + '-' +
                       title.replace(' ', '-') + '-' +
                       metric[0].replace(' ', '-') +
                       '.pdf')
            key = config['key'] if 'key' in config else 'bottom right'
            xtics = str(config['xtics']) if 'xtics' in config else 'autofreq'
            #xlabel = title + ' ' + metric[0]
            xlabel = metric[0]
            if 'time' in xlabel:
                xlabel += ' (s)'
            elif 'bitrate' in xlabel:
                xlabel += ' (kbps)'
            if xranges:
                xrange = '[0:%f]' % xranges.pop(0)
            else:
                xrange = '[0:*]'
            plot_list = []
            point_types = [1, 2, 4, 6, 8, 10]
            pti = 0
            for algorithm in algorithms:
                pt = point_types[pti]
                pti += 1
                alg_pars = algorithm[2]
                if alg_pars.startswith('notitle'):
                    alg_pars = alg_pars[len('notitle'):]
                    # HACK
                    if isinstance(term, list) and term[mi] != None:
                        do_title = ' notitle '
                    else:
                        do_title = ' title "' + algorithm[0] + '" '
                else:
                    do_title = ' title "' + algorithm[0] + '" '
                datname = info[metric[0]][algorithm[0]][-1]
                plot_list += ['"' + datname + '" notitle ' + alg_pars + ' lw 2']
                plot_list += ['"' + datname + '.dot" ' + do_title +
                              ' with linespoints pt ' + str(pt) + ' ' + alg_pars + ' lw 2']

            trm = term[mi] if isinstance(term, list) else term
            if trm == None:
                trm = 'pdf size 2.3, 1.75 font ",16"'

            plotting = '''set term ''' + trm + '''
set bmargin 3.5

set style data lines
set key ''' + key + '''

set xlabel "''' + xlabel + '''"
set xtics ''' + xtics + '''

set xrange ''' + xrange + '''

set output "''' + pdfname + '''"

plot ''' + ', '.join(plot_list) + '''

set output
'''
            #subprocess.run('gnuplot', input = plotting.encode('ascii'))
            t = threading.Thread(target = thread_run_gnuplot, args = (plotting, ))
            plotting_threads.append(t)
            t.start()

        print('\b' * (len(title) + 1), end = '')
        print(' '  * (len(title) + 1), end = '')
        print('\b' * (len(title) + 1), end = '')

    for t in plotting_threads:
        t.join()

    print('\b' * (len(prefix) + 1), end = '')
    print(' '  * (len(prefix) + 1), end = '')
    print('\b' * (len(prefix) + 1), end = '')


def figure_12_13():
    prefix = '12_13'

    subfigs = [
        ('FCC HD', 'hd_fs', ['-m', 'bbb4k.json', '-b', '25'], [0.01, 1200, 12000, 120]),
    ]

    algorithms = [
        ('BOLA-E'    , ['-ao', '-r', 'none', '-a', 'bolae'  , '-rmp', '4', '-ml', '180'], 'notitle lc 7'),
        ('BOLA-E-FS' , ['-ao', '-r', 'left', '-a', 'bolae'  , '-rmp', '4', '-ml', '180'], 'notitle lc 1'),
    ]

    metrics = [
        ('rebuffer ratio'     , 'rebuffer ratio'),
        ('average bitrate oscillation'  , 'time average bitrate change', {'xtics': 400}),
        ('average bitrate'      , 'time average played bitrate',
         {'key': 'top left reverse Left font ",12"', 'xtics': 4000}),
        ('reaction time', 'rampup time', {'xoffset': -60, 'key': 'out top center vertical', 'xtics': 40}),
    ]

    term = 'pdf size 1.5, 1.75 font ",16"\nset ytics format ""'
    do_figure(prefix, subfigs, algorithms, metrics, term = [None, None, None, term])
    
if __name__ == '__main__':

    bbb = load_json('bbb.json')
    bbb4k = load_json('bbb4k.json')

    os.makedirs('tmp', exist_ok = True)
    os.makedirs('figures', exist_ok = True)
    os.makedirs('stats', exist_ok = True)

    figure_12_13()
