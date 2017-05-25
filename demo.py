from py3nvml.py3nvml import *
from card import VideoCard, getVideoCards
import datetime

def mainWork():
	print("\n{}: Driver Version: {}".format(datetime.date.today(), str(nvmlSystemGetDriverVersion())))
	
	vcs = getVideoCards()
	for c in vcs:
		print(c.fanSpeed())
		print(c.powerSettings())
		print(c.utilizationRates())
		print(c.temperature())
		print(c.powerUsage())
		print(c.gpuClock())
		print(c.gpuMaxClock())
		print(c.smClock())
		print(c.smMaxClock())
		print(c.memoryClock())
		print(c.memoryMaxClock())
		print(c.autoBoostedClocksEnabled())
		print(c.supportedClocks())

def run():
	# run function created to make organization easy
	# and so as not to forget to init and shutdown nvml 
	nvmlInit()
	
	mainWork()
	
	nvmlShutdown()

run()