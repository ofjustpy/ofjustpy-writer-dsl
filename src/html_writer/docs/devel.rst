When parsing with html_writer
--------------------------------
.. code-block:: python
   @macros.block
   def writer_ctx(tree, *args, **kw):

- tree is a list of with-block nodes
- if `with writer_ctx as X`  is used then PyMacro will pass X in kw['target']
- if `with writer_ctx(args)` is used then it supplied to kw['args'].


The python language/AST parser details

- for `with Div`
Div is ast.Name

- for `with Div(x, y)`
then its ast.Call  


Using macros
-------------
- need run.py
- add `import macropy.activate` to top of run.py
- import the file containing the macro
  
