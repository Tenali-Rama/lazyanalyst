from . import analyze as analyze_module
from .analyze import analyze, LazyAnalystResult

# For backward compatibility with tests: from lazyanalyst import analyze; analyze.analyze()
analyze = analyze_module
