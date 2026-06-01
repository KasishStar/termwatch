# TermWatch

TermWatch is a high-density terminal system dashboard built with Textual.

It combines a fastfetch-style system overview with live telemetry widgets for CPU, memory, network, and battery monitoring.

## Features

* Real-time CPU monitoring
* Real-time memory monitoring
* Network statistics
* Battery information
* Arch Linux friendly
* Built with Textual
* Lightweight terminal interface

## Installation

### Arch Linux (AUR)
Use your favourite AUR helper
```bash
yay -S termwatch
```

### From source

```bash
git clone https://github.com/KasishStar/termwatch.git
cd termwatch
pip install .
```

### Run

```bash
termwatch
```

## Dependencies

* Python 3.10+
* textual
* psutil

## License

MIT
