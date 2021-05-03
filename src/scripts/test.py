import argparse

from houselib import test_model, fix_seeds


parser = argparse.ArgumentParser()
parser.add_argument('-m', '--modelpath', type=str, default='./src/models/model.pkl', help='path to ml model for testing')
args = parser.parse_args()

if __name__ == '__main__':
    test_model(modelpath=args.modelpath)
