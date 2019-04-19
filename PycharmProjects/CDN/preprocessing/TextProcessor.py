import sys
import utils.utils as utilz
from preprocessing.Tokenizer import *


def main():
    # if len(sys.argv) != 2:
    #     raise ValueError("Invalid path input, usage: <path_to_parse>")
    # path = sys.argv[1]
    path = "C:\\Users\\avivko\PycharmProjects\CDN\\tests\\files\\bible.txt"
    print("Starting to pre process file name {}".format(path))
    raw = utilz.read_file_to_text(path)

    # tokenizer = Tokenizer()
    # tokenized_raw = tokenizer.tokenize(raw)

    # print(tokenized_raw[:10])

if __name__ == '__main__':
    main()
