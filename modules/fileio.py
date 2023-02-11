
import state
from modules.log import Log

def write_list_to_file(data:list,filename:str,confirm_overwrite=True, fail_silently=False):
    """Writes a list to file as one list entry per line.
    Asks user if file already exists if confirm_overwrite is true.
    Raises state.ProgramCancel if writing fails, unless fail_silently is True, incase just returns without overwriting."""

    log = Log("fileio-w")
    log.info("Outputting "+str(len(data))+" entries to "+filename)

    outfile = None
    try:
        try:
            outfile = open(filename,'x', encoding="utf-8")
        except FileExistsError:
                while confirm_overwrite:
                    print("File '"+filename+"' Already exists, [a]bort, [r]ename or [o]verwrite?")
                    user_in = input()
                    match user_in:
                        case 'a'|'abort':
                            if fail_silently:
                                return
                            else:
                                raise state.ProgramCancel
                        case 'r'|'rename':
                            print("Give a new name for file to be written:")
                            filename = input()
                            break
                        case 'o'|'overwrite':
                            break
                        case _:
                            print("Not valid answer. (Ctrl-C to panic)")
        if not outfile:
            outfile = open(filename,'w', encoding="utf-8")
        for item in data:
            outfile.write(str(item)+'\n')
    finally:
        if outfile:
            outfile.close()
        log.close()

        
def read_list_from_file(filename:str, fail_silently=False) -> list:
    """Reads a list from that has one entry per line.
    Raises state.ProgramCancel if read fails, unless fail_silently is True, incase just returns with empty list"""

    log = Log("fileio-r")
    log.info("Reading entries from '"+filename+"'")

    infile = None
    outlist = []
    try:
        try:
            infile = open(filename,'r', encoding="utf-8")
            for item in infile:
                outlist.append(item.strip())
            return outlist
        except FileNotFoundError:
            if fail_silently:
                return []
            else:
                raise state.ProgramCancel
    finally:
        if infile:
            infile.close()
        log.info(str(len(outlist))+" items found from '"+filename+"'")
        log.close()