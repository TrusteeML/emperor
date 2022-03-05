import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="viper/data/model-atari-pong-1/saved", help="VIPER model checkpoint folder")
    parser.add_argument("--output_dir", type=str, default="results", help="Output folder for results")
    args = parser.parse_args()
    MODEL_PATH = args.model
    OUTPUT_DIR = args.output_dir













if __name__ == '__main__':
    main()