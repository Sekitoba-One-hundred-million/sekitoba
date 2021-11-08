from argparse import ArgumentParser

from data_analyze import data_create
#from machine_learn import learn
from machine_learn_torch import learn

def main():
    parser = ArgumentParser()
    parser.add_argument( "-g", type=bool, default = False, help = "optional" )
    parser.add_argument( "-u", type=bool, default = False, help = "optional" )

    g_check = parser.parse_args().g
    u_check = parser.parse_args().u
    data = data_create.main( update = u_check )
    #model = learn.main( data )
    model = learn.main( data )

if __name__ == "__main__":
    main()