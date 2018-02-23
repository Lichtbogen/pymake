from makefile import Makefile
from makefilecc import MakefileCC

def get_gcc_profile(cfg):
    make = Makefile(cfg)
    return make

def get_gpp_profile(cfg):
    make = MakefileCC(cfg)
    return make

table = {
  "gcc": get_gcc_profile,
  "g++": get_gpp_profile
}
