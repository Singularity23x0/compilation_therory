
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "nonassocIFXnonassocELSEleft+-left*/leftMTX_SUMMTX_DIFFERENCEleftMTX_PRODUCTMTX_QUOTIENTrightUMINUSrightTRANSPOSEADD BREAK CONT DIVIDE ELSE EQUAL EYE FLOAT FOR ID IF INT LARGER_OR_EQUAL MTX_DIFFERENCE MTX_PRODUCT MTX_QUOTIENT MTX_SUM MULTIPLY NOT_EQUAL ONES PRINT RETURN SMALLER_OR_EQUAL STRING SUBTRACT TRANSPOSE WHILE ZEROSprogram : segment\n    | segment : segment segment\n    | groupline : expression ';'block : '{' segment '}'for : FOR ID '=' range group range : value_element ':' value_elementwhile : WHILE '(' logical_expression ')' groupif : IF '(' logical_expression ')' group\n    | IF '(' logical_expression ')' group ELSE group %prec IFXgroup : conditional\n    | line\n    | block conditional : if\n    | while\n    | forvalue_element : ID\n    | arithmetic_expression\n    | FLOAT\n    | INT\n    | STRING\n    | '-' value_element %prec UMINUS\n    | value_element TRANSPOSE\n    | matrix_definitionmatrix_definition : '[' matrix_definition_inside ']'matrix_definition_inside : matrix_definition_inside matrix_definition_inside\n    | value_element ','arithmetic_expression : value_element arithmetic_operator value_element arithmetic_operator : '+'\n    | '-'\n    | '*'\n    | '/'\n    | MTX_SUM\n    | MTX_DIFFERENCE\n    | MTX_PRODUCT\n    | MTX_QUOTIENT expression : logical_expression\n        | assignment\n        | value_elementlogical_expression : value_element comparison_operator value_elementcomparison_operator : '<'\n    | '>'\n    | EQUAL\n    | NOT_EQUAL\n    | SMALLER_OR_EQUAL\n    | LARGER_OR_EQUALassignment : ID '=' value_element"
    
_lr_action_items = {'$end':([0,1,2,3,4,5,6,7,8,9,26,27,54,69,70,71,75,],[-2,0,-1,-4,-12,-13,-14,-15,-16,-17,-3,-5,-6,-10,-9,-7,-11,]),'{':([0,2,3,4,5,6,7,8,9,11,19,20,21,22,24,26,27,28,34,50,51,54,61,63,65,66,67,69,70,71,73,74,75,],[11,11,-4,-12,-13,-14,-15,-16,-17,11,-19,-20,-21,-22,-25,11,-5,11,-24,-23,-18,-6,-29,-26,11,11,11,-10,-9,-7,11,-8,-11,]),'IF':([0,2,3,4,5,6,7,8,9,11,19,20,21,22,24,26,27,28,34,50,51,54,61,63,65,66,67,69,70,71,73,74,75,],[12,12,-4,-12,-13,-14,-15,-16,-17,12,-19,-20,-21,-22,-25,12,-5,12,-24,-23,-18,-6,-29,-26,12,12,12,-10,-9,-7,12,-8,-11,]),'WHILE':([0,2,3,4,5,6,7,8,9,11,19,20,21,22,24,26,27,28,34,50,51,54,61,63,65,66,67,69,70,71,73,74,75,],[14,14,-4,-12,-13,-14,-15,-16,-17,14,-19,-20,-21,-22,-25,14,-5,14,-24,-23,-18,-6,-29,-26,14,14,14,-10,-9,-7,14,-8,-11,]),'FOR':([0,2,3,4,5,6,7,8,9,11,19,20,21,22,24,26,27,28,34,50,51,54,61,63,65,66,67,69,70,71,73,74,75,],[15,15,-4,-12,-13,-14,-15,-16,-17,15,-19,-20,-21,-22,-25,15,-5,15,-24,-23,-18,-6,-29,-26,15,15,15,-10,-9,-7,15,-8,-11,]),'ID':([0,2,3,4,5,6,7,8,9,11,15,19,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,58,61,62,63,64,65,66,67,69,70,71,72,73,74,75,],[16,16,-4,-12,-13,-14,-15,-16,-17,16,31,-19,-20,-21,-22,51,-25,51,16,-5,16,51,51,51,51,-24,51,-42,-43,-44,-45,-46,-47,-30,-31,-32,-33,-34,-35,-36,-37,-23,-18,51,-6,51,-29,51,-26,-28,16,16,16,-10,-9,-7,51,16,-8,-11,]),'FLOAT':([0,2,3,4,5,6,7,8,9,11,19,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,58,61,62,63,64,65,66,67,69,70,71,72,73,74,75,],[20,20,-4,-12,-13,-14,-15,-16,-17,20,-19,-20,-21,-22,20,-25,20,20,-5,20,20,20,20,20,-24,20,-42,-43,-44,-45,-46,-47,-30,-31,-32,-33,-34,-35,-36,-37,-23,-18,20,-6,20,-29,20,-26,-28,20,20,20,-10,-9,-7,20,20,-8,-11,]),'INT':([0,2,3,4,5,6,7,8,9,11,19,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,58,61,62,63,64,65,66,67,69,70,71,72,73,74,75,],[21,21,-4,-12,-13,-14,-15,-16,-17,21,-19,-20,-21,-22,21,-25,21,21,-5,21,21,21,21,21,-24,21,-42,-43,-44,-45,-46,-47,-30,-31,-32,-33,-34,-35,-36,-37,-23,-18,21,-6,21,-29,21,-26,-28,21,21,21,-10,-9,-7,21,21,-8,-11,]),'STRING':([0,2,3,4,5,6,7,8,9,11,19,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,58,61,62,63,64,65,66,67,69,70,71,72,73,74,75,],[22,22,-4,-12,-13,-14,-15,-16,-17,22,-19,-20,-21,-22,22,-25,22,22,-5,22,22,22,22,22,-24,22,-42,-43,-44,-45,-46,-47,-30,-31,-32,-33,-34,-35,-36,-37,-23,-18,22,-6,22,-29,22,-26,-28,22,22,22,-10,-9,-7,22,22,-8,-11,]),'-':([0,2,3,4,5,6,7,8,9,11,16,18,19,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,56,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,],[23,23,-4,-12,-13,-14,-15,-16,-17,23,-18,43,-19,-20,-21,-22,23,-25,23,23,-5,23,23,23,23,23,-24,23,-42,-43,-44,-45,-46,-47,-30,-31,-32,-33,-34,-35,-36,-37,-23,-18,23,43,-6,43,23,43,43,43,23,-26,-28,23,23,23,43,-10,-9,-7,23,23,43,-11,]),'[':([0,2,3,4,5,6,7,8,9,11,19,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,58,61,62,63,64,65,66,67,69,70,71,72,73,74,75,],[25,25,-4,-12,-13,-14,-15,-16,-17,25,-19,-20,-21,-22,25,-25,25,25,-5,25,25,25,25,25,-24,25,-42,-43,-44,-45,-46,-47,-30,-31,-32,-33,-34,-35,-36,-37,-23,-18,25,-6,25,-29,25,-26,-28,25,25,25,-10,-9,-7,25,25,-8,-11,]),'}':([3,4,5,6,7,8,9,26,27,28,54,69,70,71,75,],[-4,-12,-13,-14,-15,-16,-17,-3,-5,54,-6,-10,-9,-7,-11,]),'ELSE':([4,5,6,7,8,9,27,54,69,70,71,75,],[-12,-13,-14,-15,-16,-17,-5,-6,73,-9,-7,-11,]),';':([10,13,16,17,18,19,20,21,22,24,34,50,51,59,60,61,63,],[27,-38,-18,-39,-40,-19,-20,-21,-22,-25,-24,-23,-18,-48,-41,-29,-26,]),'(':([12,14,],[29,30,]),'=':([16,31,],[32,58,]),'TRANSPOSE':([16,18,19,20,21,22,24,34,50,51,53,56,59,60,61,63,68,74,],[-18,34,-19,-20,-21,-22,-25,-24,34,-18,34,34,34,34,34,-26,34,34,]),'<':([16,18,19,20,21,22,24,34,50,51,56,61,63,],[-18,36,-19,-20,-21,-22,-25,-24,-23,-18,36,-29,-26,]),'>':([16,18,19,20,21,22,24,34,50,51,56,61,63,],[-18,37,-19,-20,-21,-22,-25,-24,-23,-18,37,-29,-26,]),'EQUAL':([16,18,19,20,21,22,24,34,50,51,56,61,63,],[-18,38,-19,-20,-21,-22,-25,-24,-23,-18,38,-29,-26,]),'NOT_EQUAL':([16,18,19,20,21,22,24,34,50,51,56,61,63,],[-18,39,-19,-20,-21,-22,-25,-24,-23,-18,39,-29,-26,]),'SMALLER_OR_EQUAL':([16,18,19,20,21,22,24,34,50,51,56,61,63,],[-18,40,-19,-20,-21,-22,-25,-24,-23,-18,40,-29,-26,]),'LARGER_OR_EQUAL':([16,18,19,20,21,22,24,34,50,51,56,61,63,],[-18,41,-19,-20,-21,-22,-25,-24,-23,-18,41,-29,-26,]),'+':([16,18,19,20,21,22,24,34,50,51,53,56,59,60,61,63,68,74,],[-18,42,-19,-20,-21,-22,-25,-24,-23,-18,42,42,42,42,42,-26,42,42,]),'*':([16,18,19,20,21,22,24,34,50,51,53,56,59,60,61,63,68,74,],[-18,44,-19,-20,-21,-22,-25,-24,-23,-18,44,44,44,44,44,-26,44,44,]),'/':([16,18,19,20,21,22,24,34,50,51,53,56,59,60,61,63,68,74,],[-18,45,-19,-20,-21,-22,-25,-24,-23,-18,45,45,45,45,45,-26,45,45,]),'MTX_SUM':([16,18,19,20,21,22,24,34,50,51,53,56,59,60,61,63,68,74,],[-18,46,-19,-20,-21,-22,-25,-24,-23,-18,46,46,46,46,46,-26,46,46,]),'MTX_DIFFERENCE':([16,18,19,20,21,22,24,34,50,51,53,56,59,60,61,63,68,74,],[-18,47,-19,-20,-21,-22,-25,-24,-23,-18,47,47,47,47,47,-26,47,47,]),'MTX_PRODUCT':([16,18,19,20,21,22,24,34,50,51,53,56,59,60,61,63,68,74,],[-18,48,-19,-20,-21,-22,-25,-24,-23,-18,48,48,48,48,48,-26,48,48,]),'MTX_QUOTIENT':([16,18,19,20,21,22,24,34,50,51,53,56,59,60,61,63,68,74,],[-18,49,-19,-20,-21,-22,-25,-24,-23,-18,49,49,49,49,49,-26,49,49,]),',':([19,20,21,22,24,34,50,51,53,61,63,],[-19,-20,-21,-22,-25,-24,-23,-18,64,-29,-26,]),')':([19,20,21,22,24,34,50,51,55,57,60,61,63,],[-19,-20,-21,-22,-25,-24,-23,-18,65,66,-41,-29,-26,]),':':([19,20,21,22,24,34,50,51,61,63,68,],[-19,-20,-21,-22,-25,-24,-23,-18,-29,-26,72,]),']':([52,62,64,],[63,-27,-28,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'segment':([0,2,11,26,28,],[2,26,28,26,26,]),'group':([0,2,11,26,28,65,66,67,73,],[3,3,3,3,3,69,70,71,75,]),'conditional':([0,2,11,26,28,65,66,67,73,],[4,4,4,4,4,4,4,4,4,]),'line':([0,2,11,26,28,65,66,67,73,],[5,5,5,5,5,5,5,5,5,]),'block':([0,2,11,26,28,65,66,67,73,],[6,6,6,6,6,6,6,6,6,]),'if':([0,2,11,26,28,65,66,67,73,],[7,7,7,7,7,7,7,7,7,]),'while':([0,2,11,26,28,65,66,67,73,],[8,8,8,8,8,8,8,8,8,]),'for':([0,2,11,26,28,65,66,67,73,],[9,9,9,9,9,9,9,9,9,]),'expression':([0,2,11,26,28,65,66,67,73,],[10,10,10,10,10,10,10,10,10,]),'logical_expression':([0,2,11,26,28,29,30,65,66,67,73,],[13,13,13,13,13,55,57,13,13,13,13,]),'assignment':([0,2,11,26,28,65,66,67,73,],[17,17,17,17,17,17,17,17,17,]),'value_element':([0,2,11,23,25,26,28,29,30,32,33,35,52,58,62,65,66,67,72,73,],[18,18,18,50,53,18,18,56,56,59,60,61,53,68,53,18,18,18,74,18,]),'arithmetic_expression':([0,2,11,23,25,26,28,29,30,32,33,35,52,58,62,65,66,67,72,73,],[19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,]),'matrix_definition':([0,2,11,23,25,26,28,29,30,32,33,35,52,58,62,65,66,67,72,73,],[24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,]),'comparison_operator':([18,56,],[33,33,]),'arithmetic_operator':([18,50,53,56,59,60,61,68,74,],[35,35,35,35,35,35,35,35,35,]),'matrix_definition_inside':([25,52,62,],[52,62,62,]),'range':([58,],[67,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> segment','program',1,'p_program','parser2.py',23),
  ('program -> <empty>','program',0,'p_program','parser2.py',24),
  ('segment -> segment segment','segment',2,'p_segment','parser2.py',28),
  ('segment -> group','segment',1,'p_segment','parser2.py',29),
  ('line -> expression ;','line',2,'p_line','parser2.py',33),
  ('block -> { segment }','block',3,'p_block','parser2.py',37),
  ('for -> FOR ID = range group','for',5,'p_for','parser2.py',41),
  ('range -> value_element : value_element','range',3,'p_range','parser2.py',45),
  ('while -> WHILE ( logical_expression ) group','while',5,'p_while','parser2.py',49),
  ('if -> IF ( logical_expression ) group','if',5,'p_if','parser2.py',53),
  ('if -> IF ( logical_expression ) group ELSE group','if',7,'p_if','parser2.py',54),
  ('group -> conditional','group',1,'p_group','parser2.py',58),
  ('group -> line','group',1,'p_group','parser2.py',59),
  ('group -> block','group',1,'p_group','parser2.py',60),
  ('conditional -> if','conditional',1,'p_conditional','parser2.py',64),
  ('conditional -> while','conditional',1,'p_conditional','parser2.py',65),
  ('conditional -> for','conditional',1,'p_conditional','parser2.py',66),
  ('value_element -> ID','value_element',1,'p_value_element','parser2.py',70),
  ('value_element -> arithmetic_expression','value_element',1,'p_value_element','parser2.py',71),
  ('value_element -> FLOAT','value_element',1,'p_value_element','parser2.py',72),
  ('value_element -> INT','value_element',1,'p_value_element','parser2.py',73),
  ('value_element -> STRING','value_element',1,'p_value_element','parser2.py',74),
  ('value_element -> - value_element','value_element',2,'p_value_element','parser2.py',75),
  ('value_element -> value_element TRANSPOSE','value_element',2,'p_value_element','parser2.py',76),
  ('value_element -> matrix_definition','value_element',1,'p_value_element','parser2.py',77),
  ('matrix_definition -> [ matrix_definition_inside ]','matrix_definition',3,'p_matrix_definition','parser2.py',81),
  ('matrix_definition_inside -> matrix_definition_inside matrix_definition_inside','matrix_definition_inside',2,'p_matrix_definition_inside','parser2.py',85),
  ('matrix_definition_inside -> value_element ,','matrix_definition_inside',2,'p_matrix_definition_inside','parser2.py',86),
  ('arithmetic_expression -> value_element arithmetic_operator value_element','arithmetic_expression',3,'p_arithmetic_expression','parser2.py',90),
  ('arithmetic_operator -> +','arithmetic_operator',1,'p_arithmetic_operator','parser2.py',94),
  ('arithmetic_operator -> -','arithmetic_operator',1,'p_arithmetic_operator','parser2.py',95),
  ('arithmetic_operator -> *','arithmetic_operator',1,'p_arithmetic_operator','parser2.py',96),
  ('arithmetic_operator -> /','arithmetic_operator',1,'p_arithmetic_operator','parser2.py',97),
  ('arithmetic_operator -> MTX_SUM','arithmetic_operator',1,'p_arithmetic_operator','parser2.py',98),
  ('arithmetic_operator -> MTX_DIFFERENCE','arithmetic_operator',1,'p_arithmetic_operator','parser2.py',99),
  ('arithmetic_operator -> MTX_PRODUCT','arithmetic_operator',1,'p_arithmetic_operator','parser2.py',100),
  ('arithmetic_operator -> MTX_QUOTIENT','arithmetic_operator',1,'p_arithmetic_operator','parser2.py',101),
  ('expression -> logical_expression','expression',1,'p_expression','parser2.py',105),
  ('expression -> assignment','expression',1,'p_expression','parser2.py',106),
  ('expression -> value_element','expression',1,'p_expression','parser2.py',107),
  ('logical_expression -> value_element comparison_operator value_element','logical_expression',3,'p_logical_expression','parser2.py',111),
  ('comparison_operator -> <','comparison_operator',1,'p_comparison_operator','parser2.py',115),
  ('comparison_operator -> >','comparison_operator',1,'p_comparison_operator','parser2.py',116),
  ('comparison_operator -> EQUAL','comparison_operator',1,'p_comparison_operator','parser2.py',117),
  ('comparison_operator -> NOT_EQUAL','comparison_operator',1,'p_comparison_operator','parser2.py',118),
  ('comparison_operator -> SMALLER_OR_EQUAL','comparison_operator',1,'p_comparison_operator','parser2.py',119),
  ('comparison_operator -> LARGER_OR_EQUAL','comparison_operator',1,'p_comparison_operator','parser2.py',120),
  ('assignment -> ID = value_element','assignment',3,'p_assignment','parser2.py',124),
]
