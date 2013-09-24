from pyfortune.entry import main
import logging

if __name__ == '__main__':
    format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(format=format)
    logging.getLogger().setLevel(logging.DEBUG)
    main()
