from app.NeuralGas import NeuralGas
from DataFetch.DataFetch import load
from random import *
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('filename', help='name of the source file.\n /!\ the .png file should be in the static folder')

options=argparser.parse_args()
filename = options.filename

print("Growing Neural Gas")

datas = load(filename)
parameters = {"eps_b" : 5E-2 ,  # Winning node adaptation factor
              "eps_n" : 6E-4 ,  # Winning node, neighbor adaptation factor
              "age_max" : 70,   # Oldest age allowed for an edge
              "lambda" : 300,   # Cycle interval between node insertions
              "alpha" : 5E-2,   # Error reduction factor upon insertion
              "beta" : 5E-4     # Error reduction factor for each cycle
              }

g = NeuralGas(datas,parameters)
g.run(animated = True)
