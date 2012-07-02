#!/usr/bin/env python
# encoding: utf-8

"""
pyedf.py

Created by Ray Slakinski on 2010-09-14.
Copyright (c) 2010 Ray Slakinski. All rights reserved.

Modified by Ryan M. Hope on 2012-07-01.
Copyright (c) 2012 Ryan M. Hope. All rights reserved.

EDF/EDF+ Spec:
    http://www.edfplus.info/specs/index.html
"""

import sys
import argparse
import struct
from pprint import pprint

def parse_edf_file( fileobj ):

    header_raw = map( str.strip, struct.unpack_from( '8s80s80s8s8s8s44s8s8s4s', fileobj.read( 256 ) ) )

    header = {}
    header['version'] = int( header_raw[0] )
    header['patient_id'] = header_raw[1]
    header['rec_id'] = header_raw[2]
    header['startdate'] = header_raw[3]
    header['starttime'] = header_raw[4]
    header['header_bytes'] = int( header_raw[5] )
    header['reserved'] = header_raw[6]
    header['num_records'] = int( header_raw[7] )
    header['data_duration'] = float( header_raw[8] )
    header['num_signals'] = int( header_raw[9] )

    signals = {}
    signals['labels'] = map( str.strip, struct.unpack_from( '16s' * header['num_signals'], fileobj.read( 16 * header['num_signals'] ) ) )
    signals['type'] = map( str.strip, struct.unpack_from( '80s' * header['num_signals'], fileobj.read( 80 * header['num_signals'] ) ) )
    signals['physical_dim'] = map( str.strip, struct.unpack_from( '8s' * header['num_signals'], fileobj.read( 8 * header['num_signals'] ) ) )
    signals['physical_min'] = map( int, struct.unpack_from( '8s' * header['num_signals'], fileobj.read( 8 * header['num_signals'] ) ) )
    signals['physical_max'] = map( int, struct.unpack_from( '8s' * header['num_signals'], fileobj.read( 8 * header['num_signals'] ) ) )
    signals['digital_min'] = map( int, struct.unpack_from( '8s' * header['num_signals'], fileobj.read( 8 * header['num_signals'] ) ) )
    signals['digital_max'] = map( int, struct.unpack_from( '8s' * header['num_signals'], fileobj.read( 8 * header['num_signals'] ) ) )
    signals['pre_filtering'] = map( str.strip, struct.unpack_from( '80s' * header['num_signals'], fileobj.read( 80 * header['num_signals'] ) ) )
    signals['num_samples'] = map( int, struct.unpack_from( '8s' * header['num_signals'], fileobj.read( 8 * header['num_signals'] ) ) )
    signals['reserved'] = map( str.strip, struct.unpack_from( '32s' * header['num_signals'], fileobj.read( 32 * header['num_signals'] ) ) )

    data = {}
    for signal in signals['labels']:
        data[signal] = []
    for r in range( 0, header['num_records'] ):
        for s, signal in enumerate( signals['labels'] ):
            data[signal].append( map( int, struct.unpack_from( '%sh' % signals['num_samples'][s], fileobj.read( 2 * signals['num_samples'][s] ) ) ) )

    return {'header': header, 'signals': signals, 'data': data}

def main():
    """This is really only usefull for testing purposes."""
    parser = argparse.ArgumentParser( description = 'Process a given EDF File.' )
    parser.add_argument(
        '-f',
        '--file',
        type = argparse.FileType( 'r' ),
        required = True,
        help = 'EDF File to be processed.',
    )
    args = parser.parse_args()
    data = parse_edf_file( args.file )
    pprint( data['header'] )
    args.file.close()

if __name__ == '__main__':
    main()
