import inspect
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﳜ=ImportError
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𐰁=issubclass
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴈ=True
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇䎉=TypeError
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇즅=False
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇퉴=hasattr
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𐠜=StopIteration
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇望=isinstance
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ڈ=tuple
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𩖒=None
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𐰖=list
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𓄇=inspect.getmembers
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ࡊ=inspect.getfile
import os
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇Ω=os.listdir
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﳴ=os.path
import platform
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𧱭=platform.system
import sys
ﲃﶉￋ疗ﭖﯚࡒ礼𪝇쉦=sys.path
from coalib.misc.Decorators import arguments_to_lists,yield_once
from coalib.misc.ContextManagers import suppress_stdout
def ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𩝆(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇㘰):
 if not ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﳴ.exists(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇㘰):
  raise ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﳜ
 ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﻤ=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﳴ.splitext(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﳴ.basename(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇㘰))[0]
 ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𣂋=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﳴ.dirname(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇㘰)
 if ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𣂋 not in ﲃﶉￋ疗ﭖﯚࡒ礼𪝇쉦:
  ﲃﶉￋ疗ﭖﯚࡒ礼𪝇쉦.insert(0,ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𣂋)
 if ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𧱭()=='Windows': 
  for ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𝟀 in ﲃﶉￋ疗ﭖﯚࡒ礼𪝇Ω(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𣂋):
   ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𞺡=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﳴ.splitext(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𝟀)[0]
   if ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𞺡.lower()==ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﻤ.lower():
    ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﻤ=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𞺡
    break
 return __import__(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﻤ)
def ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴴ(test_class,superclasses):
 for ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﮩ in superclasses:
  try:
   if ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𐰁(test_class,ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﮩ):
    return ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴈ
  except ﲃﶉￋ疗ﭖﯚࡒ礼𪝇䎉:
   pass
 return ﲃﶉￋ疗ﭖﯚࡒ礼𪝇즅
def ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﯘ(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ,attribute_names):
 for ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𦌤 in attribute_names:
  if not ﲃﶉￋ疗ﭖﯚࡒ礼𪝇퉴(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ,ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𦌤):
   return ﲃﶉￋ疗ﭖﯚࡒ礼𪝇즅
 return ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴈ
def ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﵶ(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ,ﲃﶉￋ疗ﭖﯚࡒ礼𪝇㘰):
 try:
  ﲃﶉￋ疗ﭖﯚࡒ礼𪝇呾=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ࡊ(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ)
  if(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𧱭()=='Windows' and ﲃﶉￋ疗ﭖﯚࡒ礼𪝇呾.lower()==ﲃﶉￋ疗ﭖﯚࡒ礼𪝇㘰.lower()or ﲃﶉￋ疗ﭖﯚࡒ礼𪝇呾==ﲃﶉￋ疗ﭖﯚࡒ礼𪝇㘰):
   return ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴈ
 except ﲃﶉￋ疗ﭖﯚࡒ礼𪝇䎉: 
  pass
 return ﲃﶉￋ疗ﭖﯚࡒ礼𪝇즅
@arguments_to_lists
@yield_once
def ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𦊐(file_paths,names,types,supers,attributes,local):
 if file_paths==[]or (names==[]and types==[]and supers==[]and attributes==[]):
  raise ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𐠜
 for ﲃﶉￋ疗ﭖﯚࡒ礼𪝇㘰 in file_paths:
  try:
   ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𐩶=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𩝆(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇㘰)
   for ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𐨧,ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ in ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𓄇(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𐩶):
    if(names==[]or ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𐨧 in names)and (types==[]or ﲃﶉￋ疗ﭖﯚࡒ礼𪝇望(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ,ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ڈ(types)))and (supers==[]or ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴴ(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ,supers))and (attributes==[]or ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﯘ(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ,attributes))and (local[0]is ﲃﶉￋ疗ﭖﯚࡒ礼𪝇즅 or ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﵶ(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ,ﲃﶉￋ疗ﭖﯚࡒ礼𪝇㘰)):
     yield ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ
  except ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﳜ:
   pass
def ﲃﶉￋ疗ﭖﯚࡒ礼𪝇乼(file_paths,names=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𩖒,types=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𩖒,supers=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𩖒,attributes=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𩖒,local=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇즅,verbose=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇즅):
 if not verbose:
  with suppress_stdout():
   for ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ in ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𦊐(file_paths,names,types,supers,attributes,local):
    yield ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ
 else:
  for ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ in ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𦊐(file_paths,names,types,supers,attributes,local):
   yield ﲃﶉￋ疗ﭖﯚࡒ礼𪝇ﴐ
def ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𡂇(file_paths,names=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𩖒,types=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𩖒,supers=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𩖒,attributes=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𩖒,local=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇즅,verbose=ﲃﶉￋ疗ﭖﯚࡒ礼𪝇즅):
 return ﲃﶉￋ疗ﭖﯚࡒ礼𪝇𐰖(ﲃﶉￋ疗ﭖﯚࡒ礼𪝇乼(file_paths,names,types,supers,attributes,local,verbose))
