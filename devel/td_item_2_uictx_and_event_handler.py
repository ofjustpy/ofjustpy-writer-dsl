
from html_writer.macro_module import macros, Div, Button
from py_tailwind_utils import *
import ofjustpy as oj


with oj.uictx("tlctx") as tlctx:
        with Button({'key': "abtn",
                     'text':"click me",
                     'classes': "bg-green-100",
                     }
                    ) as abtn:
            pass

def on_click(dbref, msg, to_ms):
    #tlctx.mbtn.add_twsty_tags(bg/blue/1)
    pass

print(type(tlctx.abtn))
tlctx.abtn.on('click', on_click)                

