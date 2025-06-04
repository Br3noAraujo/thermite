#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Thermite - Secure Data Destruction Tool
======================================

DISCLAIMER:
This software is provided "as is", without warranty of any kind.
Use of this software is entirely at your own risk.
The author is not responsible for any damage or consequences resulting from the use of this software.

TECHNICAL LIMITATIONS:
- On SSDs and NVMe, due to wear leveling and TRIM, overwriting may not be effective
- Some file systems may maintain logs or journals that preserve metadata
- Modern file systems may implement copy-on-write that preserves previous versions

Author: Br3noAraujo
License: MIT
"""

import os
import random
import secrets
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Tuple
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Custom colors for Thermite theme
class ThermiteColors:
    FIRE = Fore.RED + Style.BRIGHT
    EMBER = Fore.YELLOW + Style.BRIGHT
    ASH = Fore.WHITE + Style.DIM
    HOT = Fore.RED
    WARM = Fore.YELLOW
    COOL = Fore.WHITE
    BURN = Back.RED + Fore.WHITE + Style.BRIGHT
    MELT = Back.YELLOW + Fore.BLACK + Style.BRIGHT


def create_gradient_text(text: str, start_color: str, end_color: str) -> str:
    """Creates a horizontal gradient effect for text."""
    result = ""
    length = len(text)
    for i, char in enumerate(text):
        factor = i / (length - 1) if length > 1 else 0
        # Interpolate between start and end colors (simple two-color step)
        color = start_color if factor < 0.5 else end_color
        result += f"{color}{char}"
    return result + Style.RESET_ALL


banner = f"""
{ThermiteColors.FIRE}┏┳┓┓┏┏┓┳┓┳┳┓┳┏┳┓┏┓
{ThermiteColors.EMBER} ┃ ┣┫┣ ┣┫┃┃┃┃ ┃ ┣ 
{ThermiteColors.FIRE} ┻ ┛┗┗┛┛┗┛ ┗┻ ┻ ┗┛{Style.BRIGHT} by {create_gradient_text('Br3noAraujo', ThermiteColors.FIRE, ThermiteColors.EMBER)}{Style.RESET_ALL}
{ThermiteColors.EMBER}  [ Secure Data Destruction Tool ]{Style.RESET_ALL}
"""


class Thermite:
    def __init__(self, passes: int = 3):
        self.passes = passes
        self.buffer_size = 1024 * 1024
        self.patterns = [
            bytes([0x00] * self.buffer_size),  # Zeros
            bytes([0xFF] * self.buffer_size),  # Ones
            bytes([0x55] * self.buffer_size),  # Alternating pattern 0101
            bytes([0xAA] * self.buffer_size),  # Alternating pattern 1010
        ]

    def _generate_random_name(self) -> str:
        return secrets.token_hex(16)

    def _overwrite_chunk(self, args: Tuple[Path, bytes, int, int]) -> None:
        file_path, pattern, start, size = args
        with open(file_path, 'r+b') as f:
            f.seek(start)
            f.write(pattern[:size])

    def _overwrite_file(self, file_path: Path) -> None:
        file_size = file_path.stat().st_size
        num_threads = min(os.cpu_count() or 1, 8)
        chunk_size = max(self.buffer_size, file_size // (num_threads * 2) or 1)
        for pass_num in range(self.passes):
            progress = f"{ThermiteColors.FIRE}Pass {pass_num + 1}/{self.passes}{Style.RESET_ALL}"
            print(f"\r{progress}", end="", flush=True)
            # Gera padrão aleatório novo a cada passagem
            random_pattern = bytes([random.randint(0, 255) for _ in range(self.buffer_size)])
            for pattern in self.patterns + [random_pattern]:
                # Generator para chunks
                def chunk_args():
                    for start in range(0, file_size, chunk_size):
                        size = min(chunk_size, file_size - start)
                        yield (file_path, pattern, start, size)
                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    list(executor.map(self._overwrite_chunk, chunk_args()))

    def _wipe_metadata(self, file_path: Path) -> None:
        try:
            os.chmod(file_path, 0o000)
            os.utime(file_path, (0, 0))
            if os.name != 'nt':
                os.system(f'chattr -i "{file_path}" 2>/dev/null')
        except Exception as e:
            print(f"{ThermiteColors.EMBER}Warning: Could not remove all metadata: {e}{Style.RESET_ALL}")

    def secure_delete(self, target_path: str) -> None:
        path = Path(target_path)
        if not path.exists():
            print(f"{ThermiteColors.FIRE}Error: File not found: {target_path}{Style.RESET_ALL}")
            return
        print(f"\n{ThermiteColors.FIRE}Starting secure deletion of: {ThermiteColors.COOL}{target_path}{Style.RESET_ALL}")
        print(f"{ThermiteColors.EMBER}File size: {ThermiteColors.COOL}{path.stat().st_size / (1024*1024):.2f} MB{Style.RESET_ALL}")
        print(f"{ThermiteColors.EMBER}Number of passes: {ThermiteColors.COOL}{self.passes}{Style.RESET_ALL}")
        print(f"{ThermiteColors.EMBER}Using {ThermiteColors.COOL}{min(os.cpu_count() or 1, 8)}{ThermiteColors.EMBER} threads for maximum performance{Style.RESET_ALL}")
        print(f"\n{ThermiteColors.FIRE}Progress:{Style.RESET_ALL}")
        try:
            self._overwrite_file(path)
            print()
            temp_name = self._generate_random_name()
            temp_path = path.parent / temp_name
            path.rename(temp_path)
            self._wipe_metadata(temp_path)
            temp_path.unlink()
            print(f"\n{ThermiteColors.FIRE}Secure deletion completed successfully!{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{ThermiteColors.FIRE}Error during secure deletion: {e}{Style.RESET_ALL}")

def main():
    simple_parser = argparse.ArgumentParser(
        description=f"{ThermiteColors.FIRE}Thermite - Secure Data Destruction Tool{Style.RESET_ALL}",
        add_help=False
    )
    simple_parser.add_argument(
        "target",
        nargs="?",
        help="Path to the file to be securely deleted"
    )
    simple_parser.add_argument(
        "-p", "--passes",
        type=int,
        default=3,
        help="Number of overwrite passes (default: 3)"
    )
    simple_parser.add_argument(
        "-h", "--help",
        action="store_true",
        help="Show detailed help message"
    )
    detailed_parser = argparse.ArgumentParser(
        description=f"""
{ThermiteColors.FIRE}Thermite - Secure Data Destruction Tool{Style.RESET_ALL}

A professional-grade secure file deletion tool that implements multiple security measures
to ensure data is irrecoverable. The tool performs multiple overwrites with different
patterns, removes metadata, and securely deletes files.

{ThermiteColors.EMBER}Security Features:{Style.RESET_ALL}
- Multiple overwrite passes with different patterns (zeros, ones, random data)
- File renaming to random names before deletion
- Metadata and timestamp removal
- Secure file truncation and deletion
- Cross-platform compatibility (Linux, macOS, Windows)
- Parallel processing for maximum performance

{ThermiteColors.EMBER}Note:{Style.RESET_ALL} On SSDs and NVMe drives, due to wear leveling and TRIM, overwriting may not be
effective in ensuring data irrecoverability.

{ThermiteColors.FIRE}Quick Usage Examples:{Style.RESET_ALL}
  thermite file.txt              # Basic secure deletion
  thermite -p 5 file.txt         # 5 overwrite passes
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    detailed_parser.add_argument(
        "target",
        nargs="?",
        help="Path to the file to be securely deleted"
    )
    detailed_parser.add_argument(
        "-p", "--passes",
        type=int,
        default=3,
        help="Number of overwrite passes (default: 3, recommended: 3-7)"
    )
    print(banner)
    args = simple_parser.parse_args()
    if args.help:
        detailed_parser.print_help()
        return
    if not args.target:
        print(f"{ThermiteColors.FIRE}Usage: thermite [options] <file>{Style.RESET_ALL}")
        print(f"\n{ThermiteColors.EMBER}Options:{Style.RESET_ALL}")
        print(f"  {ThermiteColors.WARM}-p, --passes N{Style.RESET_ALL}    Number of overwrite passes (default: 3)")
        print(f"  {ThermiteColors.WARM}-h, --help{Style.RESET_ALL}        Show detailed help message")
        return
    print(f"\n{ThermiteColors.FIRE}IMPORTANT WARNING:{Style.RESET_ALL}")
    print(f"{ThermiteColors.EMBER}On SSDs and NVMe, due to wear leveling and TRIM,")
    print("overwriting may not be effective in ensuring")
    print(f"data irrecoverability.{Style.RESET_ALL}\n")
    thermite = Thermite(passes=args.passes)
    thermite.secure_delete(args.target)

if __name__ == "__main__":
    main()


