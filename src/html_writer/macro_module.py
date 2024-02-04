from py_tailwind_utils import *
from macropy.core.macros import Macros
import ast


macros = Macros()

def translater(comp_type,
               comp_label,
               kwargs_nodes,
               target_ast_node=None, 
               child_comp_call_trees=[]
               ):
    """
    comp_type: passive, active div/no-chiles, mutable, HCCMutable, etc.
    comp_label: what component needs to be generated: Like PC.Div, PC.Span, AC.Button
    kwargs_nodes: list of kwarg nodes: ast.keyword(arg=..., value=...) e.g. arg=text, value="hello"
    target_ast_node: target of with context. `with myctx(..) as X`. Here ast.Name(id="X"..) is the target. 
    child_comp_call_trees: a list of ast each represent call-tree for child node creation
    """
    
    
    num_childs = len(child_comp_call_trees)

    # for no good reason we have four class of htmlcomponents
    # based on if they can hold childrens or not, if they
    # are mutable/responsive vs. passive
    # we decide which one to use based if arguments to the component
    # has key and if they have childrens
    attr = 'PC'
    if comp_type == 'Active':
            
        if num_childs == 0:
            attr='AC'
        else:
            attr = 'AD'

    elif comp_type == 'Passive':
        if num_childs == 0:
            attr='PC'
        else:
            attr = 'PD'
    elif comp_type == 'Mutable':
        attr= 'Mutable'
        comp_label = comp_label.replace("Mutable_", "")
    elif comp_type == "HCCMutable":
        attr = "HCCMutable"
        comp_label = comp_label.replace("HCCMutable_", "")
        
    elif comp_type == "HCCStatic":
        attr = "HCCStatic"
        comp_label = comp_label.replace("HCCStatic_", "")
            

    
    # The html component generator
    # e.g. oj.PC.Div, or oj.AD.Button
    div_func = ast.Attribute(
        value=ast.Attribute(
            value=ast.Name(id='oj', ctx=ast.Load()),
            attr=attr,
            ctx=ast.Load()
        ),
        attr=comp_label,
        ctx=ast.Load()
    )
    
    # Create an additional keyword argument for 'childs' with an empty list as its value
    childs_keyword = ast.keyword(arg='childs',
                                 value=ast.List(elts=child_comp_call_trees, ctx=ast.Load())
                                 )

    call_ast = ast.Call(div_func,
                        args=[],
                        keywords=[ *kwargs_nodes, childs_keyword]
                        )
    if target_ast_node:
        assign_statement = ast.Assign(targets=[target_ast_node], value=call_ast)
        return assign_statement, ast.Name(id=target_ast_node.id, ctx=ast.Load())
    else:
        return None, call_ast





def kwargs_has_key(keywords):
    for _ in keywords:
        if _.arg == "key":
            return True
    
    return False

    
def deal_with_inner_with_block(block_tree):
    # get the with blocks in the body
    assert isinstance(block_tree, ast.With)
    # get the with-blocks in the body of the With context

    child_with_blocks = [node for node in block_tree.body if isinstance(node, ast.With)]
    child_comp_call_trees = []
    assign_stmts = []
    for child_with_block in child_with_blocks:
        X = deal_with_inner_with_block(child_with_block)
        child_assign_stmts = X[0]
        ref = X[1]
        assign_stmts.extend(child_assign_stmts)
        child_comp_call_trees.append(ref)
        
    withitem = block_tree.items[0]
    target_ast_node = None
    if withitem.optional_vars:
        target_ast_node = withitem.optional_vars
        pass

    # The is the context expression `with myctx()`
    context_expr = withitem.context_expr
    if isinstance(context_expr, ast.Call):
        
        func_node = context_expr.func

        comp_type = 'Passive'
        if kwargs_has_key(context_expr.keywords):
            comp_type = 'Active'

        if func_node.id.startswith("Mutable_"):
            comp_type = "Mutable"

        if func_node.id.startswith("HCCMutable_"):
            comp_type = "HCCMutable"

        if func_node.id.startswith("HCCStatic_"):
            comp_type = "HCCStatic"


        assign_stmt, ref = translater(comp_type,
                              func_node.id,
                              context_expr.keywords,
                              target_ast_node=target_ast_node,
                              child_comp_call_trees = child_comp_call_trees
                              )
        if assign_stmt:
            assign_stmts.append(assign_stmt)
        return (assign_stmts, ref)
    elif isinstance(context_expr, ast.Name):
        comp_id = context_expr.id
        comp_type = 'Passive'
        assign_stmt, ref = translater(comp_type, comp_id, [], child_comp_call_trees = child_comp_call_trees)
        if assign_stmt:
            assign_stmts.append(assign_stmt)
        return assign_stmts, ref
    else:
        assert False
        
    assert False


@macros.block
def writer_ctx(tree, *args, **kw):
    """
    a macro that patches the ast-tree
    : in our use-case -- tree is a list of With nodes
    """
    with_blocks = [node for node in tree if isinstance(node, ast.With)]
    assign_stmts, ref = deal_with_inner_with_block(with_blocks[0])
    if assign_stmts:
        if ref:
            # ditch the ref -- it is used only for additions to the child nodes
            return [*assign_stmts]
        else:
            assert False
            return assign_stmts
    else:
        if ref:
            assert False
            return [ref]
        else:
            assert False
            
    #return [deal_with_inner_with_block(with_blocks[0])]



