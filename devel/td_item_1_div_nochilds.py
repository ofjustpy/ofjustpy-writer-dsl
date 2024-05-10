from html_writer.macro_module import macros, Div
from py_tailwind_utils import *
import ofjustpy as oj


with oj.uictx("tlctx") as tlctx:
    with Div({'class':[bg/green/100]}) as tldiv:
        with Span({"text":"hello", 'classes':"bg-green-100"}):
            pass

        with Span({"text":"hello", 'classes':"bg-green-100"}):

            pass    

        # with Button({'key': "abtn",
        #              'text':"click me",
        #              'classes': "bg-green-100",
        #              'on_click': on_click}
        #             ):
        #     pass

        # with MButton({'key': "mbtn",
        #              'text':"click me",
        #              'classes': "bg-green-100",
        #              'on_click': on_click}
        #             ):
        #     pass


# def on_click(dbref, msg, to_ms):
#     tlctx.mbtn.add_twsty_tags(bg/blue/1)
#     pass
#tlctx.abtn.target.on('click', on_click)                
print(tldiv)
