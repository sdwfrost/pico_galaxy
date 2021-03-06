#!/usr/bin/env python

"""Wrapper for the interproscan tool.

James E Johnson - University of Minnesota
"""
import logging
import subprocess
import sys

log = logging.getLogger(__name__)

assert sys.version_info[:2] >= (2, 4)


def __main__():
    # Parse Command Line

    # TODO, unused argument?
    # working_dir = sys.argv[1]

    input_file = sys.argv[2]
    format = sys.argv[3]
    output = sys.argv[4]
    # Convert all spaces in ORF header to underscores
    cmdline = 'sed  \'s/ /_/\' %s > temp.fa' % (input_file)
    # print >> sys.stderr, cmdline
    try:
        proc = subprocess.Popen(args=cmdline, shell=True,
                                universal_newlines=True,
                                stderr=subprocess.PIPE)
        returncode = proc.wait()
        # get stderr, allowing for case where it's very large
        stderr = ''
        buffsize = 1048576
        try:
            while True:
                stderr += proc.stderr.read(buffsize)
                if not stderr or len(stderr) % buffsize != 0:
                    break
        except OverflowError:
            pass
        if returncode != 0:
            raise Exception(stderr)
    except Exception as e:
        sys.exit('Error running sed ' + str(e))

    cmdline = ('iprscan -cli -nocrc -i temp.fa -o temp.iprscan -goterms'
               ' -seqtype p -altjobs -format %s -appl hmmpfam > /dev/null'
               % (format))
    # print >> sys.stderr, cmdline # so will appear as blurb for file
    try:
        proc = subprocess.Popen(args=cmdline, shell=True,
                                universal_newlines=True,
                                stderr=subprocess.PIPE)
        returncode = proc.wait()
        # get stderr, allowing for case where it's very large
        stderr = ''
        buffsize = 1048576
        try:
            while True:
                stderr += proc.stderr.read(buffsize)
                if not stderr or len(stderr) % buffsize != 0:
                    break
        except OverflowError:
            pass
        if returncode != 0:
            raise Exception(stderr)
    except Exception as e:
        sys.exit('Error running iprscan ' + str(e))

    out = open(output, 'w')
    # outpe_path = os.path.join(working_dir,'')
    for line in open('temp.iprscan'):
        out.write("%s" % (line))
    out.close()


if __name__ == "__main__":
    __main__()
