import argparse

from houselib import train_model, fix_seeds


fix_seeds()

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--model_type', type=str, default='linreg', help='ml model to use in training')
parser.add_argument('-m', '--models_path', type=str, default='./src/models', help='path to save models')
parser.add_argument('-l', '--logs', type=str, default=True, help='print or not results of training model')
args = parser.parse_args()

if __name__ == '__main__':
    train_model(modeltype=args.model_type, show_res=args.logs, models_path=args.models_path)
