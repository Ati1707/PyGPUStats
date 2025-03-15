import subprocess
import re


class GPUStats:
    """
    A class to retrieve and parse GPU statistics for NVIDIA GPUs using nvidia-smi.
    """

    def __init__(self):
        self.nvidia_smi_path = "nvidia-smi"
        self.gpu_data = []
        self._refresh_data()

    def _refresh_data(self):
        """Internal method to refresh GPU data"""
        raw_output = self._get_raw_stats()
        if raw_output:
            self.gpu_data = self._parse_stats(raw_output)

    def _get_raw_stats(self):
        try:
            result = subprocess.run(
                [self.nvidia_smi_path], capture_output=True, text=True, check=True
            )
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error accessing GPU stats: {e}")
            return None

    def _parse_stats(self, raw_output):
        """Parse raw output into structured GPU data"""
        gpu_blocks = self._split_gpu_blocks(raw_output)
        gpus = []

        for block in gpu_blocks:
            gpu = {
                "id": self._parse_gpu_id(block),
                "name": self._parse_gpu_name(block),
                "fan_speed": self._parse_fan_speed(block),
                "temperature": self._parse_temperature(block),
                "memory_used": self._parse_memory_used(block),
                "memory_total": self._parse_memory_total(block),
                "utilization": self._parse_utilization(block),
                "power_usage": self._parse_power_usage(block),
                "power_cap": self._parse_power_cap(block),
            }
            gpu["memory_free"] = gpu["memory_total"] - gpu["memory_used"]
            gpus.append(gpu)

        return gpus

    def _split_gpu_blocks(self, raw_output):
        return re.findall(r"(\|\s+\d+.*\n\|\s+\d+%.*\|)", raw_output)

    # Parsing helper methods
    def _parse_gpu_id(self, block):
        match = re.search(r"\|\s+(\d+)\s+", block)
        return int(match.group(1)) if match else None

    def _parse_gpu_name(self, block):
        match = re.search(r"\|\s+\d+\s+(.+?)\s+WDDM", block)
        return match.group(1).strip() if match else "Unknown GPU"

    def _parse_fan_speed(self, block):
        match = re.search(r"(\d+)%\s+\d+C", block)
        return int(match.group(1)) if match else 0

    def _parse_temperature(self, block):
        match = re.search(r"\|\s+\d+%\s+(\d+)C", block)
        return int(match.group(1)) if match else 0

    def _parse_memory_used(self, block):
        match = re.search(r"(\d+)MiB\s+/\s+\d+MiB", block)
        return int(match.group(1)) if match else 0

    def _parse_memory_total(self, block):
        match = re.search(r"/\s+(\d+)MiB", block)
        return int(match.group(1)) if match else 0

    def _parse_utilization(self, block):
        match = re.search(r"MiB\s*\|\s*(\d{1,3})%", block)
        return int(match.group(1)) if match else 0

    def _parse_power_usage(self, block):
        match = re.search(r"(\d+)W\s+/\s+\d+W", block)
        return int(match.group(1)) if match else 0

    def _parse_power_cap(self, block):
        match = re.search(r"/\s+(\d+)W", block)
        return int(match.group(1)) if match else 0

    # Public interface
    def get_all_gpus(self):
        self._refresh_data()
        return self.gpu_data

    def get_first_gpu(self):
        self._refresh_data()
        return self.gpu_data[0] if self.gpu_data else None

    def get_gpus(self, count=1):
        self._refresh_data()
        return self.gpu_data[:count] if self.gpu_data else []

    def get_gpu_by_id(self, gpu_id):
        self._refresh_data()
        for gpu in self.gpu_data:
            if gpu["id"] == gpu_id:
                return gpu
        return None

    def get_clean_output(self):
        for gpu in self.get_all_gpus():
            print(f"GPU {gpu['id']}: {gpu['name']}")
            print(f"  Temperature: {gpu['temperature']}°C")
            print(f"  Memory: {gpu['memory_used']}/{gpu['memory_total']} MiB")
            print(f"  Utilization: {gpu['utilization']}%")
            print(f"  Power: {gpu['power_usage']}/{gpu['power_cap']}W")
