import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SMALL_DOC = """# Tiny Doc

## 1 Alpha
Alpha intro text.

### 1.1 Apples
Apples are red. Apples grow on trees.

### 1.2 Avocados
Avocados are green and creamy.

## 2 Beta
### 2.1 Bananas
#### 2.1.1 Ripe bananas
Ripe bananas are yellow with brown spots.

#### 2.1.2 Green bananas
Green bananas are firm and starchy.
"""


@pytest.fixture
def small_doc():
    return SMALL_DOC


@pytest.fixture
def handbook_path():
    return str(ROOT / "data" / "handbook.md")
