#!/usr/bin/env python3
"""
System Information Collector Utility

This script collects and displays detailed system information including CPU,
memory, disk, and network statistics. It supports multiple output formats and
handles unavailable metrics gracefully.

Author: Zulqurnain Haider
Email: zulqurnainjj@gmail.com
"""

import psutil
import platform
import json
import argparse
from datetime import datetime
from pathlib import Path

def get_cpu_freq():
    """
    Safely get CPU frequency information.
    
    Returns:
        dict: CPU frequency information with the following keys:
            - current: Current frequency in MHz
            - min: Minimum frequency in MHz
            - max: Maximum frequency in MHz
            - error: Error message if frequency info is unavailable
    
    Example:
        >>> get_cpu_freq()
        {
            'current': 2500.0,
            'min': 2200.0,
            'max': 3500.0
        }
    """
    try:
        freq = psutil.cpu_freq()
        if freq is None:
            return {
                "current": None,
                "min": None,
                "max": None,
                "error": "CPU frequency information not available"
            }
        return {
            "current": freq.current,
            "min": freq.min,
            "max": freq.max
        }
    except Exception as e:
        return {
            "current": None,
            "min": None,
            "max": None,
            "error": str(e)
        }

def get_system_info():
    """
    Collect comprehensive system information.
    
    Returns:
        dict: System information including:
            - system: OS and hardware information
            - cpu: CPU statistics and usage
            - memory: RAM usage statistics
            - disk: Partition information and usage
            - network: Interface and I/O statistics
    
    Example:
        >>> info = get_system_info()
        >>> print(f"OS: {info['system']['os']}")
        OS: Darwin
        >>> print(f"CPU Cores: {info['cpu']['total_cores']}")
        CPU Cores: 8
    """
    info = {
        "system": {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": platform.node()
        },
        "cpu": {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "cpu_freq": get_cpu_freq(),
            "cpu_usage_per_core": [x for x in psutil.cpu_percent(percpu=True)],
            "total_cpu_usage": psutil.cpu_percent()
        },
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "used": psutil.virtual_memory().used,
            "percentage": psutil.virtual_memory().percent
        },
        "disk": {
            "partitions": [],
            "disk_usage": {}
        },
        "network": {
            "interfaces": list(psutil.net_if_addrs().keys()),
            "io_counters": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            }
        },
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Get disk information
    for partition in psutil.disk_partitions():
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            info["disk"]["partitions"].append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": partition_usage.total,
                "used": partition_usage.used,
                "free": partition_usage.free,
                "percentage": partition_usage.percent
            })
        except Exception as e:
            info["disk"]["partitions"].append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "error": str(e)
            })
    
    return info

def format_bytes(bytes):
    """
    Format bytes to human readable format.
    
    Args:
        bytes (int): Number of bytes to format
    
    Returns:
        str: Formatted string with appropriate unit
    
    Example:
        >>> format_bytes(1024)
        '1.00 KB'
        >>> format_bytes(1048576)
        '1.00 MB'
    """
    if bytes is None:
        return "N/A"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024

def format_freq(freq):
    """
    Format CPU frequency.
    
    Args:
        freq (float): CPU frequency in MHz
    
    Returns:
        str: Formatted frequency string
    
    Example:
        >>> format_freq(2500.0)
        '2500.00 MHz'
        >>> format_freq(None)
        'N/A'
    """
    if freq is None:
        return "N/A"
    return f"{freq:.2f} MHz"

def display_info(info, format_type="text"):
    """
    Display system information in specified format.
    
    Args:
        info (dict): System information dictionary
        format_type (str): Output format ('text' or 'json')
    """
    if format_type == "json":
        print(json.dumps(info, indent=4))
        return
    
    # Text format
    print("\n=== System Information ===")
    print(f"OS: {info['system']['os']} {info['system']['os_version']}")
    print(f"Architecture: {info['system']['architecture']}")
    print(f"Processor: {info['system']['processor']}")
    print(f"Hostname: {info['system']['hostname']}")
    
    print("\n=== CPU Information ===")
    print(f"Physical cores: {info['cpu']['physical_cores']}")
    print(f"Total cores: {info['cpu']['total_cores']}")
    
    cpu_freq = info['cpu']['cpu_freq']
    if 'error' in cpu_freq:
        print(f"CPU Frequency: {cpu_freq['error']}")
    else:
        print(f"CPU Frequency:")
        print(f"  Current: {format_freq(cpu_freq['current'])}")
        print(f"  Min: {format_freq(cpu_freq['min'])}")
        print(f"  Max: {format_freq(cpu_freq['max'])}")
    
    print(f"CPU Usage: {info['cpu']['total_cpu_usage']}%")
    
    print("\n=== Memory Information ===")
    print(f"Total: {format_bytes(info['memory']['total'])}")
    print(f"Available: {format_bytes(info['memory']['available'])}")
    print(f"Used: {format_bytes(info['memory']['used'])} ({info['memory']['percentage']}%)")
    
    print("\n=== Disk Information ===")
    for partition in info['disk']['partitions']:
        print(f"\nDevice: {partition['device']}")
        print(f"Mountpoint: {partition['mountpoint']}")
        print(f"File System: {partition['fstype']}")
        if 'error' in partition:
            print(f"Error: {partition['error']}")
        else:
            print(f"Total: {format_bytes(partition['total'])}")
            print(f"Used: {format_bytes(partition['used'])} ({partition['percentage']}%)")
            print(f"Free: {format_bytes(partition['free'])}")
    
    print("\n=== Network Information ===")
    print(f"Interfaces: {', '.join(info['network']['interfaces'])}")
    print(f"Bytes sent: {format_bytes(info['network']['io_counters']['bytes_sent'])}")
    print(f"Bytes received: {format_bytes(info['network']['io_counters']['bytes_recv'])}")

def main():
    """
    Main function to handle command-line arguments and execute system information collection.
    
    The script accepts the following arguments:
    1. --format: Output format (text or json)
    2. --output: Optional output file path
    
    Returns:
        bool: True if operation was successful, False otherwise
    """
    parser = argparse.ArgumentParser(
        description="Display system information",
        epilog="For issues or suggestions, contact: zulqurnainjj@gmail.com"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (optional)"
    )
    
    args = parser.parse_args()
    
    try:
        # Collect system information
        info = get_system_info()
        
        # Create output directory if needed
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Display or save information
        if args.output:
            with open(args.output, 'w') as f:
                if args.format == "json":
                    json.dump(info, f, indent=4)
                else:
                    # Redirect stdout to file
                    import sys
                    original_stdout = sys.stdout
                    sys.stdout = f
                    display_info(info, args.format)
                    sys.stdout = original_stdout
            print(f"System information saved to: {args.output}")
        else:
            display_info(info, args.format)
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1) 