from mkfile import Makefile

def get_gcc_profile(cfg):
    make = Makefile(cfg)
    make.compiler = "gcc"
    return make

def get_gpp_profile(cfg):
    make = Makefile(cfg)
    make.compiler = "g++"
    return make

table = {
  "gcc": get_gcc_profile,
  "g++": get_gpp_profile
}
