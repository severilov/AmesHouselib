import argparse

from houselib import train_model, fix_seeds


fix_seeds()

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', type=str, default='linreg', help='ml model to use in training')
args = parser.parse_args()

if __name__ == '__main__':
    train_model(modeltype=args.model)
