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
        self.libs = []
        self.cflags = "-Wall"
        self.lflags = ""
        self.oflags = "-DNDEBUG -O2"
        self.pflags = ""
        self.dflags = "-DDEBUG"
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
            if 'source' in src.keys():
                self.source = src['source']
            if 'libs' in src.keys():
                self.libs = src['libs']

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
        if self.libs != "":
            pdc.update({"libs":self.libs})
        pdc.update({"source":self.source})
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
        line = "$(CC) $(CF) -c %s" % name
        if self.objpath != "":
            line += " -o %s" % self.get_obj_name(name)
        return line

    def get_linker_statement(self):
        """ Gets the final linker statement """
        if len(self.libs) > 0:
            line = "$(CC) $(LF) $(OBJ) -o $(NAME) $(LIBS)"
        else:
            line = "$(CC) $(LF) $(OBJ) -o $(NAME)"
        return line

    def get_obj_name(self, fname):
        """ Returns the object name of source file """
        fname = os.path.basename(fname)
        if fname.endswith(".c"):
            fname = fname.replace(".c", ".o")
        elif fname.endswith(".cpp"):
            fname = fname.replace(".cpp", ".o")
        if self.objpath != "":
            fname = self.objpath + '/' + fname
        return fname

    def get_libs(self):
        """ Returns the library objects as command line argument for the compiler """
        result = ""
        for lib in self.libs:
            result += "-l%s " % lib
        return result[0:len(result)-1]

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
        self.lines.append(line[0:len(line)-1])
        self.lines.append("")

    def add_debug_target(self):
        """ Adds the debug target to the output """
        self.lines.append("debug: CF = -g $(DFLAGS) $(CFLAGS)")
        self.lines.append("debug: LF = -g")
        self.lines.append("debug: $(NAME)")
        self.lines.append("")

    def add_release_target(self):
        """ Adds the release target to the output """
        self.lines.append("release: CF = $(CFLAGS) $(OFLAGS)")
        self.lines.append("release: LF = -s")
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
        if len(self.libs) > 0:
            self.lines.append("LIBS   = %s" % self.get_libs())
        self.lines.append("")

    def __str__(self):
        return '\n'.join(self.lines)

    def scan(self, root='.', recursive=False):
        """ Scans the given directory for source files """
        if recursive:
            for path, subdirs, files in os.walk(root):
                for name in files:
                    fname = os.path.join(path, name)
                    if fname.endswith(".c") or fname.endswith(".cpp"):
                        self.source.append(fname)
        else:
            for fname in os.listdir(root):
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
        self.add_release_target()
        self.add_debug_target()
        self.add_linker_statement()
        self.add_compiler_statements()
        self.add_clean_target()
        self.add_phony_targets()
