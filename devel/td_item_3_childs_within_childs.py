"""
childs of top-level components contain childs.
this is to excercise with-block parsing within with-blocks
"""
import html_writer.macro_module as mm
from html_writer.macro_module import macros, writer_ctx
from py_tailwind_utils import *
import ofjustpy as oj


# with TLDiv({'classes':"bg-green-100"}) as tldiv:
#     pass


with oj.uictx("tlctx") as tlctx:
    with writer_ctx:
        with Div({'classes':"bg-blue-100"}) as tldiv:
            with Span({'classes': "bg-blue-100"}):            
                pass
            with Span({'classes':"bg-green-100"}):
                pass
            # with Span({'classes':"bg-green-100"}):
            #     # with Span({'classes': "bg-blue-100"}):
            #     #     pass
            #     pass
            pass
        with Div({'classes':"bg-blue-100"}):
            pass
    print(tldiv)            

        
#             with Div({'classes':"bg-blue-100"}):
#                 with Span({"text":"hello", 'classes':"bg-green-100"}):
#                     pass

#                 with Span({"text":"hello", 'classes':"bg-green-100"}):

#                     pass    


