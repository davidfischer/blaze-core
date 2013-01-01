
# /home/stephen/continuum/blazepro/blaze/datashape/dyacc.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = 'A\x8f\x0c\t-\xc9\x9f\x99\xad\xb3\xd4\xcd1\xe7-@'
    
_lr_action_items = {'LBRACE':([0,12,13,25,],[1,1,1,1,]),'NAME':([0,1,12,13,14,15,17,25,],[3,11,19,19,22,11,24,19,]),'SPACE':([3,4,21,22,],[-4,14,-3,-4,]),')':([5,6,16,18,19,27,],[-8,-6,-9,-5,-7,28,]),'(':([17,],[25,]),'NUMBER':([0,12,13,17,25,],[5,5,5,26,5,]),'RBRACE':([1,8,9,10,15,23,24,26,28,],[-16,16,-11,-12,-16,-10,-14,-15,-13,]),'EQUALS':([3,4,21,22,],[-4,13,-3,-4,]),'COMMA':([1,2,3,5,6,8,9,10,15,16,18,19,20,23,24,26,27,28,],[-16,12,-7,-8,-6,15,-11,-12,-16,-9,12,-7,12,15,-14,-15,12,-13,]),'COLON':([11,],[17,]),'$end':([2,3,5,6,7,16,18,19,20,],[-2,-7,-8,-6,0,-9,-5,-7,-1,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'rhs_expression':([0,12,13,25,],[2,18,20,27,]),'record_opt':([1,15,],[8,23,]),'lhs_expression':([0,14,],[4,21,]),'record':([0,12,13,25,],[6,6,6,6,]),'record_item':([1,15,],[9,9,]),'statement':([0,],[7,]),'empty':([1,15,],[10,10,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> lhs_expression EQUALS rhs_expression','statement',3,'p_statement_assign','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',130),
  ('statement -> rhs_expression','statement',1,'p_statement_expr','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',139),
  ('lhs_expression -> lhs_expression SPACE lhs_expression','lhs_expression',3,'p_lhs_expression','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',143),
  ('lhs_expression -> NAME','lhs_expression',1,'p_lhs_expression_node','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',148),
  ('rhs_expression -> rhs_expression COMMA rhs_expression','rhs_expression',3,'p_rhs_expression','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',152),
  ('rhs_expression -> record','rhs_expression',1,'p_rhs_expression_node1','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',157),
  ('rhs_expression -> NAME','rhs_expression',1,'p_rhs_expression_node2','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',161),
  ('rhs_expression -> NUMBER','rhs_expression',1,'p_rhs_expression_node2','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',162),
  ('record -> LBRACE record_opt RBRACE','record',3,'p_record','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',166),
  ('record_opt -> record_opt COMMA record_opt','record_opt',3,'p_record_opt1','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',174),
  ('record_opt -> record_item','record_opt',1,'p_record_opt2','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',178),
  ('record_opt -> empty','record_opt',1,'p_record_opt3','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',182),
  ('record_item -> NAME COLON ( rhs_expression )','record_item',5,'p_record_item1','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',186),
  ('record_item -> NAME COLON NAME','record_item',3,'p_record_item2','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',190),
  ('record_item -> NAME COLON NUMBER','record_item',3,'p_record_item2','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',191),
  ('empty -> <empty>','empty',0,'p_empty','/home/stephen/continuum/blazepro/blaze/datashape/parser.py',195),
]