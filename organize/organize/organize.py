import sys
from config import MainDisplay
from the_parser import parser

if __name__ == '__main__':
    args = parser.parse_args()
    config = MainDisplay()

    if args.choice == 'config':
        config.run()

