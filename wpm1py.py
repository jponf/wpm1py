#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

__program__='WPM1PY'
__author__ = 'Josep Pon Farreny <jpf2@alumnes.udl.cat>'
__version__ = '0.1a'
__licence__ = 'GPL'

def main():
    parser = argparse.ArgumentParser(
                            description='Educational implementation of WPM1')



    options = parser.parse_args()




# Program entry point, calls immediatly the main routine
if __name__ == '__main__':
    main()
