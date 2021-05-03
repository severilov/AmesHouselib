import argparse

from houselib import test_model, fix_seeds


parser = argparse.ArgumentParser()
parser.add_argument('-m', '--modelpath', type=str, default='./src/models/model.pkl', help='path to ml model for testing')
parser.add_argument('-l', '--logs', type=str, default=True, help='print or not results of testing model')
args = parser.parse_args()

if __name__ == '__main__':
    test_model(modelpath=args.modelpath, show_res=args.logs)
