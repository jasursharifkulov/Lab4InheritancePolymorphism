# Intentionally invalid: mypy must reject this target. Not a working solution.
from task06 import export_report
export_report([[1, 'Ali']], object())
