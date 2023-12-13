import cProfile
import pstats
import os
from typing import Any, Callable, Optional, List


class Profiler:
    def __init__(self, exclude_modules: Optional[List[str]] = None) -> None:
        self.profiler = cProfile.Profile()
        self.exclude_modules = exclude_modules or ["PyQt6", "__main__"]

    def enable(self) -> None:
        self.profiler.enable()

    def disable(self) -> None:
        self.profiler.disable()

    def runcall(self, func: Callable[..., Any]) -> Any:
        return self.profiler.runcall(self.profile_filter(func))

    def profile_filter(self, func: Callable[..., Any]) -> Callable[..., Any]:
        def inner(*args, **kwargs) -> Any:
            if func.__module__ and not any(
                mod in func.__module__ for mod in self.exclude_modules
            ):
                self.enable()
                try:
                    result = func(*args, **kwargs)
                finally:
                    self.disable()
            else:
                result = func(*args, **kwargs)
            return result

        return inner

    def write_profiling_stats_to_file(self, file_path: str, app_root: str) -> None:
        stats = pstats.Stats(self.profiler)

        # Normalize the app_root path to use consistent separators
        app_root = os.path.normpath(app_root)

        with open(file_path, "w") as f:
            f.write("Organized by number of calls:\n\n")
            self._write_stats_section(f, stats, "calls", app_root)
            f.write("\n\n")  # Separate the two sections
            f.write("Organized by total time:\n\n")
            self._write_stats_section(f, stats, "time", app_root)

    def _write_stats_section(self, file, stats, sort_by: str, app_root: str) -> None:
        stats.sort_stats(sort_by)
        header = "{:>10} {:>15} {:>15} {:>20} {:>20} Function\n".format(
            "Calls", "Total Time", "Per Call", "Cumulative Time", "Per Call (Cum)"
        )
        file.write(header)
        file.write("-" * 85 + "\n")

        path_to_remove = "f:\\CODE\\tka-app\\tka-sequence-constructor\\widgets\\"
        filtered_stats = [(func, stat_info) for func, stat_info in stats.stats.items() if app_root in os.path.normpath(func[0])]

        # Apply sorting manually
        if sort_by == "calls":
            sorted_stats = sorted(filtered_stats, key=lambda x: x[1][0], reverse=True)
        elif sort_by == "time":
            sorted_stats = sorted(filtered_stats, key=lambda x: x[1][2], reverse=True)

        for func, stat_info in sorted_stats:
            file_name, line_number, func_name = func
            file_name = os.path.normpath(file_name).replace(path_to_remove, "")
            cc, nc, tt, ct, callers = stat_info
            percall_tt = tt / nc if nc else 0
            percall_ct = ct / cc if cc else 0
            file.write(
                f"{nc:>10} {tt:15.6f} {percall_tt:15.6f} {ct:20.6f} {percall_ct:20.6f} {file_name}:{line_number}({func_name})\n"
            )