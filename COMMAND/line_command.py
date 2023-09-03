from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('action',choices=['new','list'], help='type of action')
parser.add_argument('--type',help='specify type')
parser.add_argument('--participants',help='specify participants')
parser.add_argument('--price_min',help='specify price_min')
parser.add_argument('--price_max',help='specify price_max')
parser.add_argument('--accessibility_min',help='specify accessibility_min')
parser.add_argument('--accessibility_max',help='specify accessibility_max')

line_args = parser.parse_args()

