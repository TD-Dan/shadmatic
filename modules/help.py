

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
            #If user arguments present try to find help for it
            for module in state.modules:
                match args[2]:
                    case module.name | module.short:
                        if len(args)<4:
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
                                if module.commands:
                                    print("Implements following commands into the program:")
                                    for comd in module.commands:
                                        print(comd.name)
                                        print("\t"+comd.__doc__)
                            else:
                                print("No help available for module "+module.name)
                        else:
                            if module.commands:
                                for comd in module.commands:
                                    if comd.name == args[3]:
                                        print("'"+module.name+"' command '"+comd.name+"':")
                                        print(comd.__doc__)
                                        if comd.required_kwargs:
                                            print("\t required arguments: ")
                                            for key,value in comd.required_kwargs.items():
                                                print("\t"+key+"\t"+value)
                                        print("\t optional arguments: ")
                                        if comd.optional_kwargs:
                                            for key,value in comd.optional_kwargs.items():
                                                print("\t"+key+"\t"+value)
                                        raise state.ProgramExit()
                                print("no such command in module")
                                print("following commands are in the module:")
                                for comd in module.commands:
                                    print(comd.name)
                            else:
                                print("Module has no commands implemented.")
                            
                        raise state.ProgramExit()
                
            print("No help found for '"+args[2]+"'")
            raise state.ProgramExit()
        elif len(args)>1:
            # If no arguments display program help
            print("\n"+str(state.program_name.center(79)+"\n"+(" - "+state.program_slogan).center(79)))
            print(state.program_version_str.center(79))

            # Display available launch modes
            print("\n"+"    Available program launch modules:".ljust(75)+"|")
            print("".ljust(75)+"|")
            no_launch_modules = []
            for module in state.modules:
                if type(module).run_from_commandline != ModuleBase.run_from_commandline:
                    shorthelp = module.name.capitalize()
                    if module.__doc__:
                        shorthelp = module.__doc__.splitlines()[0]
                    print("    "+module.short.ljust(8)+module.name.ljust(17)+shorthelp[:45].ljust(46)+"|")
                else:
                    #stash for printing it later
                    no_launch_modules.append(module)

            #List available modules
            print("\n"+"    Available program modules:".ljust(75)+"|")
            for module in no_launch_modules:
                shorthelp = module.name.capitalize()
                if module.__doc__:
                    shorthelp = module.__doc__.splitlines()[0]
                print("    "+module.short.ljust(8)+module.name.ljust(17)+shorthelp[:45].ljust(46)+"|")
            print("\n"+("use -h <module> for more help").center(79)+"\n")
            print("\n"+("Visit "+state.program_website+" for more info").center(79)+"\n")
        else:
            print(state.program_help_doc)
        
        raise state.ProgramExit()


#register to main program as a module
state.modules.append(HelpModule())