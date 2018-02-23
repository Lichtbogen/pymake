""" Makefile generator for C++ """

from makefile import Makefile

class MakefileCC(Makefile):
    """ Class for building a C++ Makefile """
    def __init__(self, src=None):
        super(MakefileCC, self).__init__(src)

    def get_properties(self):
        """ Returns the Makefile properties as an dictionary """
        pdc = super(MakefileCC, self).get_properties()
        if self.stdvers != 0:
            pdc.update({"stdvers":self.stdvers})
        return pdc

    def load(self, src=None):
        """ Reinitialize all class members """
        super(MakefileCC, self).load(src)
        self.compiler = "g++"
        self.stdvers = 10
        self.preset = "Default G++"
        if src != None:
            if 'stdvers' in src.keys():
                self.stdvers = src['stdvers']

    def add_variables(self):
        """ Adds the variable section to the output """
        lines = super(MakefileCC, self).add_variables()
        if self.stdvers > 0 and self.stdvers < 11:
            self.lines.append("CCSTD  = -std=c++0x")
        elif self.stdvers > 0:
            self.lines.append("CCSTD  = -std=c++%d" % self.stdvers)
        return lines

    def get_compiler_statement(self, name):
        """ Returns the compiler statement """
        if self.stdvers > 0:
            line = "$(CC) $(CCSTD) $(CF) -c %s" % name
        else:
            line = "$(CC) $(CF) -c %s" % name
        if self.pkgconfig != "":
            line += " `pkg-config --cflags $(PKGCFG)`"
        if self.objpath != "":
            line += " -o %s" % self.get_obj_name(name)
        return line
