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


with writer_ctx:
    with Div(classes = "bg-blue-100") as tldiv:
        with Span(text = "hello", twsty_tags=[bg/blue/100, fc/green/800]):            
            pass
        with Span(text = "world", classes = "bg-green-100 text-pink-800"):
            pass

        pass

print(tldiv)            

app = oj.load_app()

endpoint = oj.create_endpoint("demo_html_writer",
                              childs = [tldiv],
                              title="Demo html writer"
                              )

                              
oj.add_jproute("/", endpoint)
