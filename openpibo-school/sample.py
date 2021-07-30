import os, sys, time
from utils.config import Config as cfg

sys.path.append(cfg.OPENPIBO_PATH + '/edu')
from pibo import Edu_Pibo

def sample_func():
    pibo = Edu_Pibo()
    print(dir(pibo))

if __name__ == "__main__":
    sample_func()
