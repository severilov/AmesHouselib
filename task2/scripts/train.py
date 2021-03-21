import argparse
import sys

sys.path.append('..')

from houselib import read_ames_data
from houselib.utils import fix_seeds

fix_seeds()

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', type=str, default='linreg', help='ml model to use in training')


print('AHAHAHAHH')
