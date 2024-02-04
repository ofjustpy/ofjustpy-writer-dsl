import html_writer.macro_module as mm
from html_writer.macro_module import macros, writer_ctx
from py_tailwind_utils import *
import ofjustpy as oj


# with TLDiv({'classes':"bg-green-100"}) as tldiv:
#     pass


# case 1: no childs
# translator returns
# X = Div(...) with ref being None

with writer_ctx:
    with Div(classes = "bg-blue-100") as tldiv:
        pass

