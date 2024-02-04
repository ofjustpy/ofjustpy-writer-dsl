from py_tailwind_utils import *
from macropy.core.macros import Macros
import ast


macros = Macros()

def translater(comp_type,
               comp_label,
               dict_obj_ast_node,
               target_ast_node=None, 
               child_comp_call_trees=[]
               ):
    """
    comp_type: passive, active div/no-chiles, mutable, HCCMutable, etc.
    comp_label: what component needs to be generated: Like PC.Div, PC.Span, AC.Button
    child_comp_call_trees: a list of ast each represent call-tree for child node creation
    """
    attr = 'PC'
    num_childs = len(child_comp_call_trees)

    # for no good reason we have four class of htmlcomponents
    # based on if they can hold childrens or not 
    if comp_type == 'Active':
        if num_childs == 0:
            attr='AC'
        else:
            attr = 'AD'

    if comp_type == 'Passive':
        if num_childs == 0:
            attr='PC'
        else:
            attr = 'PD'
            

    div_func = ast.Attribute(
        value=ast.Attribute(
            value=ast.Name(id='oj', ctx=ast.Load()),
            attr=attr,
            ctx=ast.Load()
        ),
        attr=comp_label,
        ctx=ast.Load()
    )
    
    #div_func = ast.Name(id='Div', ctx=ast.Load())
    keyword_argument = ast.keyword(arg=None, value=dict_obj_ast_node)
    # Create an additional keyword argument for 'childs' with an empty list as its value
    childs_keyword = ast.keyword(arg='childs',
                                 value=ast.List(elts=child_comp_call_trees, ctx=ast.Load())
                                 )

    call_ast = ast.Call(div_func,
                        args=[],
                        keywords=[keyword_argument, childs_keyword]
                        )
    if target_ast_node:
        assign_statement = ast.Assign(targets=[target_ast_node], value=call_ast)
        return assign_statement
    else:
        return call_ast


# # translate inner with block statement
# def inner_with_block(comp_type, comp_label, dict_obj_ast_node, target_ast_node=None):
#     """
#     comp_type:
#     comp_label: what component needs to be generated: Like PC.Div, PC.Span, AC.Button
#     """
#     assert comp_type == "Passive"

#     div_func = ast.Attribute(
#         value=ast.Attribute(
#             value=ast.Name(id='oj', ctx=ast.Load()),
#             attr='PC',
#             ctx=ast.Load()
#         ),
#         attr=comp_label,
#         ctx=ast.Load()
#     )
    
#     #div_func = ast.Name(id='Div', ctx=ast.Load())
#     keyword_argument = ast.keyword(arg=None, value=dict_obj_ast_node)
#     # Create an additional keyword argument for 'childs' with an empty list as its value
#     childs_keyword = ast.keyword(arg='childs', value=ast.List(elts=[], ctx=ast.Load()))

#     call_ast = ast.Call(div_func,
#                         args=[],
#                         keywords=[keyword_argument, childs_keyword]
#                         )
#     if target_ast_node:
#         assign_statement = ast.Assign(targets=[target_ast_node], value=call_ast)
#         return assign_statement
#     else:
#         call_ast
        


def kwargs_has_key(dict_ast_node):
    for akey in dict_ast_node.keys:
        if akey.value == 'key':
            return True
    return False

    
def deal_with_inner_with_block(block_tree):
    # get the with blocks in the body
    assert isinstance(block_tree, ast.With)
    # get the with-blocks in the body of the With context

    child_with_blocks = [node for node in block_tree.body if isinstance(node, ast.With)]
    child_comp_call_trees = []
    for child_with_block in child_with_blocks:
        child_comp_call_trees.append(deal_with_inner_with_block(child_with_block))
        
    withitem = block_tree.items[0]
    target_ast_node = None
    if withitem.optional_vars:
        print("optional_vars = ", ast.dump(withitem.optional_vars))
        target_ast_node = withitem.optional_vars
        pass

    context_expr = withitem.context_expr
    print ("context_expr = ", ast.dump(context_expr))
    if isinstance(context_expr, ast.Call) and isinstance(context_expr.args[0], ast.Dict):
        func_node = context_expr.func
        kwargs_dict = context_expr.args[0]
        comp_type = 'Passive'
        if kwargs_has_key(kwargs_dict):
            comp_type = 'Active'

        # TODO: recursively call to deal with inner blocks
        call_ast = translater(comp_type,
                              func_node.id,
                              kwargs_dict,
                              target_ast_node=target_ast_node,
                              child_comp_call_trees = child_comp_call_trees
                              )
        return call_ast
    # else:
    #     assert False
        
    # assert False

# def create_generic_macro(element_type):
#     @macros.block
#     def element_macro(tree, *args, **kw):
#         print (kw.keys())
#         target = kw['target']

#         dict_obj_ast_node = kw['args'][0]
#         # child blocks
#         with_blocks = [node for node in tree if isinstance(node, ast.With)]
#         child_call_tree= [deal_with_inner_with_block(_) for _ in with_blocks]
#         return [translater('Active', element_type, dict_obj_ast_node, target)]

#     return element_macro

# Button = create_generic_macro('Button')




def generic_macro_handler(comp_type, hc_comp, tree, *args, **kw):
    assert 'target' in kw
    target = kw['target']
    dict_obj_ast_node = kw['args'][0]
    with_blocks = [node for node in tree if isinstance(node, ast.With)]
    print("inner blocks = ", with_blocks)
    child_call_tree= [deal_with_inner_with_block(_) for _ in with_blocks]
    return [translater(comp_type, hc_comp, dict_obj_ast_node, target, child_call_tree)]


def static_comp_macro_handler(hc_comp, tree, *args, **kw):
    dict_obj_ast_node = kw['args'][0]
    comp_type = 'Passive'
    if kwargs_has_key(dict_obj_ast_node):
        comp_type='Active'

    return generic_macro_handler(comp_type, hc_comp, tree, *args, **kw)
    
# @macros.block
# def Button(tree, *args, **kw):
#     """
#     a macro that does nothing but shows the ast
#     """
    
#     return static_comp_macro_handler('Button', tree, *args, **kw)

# import traceback
# import sys

# @macros.block
# def Span(tree, *args, **kw):
#     """
#     a macro that does nothing but shows the ast
#     """
#     print ("now parsing span")
#     return static_comp_macro_handler('Span', tree, *args, **kw)



# @macros.block
# def Div(tree, *args, **kw):
#     """
#     a macro that does nothing but shows the ast
#     """
    
#     return static_comp_macro_handler('Div', tree, *args, **kw)

# @macros.block
# def ODiv(tree, *args, **kw):
#     """
#     a macro that does nothing but shows the ast
#     """

#     print ("now parsing ODiv")
#     return static_comp_macro_handler('Div', tree, *args, **kw)

# @macros.block
# def writer_ctx(tree, *args, **kw):
#     """
#     a macro that does nothing but shows the ast
#     """
#     print ("now parsing IDiv")
#     with_blocks = [node for node in tree if isinstance(node, ast.With)]
#     print("inner blocks = ", with_blocks)
    
#     #return static_comp_macro_handler('Div', tree, *args, **kw)



@macros.block
def TLDiv(tree, *args, **kw):
    """
    a macro that does nothing but shows the ast
    """
    assert 'target' in kw
    target = kw['target']
    dict_obj_ast_node = kw['args'][0]
    comp_type = 'Passive'
    if kwargs_has_key(dict_obj_ast_node):
        comp_type='Active'
    with_blocks = [node for node in tree if isinstance(node, ast.With)]
    child_call_tree= [deal_with_inner_with_block(_) for _ in with_blocks]
    return [translater(comp_type, 'Div', dict_obj_ast_node, target, child_call_tree)]



@macros.block
def writer_ctx(tree, *args, **kw):
    """
    a macro that does nothing but shows the ast
    tree: in our use-case -- tree is a list of With nodes
    """
    with_blocks = [node for node in tree if isinstance(node, ast.With)]

    return [deal_with_inner_with_block(with_blocks[0])]



