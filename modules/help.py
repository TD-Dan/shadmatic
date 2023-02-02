

from modules import ModuleBase
import state

from shadowui import Section


help_page = [
    Section('Help')
]

class HelpModule(ModuleBase):
    """Program help
    Shows help in commandline and inside user interface on:
    \t- using the program
    \t- modules
    \t- available tools inside modules
    """

    help_usage = \
    """help [<topic>]
    where:
    \ttopic\tModule name or command"""
    name = "help"
    short = "h"
    def load(self):
        super().load()
        content = state.root['content']
        content += help_page

    def unload(self):
        super().unload()
        pass

    def run_from_commandline(self, *args, **kwargs):
        if len(args)>2:
            #print("display help for "+args[2])
            for module in state.modules:
                match args[2]:
                    case module.name | module.short:
                        if module.__doc__:
                            print("\nModule: \t"+module.name.capitalize())
                            print("Short name: \t"+module.short+"\n")
                            if hasattr(module, '__doc__'):
                                print(module.__doc__)
                                
                            if type(module).run_from_commandline != ModuleBase.run_from_commandline: # test if subclass has implemnented run method
                                print("Can be invoked from commandline", end='')
                                if hasattr(module, 'help_usage'):
                                    print(":\nUsage: \t"+module.help_usage+"\n")
                                    print("\t ( [...] = optional parameter, \t< ... > = replace with value )")
                                else:
                                    print("\n")
                            if type(module).exec != ModuleBase.exec and module.commands:
                                print("Implements following commands into the program:")
                                # list module exec commands
                        else:
                            print("No help available for module "+module.name)
                        raise state.ProgramExit()
                
            print("No help found for '"+args[2]+"'")
            raise state.ProgramExit()
        elif len(args)>1:
            print("\n"+str(state.program_name.center(79)+"\n"+(" - "+state.program_slogan).center(79)))
            print(state.program_version_str.center(79))
            print("\n"+"    Available program launch modes:".ljust(75)+"|")
            print("".ljust(75)+"|")
            for module in state.modules:
                if type(module).run_from_commandline != ModuleBase.run_from_commandline:
                    shorthelp = module.name.capitalize()
                    if module.__doc__:
                        shorthelp = module.__doc__.splitlines()[0]
                    print("    "+module.short.ljust(8)+module.name.ljust(17)+shorthelp[:45].ljust(46)+"|")
            print("\n"+("Visit "+state.program_website+" for more info").center(79)+"\n")
        else:
            print(state.program_help_doc)
        
        raise state.ProgramExit()


#register to main program as a module
state.modules.append(HelpModule())