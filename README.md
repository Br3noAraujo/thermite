# 🔥 Thermite

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)](https://github.com/Br3noAraujo/thermite)

![Thermite Banner](https://i.imgur.com/nwsZv1C.png)

> A professional-grade secure data destruction tool that ensures your sensitive data is completely irrecoverable.

## ✨ Features

- 🔄 Multiple overwrite passes with different patterns (zeros, ones, random data)
- 🔒 File renaming to random names before deletion
- 🗑️ Metadata and timestamp removal
- ⚡ Secure file truncation and deletion
- 💻 Cross-platform compatibility (Linux, macOS, Windows)
- 🚀 Parallel processing for maximum performance

## ⚠️ Important Notice

> **Warning**: On SSDs and NVMe drives, due to wear leveling and TRIM, overwriting may not be effective in ensuring data irrecoverability.

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/Br3noAraujo/thermite.git

# Enter the directory
cd thermite

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

```bash
# Basic secure deletion
thermite file.txt

# 5 overwrite passes
thermite -p 5 file.txt
```

## ⚙️ Options

- `-p, --passes N` - Number of overwrite passes (default: 3, recommended: 3-7)
- `-h, --help` - Show detailed help message

## 📝 Technical Limitations

- 💾 On SSDs and NVMe, due to wear leveling and TRIM, overwriting may not be effective
- 📋 Some file systems may maintain logs or journals that preserve metadata
- 🔄 Modern file systems may implement copy-on-write that preserves previous versions

## ⚖️ Disclaimer

> This software is provided "as is", without warranty of any kind.
> Use of this software is entirely at your own risk.
> The author is not responsible for any damage or consequences resulting from the use of this software.

## 👨‍💻 Author

**Br3noAraujo** - [GitHub Profile](https://github.com/Br3noAraujo)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 