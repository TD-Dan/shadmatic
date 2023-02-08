
def clean_argument(str:str) -> str:
    """Remove preceding '-' marks from arguments"""
    while len(str)>0 and str[0] =='-':
        str = str[1:]
    return str

def convert_lststr_to_argskwargs(argv) -> list[tuple,dict]:
    args = []
    kwargs = {}
    for arg in argv:
        index = arg.find('=')
        if index < 0:
            args.append(arg)
        else:
            kwargs[arg[:index]]=arg[index+1:]
    return [args,kwargs]