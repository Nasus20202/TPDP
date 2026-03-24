# Lab 3 – PyQGIS

## Setup

Open the QGIS Python Console (**Plugins → Python Console**), then add the script to the path:

```python
import sys
sys.path.append("/path/to/lab3")
import lab3
```

## Running the tasks

```python
lab3.task1()   # world map + voivodeships + counties, zoomed to Poland
lab3.task2()   # voivodeships with area field; writes voivodeships_areas.txt
```

## Reloading after edits

```python
import importlib
importlib.reload(lab3)
```
