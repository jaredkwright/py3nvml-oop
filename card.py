from py3nvml.py3nvml import *
from py3nvml.nvidia_smi import StrGOM
import datetime

brandNames = {
	NVML_BRAND_UNKNOWN :  "Unknown",
	NVML_BRAND_QUADRO  :  "Quadro",
	NVML_BRAND_TESLA   :  "Tesla",
	NVML_BRAND_NVS     :  "NVS",
	NVML_BRAND_GRID    :  "Grid",
	NVML_BRAND_GEFORCE :  "GeForce",
}



def handleError(err):
	if (err.value == NVML_ERROR_UNINITIALIZED):
		print("\nERROR: Attempted to access NVML without first initializing.")
		print("Be sure you call nvmlInit() prior to accessing NVML functions.")
		quit()
	elif (err.value == NVML_ERROR_NOT_SUPPORTED):
		return("NOT SUPPORTED")
	else:
		print(err.__str__())
		nvmlShutdown()
		quit()

class VideoCard:
	"""Represents an OOP way to handle video cards returned from NVML."""
	def __init__(self, i):
		self.index = i
		self.handle = nvmlDeviceGetHandleByIndex(i)
		self.name = str(nvmlDeviceGetName(self.handle))
		
		try:
			# if nvmlDeviceGetBrand() succeeds it is guaranteed to be in the dictionary
			self.brand = brandNames[nvmlDeviceGetBrand(self.handle)]
		except NVMLError as err:
			handleError(err)
			
		
		
		self.pciInfo = nvmlDeviceGetPciInfo(self.handle)
		self.busId = self.pciInfo.busId
		
	
	def serial(self):
		try:
			return nvmlDeviceGetSerial(self.handle)
		except NVMLError as err:
			return handleError(err)
	
		
	def uuid(self):
		try:
			return nvmlDeviceGetUUID(self.handle)
		except NVMLError as err:
			return handleError(err)	
	
	
	def minorNumber(self):
		try:
			return nvmlDeviceGetMinorNumber(self.handle)
		except NVMLError as err:
			return handleError(err)	


	def vBiosVersion(self):
		try:
			return nvmlDeviceGetVbiosVersion(self.handle)
		except NVMLError as err:
			return handleError(err)	
			
	
	def displayMode(self):
		try:
			return ('enabled' if (nvmlDeviceGetDisplayMode(self.handle) != 0) else 'disabled')
		except NVMLError as err:
			return handleError(err)
			
			
	def displayActive(self):
		try:
			return ('enabled' if (nvmlDeviceGetDisplayActive(self.handle) != 0) else 'disabled')
		except NVMLError as err:
			return handleError(err)		
	
	
	def persistenceMode(self):
		try:
			return ('enabled' if (nvmlDeviceGetPersistenceMode(self.handle) != 0) else 'disabled')
		except NVMLError as err:
			return handleError(err)
	
	
	def accountingMode(self):
		try:
			return ('enabled' if (nvmlDeviceGetAccountingMode(self.handle) != 0) else 'disabled')
		except NVMLError as err:
			return handleError(err)
			
			
	def accountingModeBufferSize(self):
		try:
			return nvmlDeviceGetAccountingBufferSize(self.handle)
		except NVMLError as err:
			return handleError(err)
			
			
	def currentDriverModel(self):
		try:
			return 'WDDM' if (nvmlDeviceGetCurrentDriverModel(self.handle) == NVML_DRIVER_WDDM) else 'TCC' 
		except NVMLError as err:
			return handleError(err)


	def pendingDriverModel(self):
		try:
			return 'WDDM' if (nvmlDeviceGetPendingDriverModel(self.handle) == NVML_DRIVER_WDDM) else 'TCC' 
		except NVMLError as err:
			return handleError(err)		


	def multiGpuBoard(self):
		try:
			multiGpuBool = nvmlDeviceGetMultiGpuBoard(self.handle)
		except NVMLError as err:
			return handleError(err);

		if multiGpuBool:
			return True
		else:
			return False

	
	def boardId(self):
		try:
			boardId = nvmlDeviceGetBoardId(self.handle)
		except NVMLError as err:
			boardId = handleError(err)

		try:
			hexBID = "0x%x" % boardId
		except: 
			hexBID = boardId

		return hexBID
	
	
	def infoRomVersion(self):
		inforom = {}
		
		try:
			inforom["img_version"] = nvmlDeviceGetInforomImageVersion(self.handle)
		except NVMLError as err:
			inforom["img_version"] = handleError(err)
		
		try:
			inforom["oem_object"] = nvmlDeviceGetInforomVersion(self.handle, NVML_INFOROM_OEM)
		except NVMLError as err:
			inforom["oem_object"] = handleError(err)
	
		try:
			inforom["ecc_object"] = nvmlDeviceGetInforomVersion(self.handle, NVML_INFOROM_ECC)
		except NVMLError as err:
			inforom["ecc_object"] = handleError(err)
			
		try:
			inforom["pwr_object"] = nvmlDeviceGetInforomVersion(self.handle, NVML_INFOROM_POWER)
		except NVMLError as err:
			inforom["pwr_object"] = handleError(err)
			
		return inforom
		
	
	def currentGpuOperationMode(self):
		try:
			current = nvmlDeviceGetCurrentGpuOperationMode(self.handle)
		except NVMLError as err:
			current = handleError(err)
		return current
		
	
	def pendingGpuOperationMode(self):
		try:
			pending = nvmlDeviceGetPendingGpuOperationMode(self.handle)
		except NVMLError as err:
			pending = handleError(err)
		return pending
		
	
	def pciGpuLinkInfo(self):
		info = {
			'pcie_gen': {},
			'link_widths': {}
		}
		
		try:
			info["pcie_gen"]["max_link_gen"] = nvmlDeviceGetMaxPcieLinkGeneration(self.handle)
		except NVMLError as err:
			info["pcie_gen"]["max_link_gen"] = handleError(err)
		try:
			info["pcie_gen"]["current_link_gen"] = nvmlDeviceGetCurrPcieLinkGeneration(self.handle)
		except NVMLError as err:
			info["pcie_gen"]["current_link_gen"] = handleError(err)
		try:
			info["link_widths"]["max_link_width"] = nvmlDeviceGetMaxPcieLinkWidth(self.handle)
		except NVMLError as err:
			info["link_widths"]["max_link_width"] = handleError(err)
		try:
			info["link_widths"]["current_link_width"] = nvmlDeviceGetCurrPcieLinkWidth(self.handle)
		except NVMLError as err:
			info["link_widths"]["current_link_width"] = handleError(err)
	
		return info
	
	
	def pciBridgeChip(self):
		chip = {
			'bridge_chip_type': '',
			'bridge_chip_fw': ''
		}
		try:
			bridgeHierarchy = nvmlDeviceGetBridgeChipInfo(self.handle)
			bridge_type = ''
			if bridgeHierarchy.bridgeChipInfo[0].type == 0:
				bridge_type += 'PLX'
			else:
				bridge_type += 'BR04'                    
			chip['bridge_chip_type'] =  bridge_type

			if bridgeHierarchy.bridgeChipInfo[0].fwVersion == 0:
				strFwVersion = 'N/A'
			else:
				strFwVersion = '%08X' % (bridgeHierarchy.bridgeChipInfo[0].fwVersion)
			chip['bridge_chip_fw'] = strFwVersion
		except NVMLError as err:
			chip['bridge_chip_type'] =  handleError(err)
			chip['bridge_chip_fw'] = handleError(err)

		return chip
		
	
	def replayCounter(self):
		try:
			replay = nvmlDeviceGetPcieReplayCounter(self.handle)
		except NVMLError as err:
			replay = handleError(err)
		return replay
		
		
	def fanSpeed(self):
		"""Number returned is fan speed % out of 100."""
		try:
			return nvmlDeviceGetFanSpeed(self.handle)
		except NVMLError as err:
			return handleError(err)
		
		
	def performanceState(self):
		"""Returns "power state" of device."""
		try:
			return nvmlDeviceGetPowerState(self.handle)
		except NVMLError as err:
			return handleError(err)
		
		
	def pcieThroughput(self):
		throughput = {
			'tx_kb_sec': 0,
			'rx_kb_sec': 0
		}
		try:
			throughput['tx_kb_sec'] = nvmlDeviceGetPcieThroughput(self.handle, NVML_PCIE_UTIL_TX_BYTES)
		except NVMLError as err:
			throughput['tx_kb_sec'] =  handleError(err)

		try:
			throughput['rx_kb_sec'] = nvmlDeviceGetPcieThroughput(self.handle, NVML_PCIE_UTIL_RX_BYTES)
		except NVMLError as err:
			throughput['rx_kb_sec'] =  handleError(err)
	
		return throughput
		
	
	def memInfo(self):
		info = {}
		try:
			memInfo = nvmlDeviceGetMemoryInfo(self.handle)
			mem_total = str(memInfo.total / 1024 / 1024) + ' MiB'
			mem_used = str(memInfo.used / 1024 / 1024) + ' MiB'
			mem_free = str(memInfo.total / 1024 / 1024 - memInfo.used / 1024 / 1024) + ' MiB'
		except NVMLError as err:
			error = handleError(err)
			mem_total = error
			mem_used = error
			mem_free = error
		info['memory'] = {}
		info['memory']['total'] = memInfo.total
		info['memory']['used'] = memInfo.used
		info['memory']['free'] = memInfo.total - memInfo.used
		info['total'] = mem_total
		info['used'] = mem_used
		info['free'] = mem_free
		return info
		
		
	def bar1MemInfo(self):
		info = {}
		try:
			memInfo = nvmlDeviceGetBAR1MemoryInfo(self.handle)
			mem_total = str(memInfo.bar1Total  / 1024 / 1024) + ' MiB'
			mem_used = str(memInfo.bar1Used  / 1024 / 1024) + ' MiB'
			mem_free = str(memInfo.bar1Total  / 1024 / 1024 - memInfo.bar1Used  / 1024 / 1024) + ' MiB'
		except NVMLError as err:
			error = handleError(err)
			mem_total = error
			mem_used = error
			mem_free = error
		info['memory'] = {}
		info['memory']['total'] = memInfo.bar1Total 
		info['memory']['used'] = memInfo.bar1Used 
		info['memory']['free'] = memInfo.bar1Total  - memInfo.bar1Used 
		info['total'] = mem_total
		info['used'] = mem_used
		info['free'] = mem_free
		return info
		
		
	def computeMode(self):
		compute_mode = {}
	
		try:
			mode = nvmlDeviceGetComputeMode(self.handle)
			if mode == NVML_COMPUTEMODE_DEFAULT:
				modeStr = 'Default'
			elif mode == NVML_COMPUTEMODE_EXCLUSIVE_THREAD:
				modeStr = 'Exclusive Thread'
			elif mode == NVML_COMPUTEMODE_PROHIBITED:
				modeStr = 'Prohibited'
			elif mode == NVML_COMPUTEMODE_EXCLUSIVE_PROCESS:
				modeStr = 'Exclusive_Process'
			else:
				modeStr = 'Unknown'
		except NVMLError as err:
			modeStr = handleError(err)
			
		compute_mode['mode'] = mode
		compute_mode['mode_str'] = modeStr
		return compute_mode
		
	def clocksThrottleReasons(self):
		throttleReasons = [
				[nvmlClocksThrottleReasonGpuIdle,           "clocks_throttle_reason_gpu_idle"],
				[nvmlClocksThrottleReasonUserDefinedClocks, "clocks_throttle_reason_user_defined_clocks"],
				[nvmlClocksThrottleReasonApplicationsClocksSetting, "clocks_throttle_reason_applications_clocks_setting"],
				[nvmlClocksThrottleReasonSwPowerCap,        "clocks_throttle_reason_sw_power_cap"],
				[nvmlClocksThrottleReasonHwSlowdown,        "clocks_throttle_reason_hw_slowdown"],
				[nvmlClocksThrottleReasonUnknown,           "clocks_throttle_reason_unknown"]
				];

		reasons = {}

		try:
			supportedClocksThrottleReasons = nvmlDeviceGetSupportedClocksThrottleReasons(self.handle)
			clocksThrottleReasons = nvmlDeviceGetCurrentClocksThrottleReasons(self.handle)
			
			for (mask, name) in throttleReasons:
				if (name != "clocks_throttle_reason_user_defined_clocks"):
					if (mask & supportedClocksThrottleReasons):
						val = True if mask & clocksThrottleReasons else False
					else:
						val = handleError(NVML_ERROR_NOT_SUPPORTED);
					reasons[name] = val
		except NVMLError as err:
			return handleError(err)

		return reasons
	
	
	def utilizationRates(self):
		rates = {
			'gpu': 0,
			'memory': 0,
			'encoder': 0,
			'decoder': 0
		}
		try:
			util = nvmlDeviceGetUtilizationRates(self.handle)
			rates['gpu'] = util.gpu
			rates['memory'] = util.memory
			gpu_util = str(util.gpu) + '%'
			mem_util = str(util.memory) + '%'
		except NVMLError as err:
			error = handleError(err)
			gpu_util = error
			mem_util = error
		rates['gpu_util'] = gpu_util		
		rates['mem_util'] = mem_util
		
		try:
			(util_int, ssize) = nvmlDeviceGetEncoderUtilization(self.handle)
			rates['encoder'] = util_int
			encoder_util = str(util_int) + '%'
		except NVMLError as err:
			error = handleError(err)
			encoder_util = error

		rates['encoder_util'] = encoder_util

		try:
			(util_int, ssize) = nvmlDeviceGetDecoderUtilization(self.handle)
			rates['decoder'] = util_int
			decoder_util = str(util_int) + '%'
		except NVMLError as err:
			error = handleError(err)
			decoder_util = error

		rates['decoder_util'] = decoder_util
		
		return rates
		
		
	def temperatureThresholds(self):
		"""Returns temperature thresholds in degrees Celsius."""
		current = {}
		try:
			current['shutdown_threshold'] = nvmlDeviceGetTemperatureThreshold(self.handle, NVML_TEMPERATURE_THRESHOLD_SHUTDOWN)
		except NVMLError as err:
			current['shutdown_threshold'] = handleError(err)
	
		try:
			current['slowdown_threshold'] = nvmlDeviceGetTemperatureThreshold(self.handle, NVML_TEMPERATURE_THRESHOLD_SLOWDOWN)
		except NVMLError as err:
			current['slowdown_threshold'] = handleError(err)
			
		return current
		
		
	def temperature(self):
		"""Returns temperature in degrees Celsius."""
		try:
			return nvmlDeviceGetTemperature(self.handle, NVML_TEMPERATURE_GPU)
		except NVMLError as err:
			return handleError(err)

			
	def powerUsage(self):
		current = {
			'draw': None,
			'usage': None
		}
		try:
			powDraw = nvmlDeviceGetPowerUsage(self.handle)
			powDrawStr = '%.2f W' % (powDraw / 1000.0)
			current['draw'] = powDraw
			current['usage'] = powDrawStr
		except NVMLError as err:
			powDrawStr = handleError(err)
			current['usage'] = powDrawStr
		
		return current
		
		
	def powerSettings(self):
		current = {
			'power_state': {},
			'power_management_mode': {},
			'power_management_limit': {},
			'power_management_default_limit': {},
			'enforced_power_limit': {},
			'power_management_limit_constraints': {}
		}
		
		try:
			perfState = nvmlDeviceGetPowerState(self.handle)
			current['power_state']['state'] = perfState
			current['power_state']['state_str'] = 'P' + str(perfState)
		except NVMLError as err:
			current['power_state']['state_str'] = handleError(err)
		
		try:
			powMan = nvmlDeviceGetPowerManagementMode(self.handle)
			current['power_management_mode']['mode'] = powMan
			current['power_management_mode']['mode_str'] = 'Supported' if powMan != 0 else 'N/A'
		except NVMLError as err:
			current['power_management_mode']['mode_str'] = handleError(err)
			
		try:
			powLimit = nvmlDeviceGetPowerManagementLimit(self.handle)
			powLimitStr  = '%.2f W' % (powLimit / 1000.0)
			current['power_management_limit']['limit'] = powLimit
			current['power_management_limit']['limit_str'] = powLimitStr
		except NVMLError as err:
			powLimitStr = handleError(err)
			current['power_management_limit']['limit_str'] = powLimitStr
			
		try:
			powLimit = nvmlDeviceGetPowerManagementDefaultLimit(self.handle)
			powLimitStr  = '%.2f W' % (powLimit / 1000.0)
			current['power_management_default_limit']['limit'] = powLimit
			current['power_management_default_limit']['limit_str'] = powLimitStr
		except NVMLError as err:
			powLimitStr = handleError(err)
			current['power_management_default_limit']['limit_str'] = powLimitStr
			
		try:
			powLimit = nvmlDeviceGetEnforcedPowerLimit(self.handle)
			powLimitStr  = '%.2f W' % (powLimit / 1000.0)
			current['enforced_power_limit']['limit'] = powLimit
			current['enforced_power_limit']['limit_str'] = powLimitStr
		except NVMLError as err:
			powLimitStr = handleError(err)
			current['enforced_power_limit']['limit_str'] = powLimitStr
			
		try:
			powLimit = nvmlDeviceGetPowerManagementLimitConstraints(self.handle)
			powLimitMin = powLimit[0]
			powLimitMax = powLimit[1]
			powLimitStrMin = '%.2f W' % (powLimitMin / 1000.0)
			powLimitStrMax = '%.2f W' % (powLimitMax / 1000.0)
			current['power_management_limit_constraints']['limit_min'] = powLimitMin
			current['power_management_limit_constraints']['limit_min_str'] = powLimitStrMin
			current['power_management_limit_constraints']['limit_max'] = powLimitMax
			current['power_management_limit_constraints']['limit_max_str'] = powLimitStrMax
		except NVMLError as err:
			powLimitStr = handleError(err)
			current['power_management_limit_constraints']['limit_min_str'] = powLimitStr
			current['power_management_limit_constraints']['limit_max_str'] = powLimitStr
		
		return current
			
	
	def gpuClock(self):
		current = {
			'rate': None
		}
		try:
			clockRate = nvmlDeviceGetClockInfo(self.handle, NVML_CLOCK_GRAPHICS)
			current['rate'] = clockRate
			current['rate_str'] = str(clockRate) + ' MHz'
		except NVMLError as err:
			current['rate_str'] = handleError(err)
	
		return current
	
	
	def gpuMaxClock(self):
		current = {
			'rate': None
		}
		try:
			clockRate = nvmlDeviceGetMaxClockInfo(self.handle, NVML_CLOCK_GRAPHICS)
			current['rate'] = clockRate
			current['rate_str'] = str(clockRate) + ' MHz'
		except NVMLError as err:
			current['rate_str'] = handleError(err)
	
		return current
	
	
	def gpuApplicationsClock(self):
		current = {
			'rate': None
		}
		try:
			clockRate = nvmlDeviceGetApplicationsClock(self.handle, NVML_CLOCK_GRAPHICS)
			current['rate'] = clockRate
			current['rate_str'] = str(clockRate) + ' MHz'
		except NVMLError as err:
			current['rate_str'] = handleError(err)
	
		return current
	
	
	def gpuDefaultApplicationsClock(self):
		current = {
			'rate': None
		}
		try:
			clockRate = nvmlDeviceGetDefaultApplicationsClock(self.handle, NVML_CLOCK_GRAPHICS)
			current['rate'] = clockRate
			current['rate_str'] = str(clockRate) + ' MHz'
		except NVMLError as err:
			current['rate_str'] = handleError(err)
	
		return current
	
	
	def memoryClock(self):
		current = {
			'rate': None
		}
		try:
			clockRate = nvmlDeviceGetClockInfo(self.handle, NVML_CLOCK_MEM)
			current['rate'] = clockRate
			current['rate_str'] = str(clockRate) + ' MHz'
		except NVMLError as err:
			current['rate_str'] = handleError(err)
	
		return current
		
	
	def memoryMaxClock(self):
		current = {
			'rate': None
		}
		try:
			clockRate = nvmlDeviceGetMaxClockInfo(self.handle, NVML_CLOCK_MEM)
			current['rate'] = clockRate
			current['rate_str'] = str(clockRate) + ' MHz'
		except NVMLError as err:
			current['rate_str'] = handleError(err)
	
		return current
	
	
	def memoryApplicationsClock(self):
		current = {
			'rate': None
		}
		try:
			clockRate = nvmlDeviceGetApplicationsClock(self.handle, NVML_CLOCK_MEM)
			current['rate'] = clockRate
			current['rate_str'] = str(clockRate) + ' MHz'
		except NVMLError as err:
			current['rate_str'] = handleError(err)
	
		return current
		
		
	def memoryDefaultApplicationsClock(self):
		current = {
			'rate': None
		}
		try:
			clockRate = nvmlDeviceGetDefaultApplicationsClock(self.handle, NVML_CLOCK_MEM)
			current['rate'] = clockRate
			current['rate_str'] = str(clockRate) + ' MHz'
		except NVMLError as err:
			current['rate_str'] = handleError(err)
	
		return current
	
	
	def smClock(self):
		current = {
			'rate': None
		}
		try:
			clockRate = nvmlDeviceGetClockInfo(self.handle, NVML_CLOCK_SM)
			current['rate'] = clockRate
			current['rate_str'] = str(clockRate) + ' MHz'
		except NVMLError as err:
			current['rate_str'] = handleError(err)
	
		return current
		
		
	def smMaxClock(self):
		current = {
			'rate': None
		}
		try:
			clockRate = nvmlDeviceGetMaxClockInfo(self.handle, NVML_CLOCK_SM)
			current['rate'] = clockRate
			current['rate_str'] = str(clockRate) + ' MHz'
		except NVMLError as err:
			current['rate_str'] = handleError(err)
	
		return current
		
		
	def autoBoostedClocksEnabled(self):
		try:
			boostedState, boostedDefaultState = nvmlDeviceGetAutoBoostedClocksEnabled(self.handle)
			if boostedState == NVML_FEATURE_DISABLED:
				autoBoostStr = "Off"
			else:
				autoBoostStr = "On"
			
			if boostedDefaultState == NVML_FEATURE_DISABLED:
				autoBoostDefaultStr = "Off"
			else:
				autoBoostDefaultStr = "On"
			
		except NVMLError_NotSupported:
			autoBoostStr = "N/A"
			autoBoostDefaultStr = "N/A"
		except NVMLError as err:
			autoBoostStr = handleError(err)
			autoBoostDefaultStr = handleError(err)
		
		return {
			'auto_boost': autoBoostStr,
			'auto_boost_default': autoBoostDefaultStr
		}
	
	
	def supportedClocks(self):
		final = []
		try:
			memClocks = nvmlDeviceGetSupportedMemoryClocks(self.handle)
			for m in memClocks:
				clobj = {
					'mem_clock': m,
					'gpu_clocks': []
				}
				try:
					clocks = nvmlDeviceGetSupportedGraphicsClocks(self.handle, m)
					for c in clocks:
						clobj['gpu_clocks'].append(c)
				except NVMLError as err:
					clobj['gpu_clocks'] = handleError(err)
				final.append(clobj)

		except NVMLError as err:
			final = handleError(err)

		return final
	
	
	def describe(self):
		"""Logs info about VideoCard instance."""
		print("\nDEVICE {}".format(self.index))
		print("="*40)
		print("    Name: \t\t\t{}".format(self.name))
		print("    VBIOS Version: \t\t{}".format(str(self.vBiosVersion())))
		print("    UUID: \t\t\t{}".format(str(self.uuid())))
		print("    Board ID: \t\t\t{}".format(str(self.boardId())))
		print("    Brand: \t\t\t{}".format(self.brand))
		print("    Serial: \t\t\t{}".format(str(self.serial())))
		print("    Minor Number: \t\t{}".format(str(self.minorNumber())))
		print("    Multi GPU: \t\t\t{}".format(str(self.multiGpuBoard())))
		print("    Display Mode: \t\t{}".format(self.displayMode()))
		print("    Display Active: \t\t{}".format(self.displayActive()))
		print("    Persistence Mode: \t\t{}".format(self.persistenceMode()))
		print("    Accounting Mode: \t\t{}".format(self.accountingMode()))
		print("    Accounting Buffer Size: \t{}".format(str(self.accountingModeBufferSize())))
		print("    Current Driver Model: \t{}".format(self.currentDriverModel()))
		print("    Pending Driver Model: \t{}".format(self.pendingDriverModel()))
		infoRom = self.infoRomVersion()
		print("    InfoROM Image Version: \t{}".format(infoRom["img_version"]))
		print("            \t\tOEM: \t{}".format(infoRom["oem_object"]))
		print("            \t\tECC: \t{}".format(infoRom["ecc_object"]))
		print("            \t\tPWR: \t{}".format(infoRom["pwr_object"]))
		print("    Current GPU Operation Mode: {}".format(StrGOM(self.currentGpuOperationMode())))
		print("    Pending GPU Operation Mode: {}".format(StrGOM(self.pendingGpuOperationMode())))
		print("    \tPCI:")
		print("            \t\tBus: \t\t{}".format('%02X' % self.pciInfo.bus))
		print("            \t\tDevice: \t{}".format('%02X' % self.pciInfo.device))
		print("            \t\tDomain: \t{}".format('%04X' % self.pciInfo.domain))
		print("            \t\tBusId: \t\t{}".format(str(self.busId, 'utf-8')))
		print("            \t\tDeviceId: \t{}".format('%02X' % self.pciInfo.pciDeviceId))
		print("            \t\tSubsystemId: \t{}".format('%02X' % self.pciInfo.pciSubSystemId))
		
def getVideoCards():
	cards = []
	try:
		deviceCount = nvmlDeviceGetCount()
		for i in range(deviceCount):
			c = VideoCard(i)
			cards.append(c)
		return cards
	except NVMLError as err:
		handleError(err)
		return None


	