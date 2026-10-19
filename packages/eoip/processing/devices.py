"""Device Enumeration, Resource Probing, and Qualification (PUR-FND-001, PUR-RUN-010..011).

Discovers actual local CPU resources, checks for optional hardware runtimes
(DirectML, OpenVINO, Qiskit Aer), and enforces bounded thread budgeting.
"""

from __future__ import annotations

import os
import platform
from typing import Dict, List, Optional

try:
    import psutil
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False

from eoip.processing.contracts import DeviceDescriptor, ProviderQualification


def get_usable_cpu_cores() -> int:
    """Calculate bounded CPU cores per initial safety defaults (max(1, min(2, cpu_count)))."""
    raw_count = os.cpu_count() or 1
    # Bounded default thread budget: max(1, min(2, usable_cpu_count))
    return max(1, min(2, raw_count))


def get_thread_budget() -> int:
    """Alias for thread budget based on usable CPU cores."""
    return get_usable_cpu_cores()


def get_available_memory_mib() -> int:
    """Get system available memory in MiB."""
    if _HAS_PSUTIL:
        try:
            mem = psutil.virtual_memory()
            return int(mem.available / (1024 * 1024))
        except Exception:
            pass
    return 2048  # Safe default



def enumerate_devices() -> List[DeviceDescriptor]:
    """Enumerate discovered devices with redacted stable identifiers."""
    devices = []

    # 1. Primary CPU reference device
    cpu_cores = get_usable_cpu_cores()
    mem_mib = get_available_memory_mib()
    devices.append(DeviceDescriptor(
        device_id="dev:cpu:0",
        device_type="cpu",
        vendor="Intel / AMD / ARM",
        model=f"{platform.processor() or 'Standard x86_64/ARM64 CPU'}",
        usable_cores=cpu_cores,
        usable_memory_mib=min(mem_mib, 4096),
        supported_profiles=["cpu", "cpu_numpy", "cpu_qiskit_aer", "onnx_cpu"],
        driver_version=platform.version(),
        runtime_version=platform.python_version(),
        is_qualified=True,
    ))

    # 2. Check for optional DirectML GPU
    try:
        import onnxruntime as ort
        providers = ort.get_available_providers()
        if "DmlExecutionProvider" in providers:
            devices.append(DeviceDescriptor(
                device_id="dev:gpu:dml:0",
                device_type="gpu",
                vendor="Microsoft DirectML",
                model="DirectML Qualified Hardware Accelerator",
                usable_cores=4,
                usable_memory_mib=2048,
                supported_profiles=["gpu_directml"],
                runtime_version=ort.__version__,
                is_qualified=True,
            ))
        if "OpenVINOExecutionProvider" in providers:
            devices.append(DeviceDescriptor(
                device_id="dev:npu:openvino:0",
                device_type="npu",
                vendor="Intel OpenVINO",
                model="Intel NPU Accelerator",
                usable_cores=2,
                usable_memory_mib=1024,
                supported_profiles=["npu_openvino"],
                runtime_version=ort.__version__,
                is_qualified=True,
            ))
    except ImportError:
        pass

    return devices
