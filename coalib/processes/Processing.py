import multiprocessing
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂߩ=NotImplementedError
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𢐯=sum
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂڗ=list
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ톱=filter
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𫖷=isinstance
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𧕌=len
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﭫ=open
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﰔ=UnicodeDecodeError
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂއ=Exception
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂބ=range
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣭗=False
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ脭=multiprocessing.cpu_count
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂｇ=multiprocessing.Process
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ鹻=multiprocessing.Manager
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐠲=multiprocessing.Queue
import queue
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ䎻=queue.Empty
from coalib.collecting.Collectors import collect_files
from coalib.collecting import Dependencies
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐦐=Dependencies.resolve
from coalib.output.printers import LOG_LEVEL
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ遆=LOG_LEVEL.WARNING
from coalib.processes.BearRunning import run
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᚘ=CONTROL_ELEMENT.GLOBAL_FINISHED
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞺓=CONTROL_ELEMENT.LOCAL_FINISHED
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𧍛=CONTROL_ELEMENT.GLOBAL
𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ좁=CONTROL_ELEMENT.LOCAL
from coalib.results.HiddenResult import HiddenResult
from coalib.settings.Setting import path_list
from coalib.misc.i18n import _
from coalib.processes.LogPrinterThread import LogPrinterThread
def 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐠪():
 try:
  return 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ脭()
 except 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂߩ: 
  return 2
def 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ륗(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ僰,any_list):
 for 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ镒 in any_list:
  𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ僰.put(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ镒)
def 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣂔(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸):
 return 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𢐯((1 if process.is_alive()else 0)for process in 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸)
def 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ脩(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﴳ,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﯘ,print_results):
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﴳ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂڗ(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ톱(lambda result:not 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𫖷(result,HiddenResult),𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﴳ))
 print_results(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﴳ,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕)
 return 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﯘ or 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𧕌(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﴳ)>0
def 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂޅ(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂޜ,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺑ):
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕={}
 for 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂݖ in 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂޜ:
  try:
   with 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﭫ(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂݖ,"r",encoding="utf-8")as f:
    𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕[𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂݖ]=f.readlines()
  except 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﰔ:
   𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺑ.warn(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𝞧("Failed to read file '{}'. It seems to contain " "non-unicode characters. Leaving it " "out.".format(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂݖ)))
  except 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂއ as 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﳲ: 
   𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺑ.log_exception(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𝞧("Failed to read file '{}' because of " "an unknown error. Leaving it " "out.").format(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂݖ),𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﳲ,log_level=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ遆)
 return 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕
def 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﵙ(section,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ滢,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐰲):
 for 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𢄦 in 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂބ(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𧕌(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ滢)):
  𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ滢[𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𢄦]=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ滢[𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𢄦](section,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐰲,TIMEOUT=0.1)
 for 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𢄦 in 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂބ(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𧕌(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ)):
  𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ[𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𢄦]=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ[𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𢄦](𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕,section,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐰲,TIMEOUT=0.1)
def 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣐍(section,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ滢,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ,job_count,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺑ):
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂޜ=collect_files(path_list(section.get('files',"")))
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂޅ(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂޜ,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺑ)
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐰅=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ鹻()
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣰯=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐠲()
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﱮ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐠲()
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩛀=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐰅.dict()
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﳸ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐰅.dict()
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐰲=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐠲()
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺊ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐠲()
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𠵑={"file_name_queue":𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﱮ,"local_bear_list":𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ滢,"global_bear_list":𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ,"global_bear_queue":𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣰯,"file_dict":𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕,"local_result_dict":𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩛀,"global_result_dict":𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﳸ,"message_queue":𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐰲,"control_queue":𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺊ,"timeout":0.1}
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﵙ(section,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ滢,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐰲)
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ륗(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﱮ,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕.keys())
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ륗(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣰯,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂބ(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𧕌(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ)))
 return([𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂｇ(target=run,kwargs=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𠵑)for 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𢄦 in 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂބ(job_count)],𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𠵑)
def 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﲗ(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺊ,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩛀,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﳸ,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕,print_results):
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ섑=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣂔(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸)
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﯘ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣭗
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐭉=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𧕌(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸)
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂک=[]
 while 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐭉>1 and 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ섑>1:
  try:
   𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𨦧,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᵴ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺊ.get(timeout=0.1)
   if 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𨦧==𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞺓:
    𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐭉-=1
   elif 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𨦧==𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ좁:
    assert 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐭉!=0
    𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﯘ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ脩(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩛀[𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᵴ],𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﯘ,print_results)
   elif 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𨦧==𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𧍛:
    𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂک.append(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᵴ)
  except 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ䎻:
   𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ섑=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣂔(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸)
 for 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ镒 in 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂک:
  𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﯘ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ脩(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﳸ[𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ镒],𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﯘ,print_results)
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ섑=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣂔(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸)
 while 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ섑>1:
  try:
   𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𨦧,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᵴ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺊ.get(timeout=0.1)
   if 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𨦧==𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𧍛:
    𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﯘ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ脩(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﳸ[𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᵴ],𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𞸕,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﯘ,print_results)
   else:
    assert 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𨦧==𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᚘ
    𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ섑=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣂔(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸)
  except 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ䎻:
   𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ섑=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣂔(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸)
 return 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﯘ
def 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺲ(section,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ滢,print_results,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺑ):
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ滢=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐦐(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ滢)
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐦐(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ)
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ섑=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐠪()
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﵥ=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣐍(section,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ滢,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂᶀ,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ섑,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺑ)
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐤇=LogPrinterThread(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﵥ["message_queue"],𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﺑ)
 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸.append(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐤇)
 for 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐦿 in 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸:
  𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐦿.start()
 try:
  return(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﲗ(𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸,𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﵥ["control_queue"],𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﵥ["local_result_dict"],𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﵥ["global_result_dict"],𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﵥ["file_dict"],print_results),𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﵥ["local_result_dict"],𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﵥ["global_result_dict"],𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂﵥ["file_dict"])
 finally:
  𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐤇.running=𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𣭗
  for 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐦿 in 𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𩴸:
   𩧡ﳍ𐰦𥏵𡍝𞺌𤳁𣄕ﴂ𐦿.join()
