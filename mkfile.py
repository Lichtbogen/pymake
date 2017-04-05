""" Class for automated creation of Makefiles """

import os

class Makefile(object):
    """ Class for building a Makefile """
    def __init__(self, src=None):
        self.load(src)

    def load(self, src=None):
        """ Reinitialize all class members """
        self.lines = []
        self.source = []
        self.compiler = "g++"
        self.cflags = "-Wall"
        self.lflags = ""
        self.oflags = "-O2"
        self.pflags = ""
        self.dflags = "-DDEBUG -g"
        self.objpath = ""
        self.name = "prog"
        self.preset = "Default GCC"
        if src != None:
            if 'objpath' in src.keys():
                self.objpath = src['objpath']
            if 'compiler' in src.keys():
                self.compiler = src['compiler']
            if 'name' in src.keys():
                self.name = src['name']
            if 'cflags' in src.keys():
                self.cflags = src['cflags']
            if 'lflags' in src.keys():
                self.lflags = src['lflags']
            if 'oflags' in src.keys():
                self.oflags = src['oflags']
            if 'pflags' in src.keys():
                self.pflags = src['pflags']
            if 'dflags' in src.keys():
                self.dflags = src['dflags']

    def get_properties(self):
        """ Returns the Makefile properties as an dictionary """
        pdc = {"name":self.name, "compiler":self.compiler}
        if self.objpath != "":
            pdc.update({"objpath":self.objpath})
        if self.cflags != "":
            pdc.update({"cflags":self.cflags})
        if self.lflags != "":
            pdc.update({"lflags":self.lflags})
        if self.oflags != "":
            pdc.update({"oflags":self.oflags})
        if self.dflags != "":
            pdc.update({"dflags":self.dflags})
        if self.pflags != "":
            pdc.update({"pflags":self.pflags})
        return pdc

    def add_header(self):
        """ Adds the file header """
        self.lines.append("#")
        self.lines.append("# Automatic generated Makefile by pymake")
        self.lines.append("#")
        self.lines.append("# Preset: %s" % self.preset)
        self.lines.append("#")

    def get_compiler_statement(self, name):
        """ Returns the compiler statement """
        line = "$(CC) "
        if self.cflags != "":
            line += "$(CFLAGS) "
        if self.pflags != "":
            line += "$(PFLAGS) "
        line += "-c %s" % name
        if self.objpath != "":
            line += " -o %s" % self.get_obj_name(name)
        return line

    def get_linker_statement(self):
        """ Gets the final linker statement """
        line = "$(CC) $(LFLAGS) "
        if self.cflags != "":
            line += "$(CFLAGS) "
        if self.pflags != "":
            line += "$(PFLAGS) "
        line += "$(OBJ) -o $(NAME)"
        return line

    def get_obj_name(self, fname):
        """ Returns the object name of source file """
        if fname.endswith(".c"):
            fname = fname.replace(".c", ".o")
        elif fname.endswith(".cpp"):
            fname = fname.replace(".cpp", ".o")
        if self.objpath != "":
            fname = self.objpath + '/' + fname
        return fname

    def add_objects(self):
        """ Adds the list of objects to compile """
        self.lines.append("## Object file list")
        line = "OBJ = "
        for src in self.source:
            obj = self.get_obj_name(src)
            line += obj + ' '
            if len(line) > 80:
                line += '\\'
                self.lines.append(line)
                line = '\t'
        self.lines.append(line)
        self.lines.append("")

    def add_all_target(self):
        """ Adds the all target """
        self.lines.append("all: $(NAME)")
        self.lines.append("")

    def add_debug_target(self):
        """ Adds the debug target to the output """
        if self.dflags != "":
            self.lines.append("debug: CFLAGS += $(DFLAGS)")
            self.lines.append("debug: $(NAME)")
            self.lines.append("")

    def add_release_target(self):
        """ Adds the release target to the output """
        if self.dflags != "":
            self.lines.append("release: CFLAGS += $(OFLAGS) -DNDEBUG")
            self.lines.append("release: LFLAGS += -s")
            self.lines.append("release: $(NAME)")
            self.lines.append("")

    def add_clean_target(self):
        """ Adds the clean target """
        self.lines.append("clean:")
        self.lines.append("\trm $(OBJ)")
        self.lines.append("")

    def add_phony_targets(self):
        """ Adds the phony targets to the Makefile """
        self.lines.append(".PHONY: clean")
        self.lines.append("")

    def add_linker_statement(self):
        """ Adds the final linker statement to the output """
        self.lines.append("$(NAME): $(OBJ)")
        self.lines.append("\t%s" % self.get_linker_statement())
        self.lines.append("")

    def add_compiler_statements(self):
        """ Adds compiler statements for all source modules """
        for src in self.source:
            obj = self.get_obj_name(src)
            self.lines.append("%s: %s" % (obj, src))
            self.lines.append("\t%s" % self.get_compiler_statement(src))
            self.lines.append("")

    def add_variables(self):
        """ Adds the variable section to the output """
        self.lines.append("")
        self.lines.append("## General variables")
        self.lines.append("NAME   = %s" % self.name)
        self.lines.append("")
        self.lines.append("## Compiler and flags")
        self.lines.append("CC     = %s" % self.compiler)
        if self.cflags != "":
            self.lines.append("CFLAGS = %s" % self.cflags)
        if self.lflags != "":
            self.lines.append("LFLAGS = %s" % self.lflags)
        if self.dflags != "":
            self.lines.append("DFLAGS = %s" % self.dflags)
        if self.oflags != "":
            self.lines.append("OFLAGS = %s" % self.oflags)
        if self.pflags != "":
            self.lines.append("PFLAGS = %s" % self.pflags)
        self.lines.append("")

    def __str__(self):
        return '\n'.join(self.lines)

    def scan(self, fdir='.'):
        """ Scans the given directory for source files """
        for fname in os.listdir(fdir):
            if fname.endswith(".c") or fname.endswith(".cpp"):
                self.source.append(fname)

    def write(self, fname):
        """ Writes the current content to the output file """
        with open(fname, "wt") as outf:
            outf.write(str(self))

    def build(self):
        """ Builds the whole file structure """
        self.add_header()
        self.add_variables()
        self.add_objects()
        self.add_all_target()
        self.add_debug_target()
        self.add_release_target()
        self.add_linker_statement()
        self.add_compiler_statements()
        self.add_clean_target()
        self.add_phony_targets()
