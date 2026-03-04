# Shelfshift Getting Started

## Install

### [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
uv add shelfshift
uv sync
```

### [pip](https://pip.pypa.io/en/stable/installation/)

```bash
pip install shelfshift
```

## Convert a CSV in one line

```python
from shelfshift import convert_csv

csv_bytes, report = convert_csv(
    "./source.csv",
    target="shopify",
)
```

---

Previous: [Core Library Guide Index](./INDEX.md) | Next: [Core Concepts](./CORE_CONCEPTS.md)
