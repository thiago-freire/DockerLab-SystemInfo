import psutil
import GPUtil
import platform
from datetime import datetime
import json


class SystemInformation:

    def __init__(self):
        
        self.__system = {
            "Processor": self.__getPS(),
            "CPU": self.__getCPUInfo(),
            "Memory": self.__getMemoryInfo(),
            "Disck": self.__getDisckInfo(),
            "Network": self.__getNetworkInfo(),
            "GPU": self.__getGPUInfo()
        }

    def __get_size(self, bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def __getPS(self):

        uname = platform.uname()

        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        boot = f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"

        processor = {"System": uname.system,
                     "NodeName": uname.node,
                     "Release": uname.release,
                     "Version": uname.version,
                     "Machine": uname.machine,
                     "Processor": uname.processor,
                     "Boot": boot}

        return processor
    
    def __getCPUInfo(self):

        cpufreq = psutil.cpu_freq()

        cpu = {"cores_fisicos": psutil.cpu_count(logical=False),
               "cores_total": psutil.cpu_count(logical=True),
               "freq_max": cpufreq.max,
               "freq_min": cpufreq.min,
               "frequencia": cpufreq.current,
               "list_uso": psutil.cpu_percent(percpu=True, interval=1),
               "uso_total": psutil.cpu_percent()
            }
        
        return cpu

    def __getMemoryInfo(self):

        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        memoria = {"Total": self.__get_size(svmem.total),
                   "Available": self.__get_size(svmem.available),
                   "Used": self.__get_size(svmem.used),
                   "Percentage": svmem.percent,
                   "SWAP_Total": self.__get_size(swap.total),
                   "SWAP_Free": self.__get_size(swap.free),
                   "SWAP_Used": self.__get_size(swap.used),
                   "SWAP_Percentage": swap.percent,
                }

        return memoria
    
    def __getDisckInfo(self):

        particoes = []

        partitions = psutil.disk_partitions()

        for partition in partitions:

            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                particoes.append({"device": partition.device,
                                   "mountpoint": partition.mountpoint,
                                   "file_system": partition.fstype
                                })
                continue
            
            disk_io = psutil.disk_io_counters()

            particoes.append({"device": partition.device,
                              "mountpoint": partition.mountpoint,
                              "file_system": partition.fstype,
                              "total_size": self.__get_size(partition_usage.total),
                              "used": self.__get_size(partition_usage.used),
                              "free": self.__get_size(partition_usage.free),
                              "percentage": partition_usage.percent,
                              "total_read": self.__get_size(disk_io.read_bytes),
                              "total_write": self.__get_size(disk_io.write_bytes)
                            })
        
        return particoes

    def __getNetworkInfo(self):

        if_addrs = psutil.net_if_addrs()
        net_io = psutil.net_io_counters()
        
        devices = []

        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:

                if str(address.family) == '2':
                    item = {interface_name:{"IP": address.address,
                                            "mascara": address.netmask,
                                            "broadcast": address.broadcast}}
                    devices.append(item)
                elif str(address.family) == '-1' or str(address.family) == '17':
                    devices.append({interface_name:{"MAC": address.address,
                                                    "mac_mascara": address.netmask,
                                                    "mac_broadcast": address.broadcast}})
                    
        network = {"total_sent": self.__get_size(net_io.bytes_sent),
                   "total_received": self.__get_size(net_io.bytes_recv),
                   "networs": devices}
        
        return network

    def __getGPUInfo(self):

        gpus = GPUtil.getGPUs()

        list_gpus = []

        for gpu in gpus:
            # get the GPU id
            gpu_id = gpu.id
            # name of GPU
            gpu_name = gpu.name
            # get % percentage of GPU usage of that GPU
            gpu_load = f"{gpu.load*100}%"
            # get free memory in MB format
            gpu_free_memory = f"{gpu.memoryFree} MB"
            # get used memory
            gpu_used_memory = f"{gpu.memoryUsed} MB"
            # get total memory
            gpu_total_memory = f"{gpu.memoryTotal} MB"
            # get GPU temperature in Celsius
            gpu_temperature = gpu.temperature
            gpu_uuid = gpu.uuid
            list_gpus.append({"id": gpu_id, 
                              "nome": gpu_name,
                              "load": gpu_load,
                              "free": gpu_free_memory, 
                              "used": gpu_used_memory,
                              "total": gpu_total_memory,
                              "temperature": gpu_temperature,
                              "uuid": gpu_uuid
                            })

        return list_gpus
        
    def getSystemInfo(self):

        return json.dumps(self.__system, indent = 4)

if __name__ == "__main__":

    s = SystemInformation()

    print(s.getSystemInfo())