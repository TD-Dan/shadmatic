
import shadowui


class CommandlineWindow(shadowui.WindowBase):

    def run(self):
        super().run()
        
        while True:    
            try:
                user_input = input()
                match user_input:
                    case 'x'|'exit':
                        exit()
            except KeyboardInterrupt:
                print("Catch!")
                raise
        
    
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)