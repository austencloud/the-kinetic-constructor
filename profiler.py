import cProfile
import pstats
import os
from typing import Any, Callable


class Profiler:
    def __init__(self, exclude_modules=None) -> None:
        self.profiler = cProfile.Profile()
        self.exclude_modules = exclude_modules or ["PyQt6"]

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
                result = func(*args, **kwargs)
                self.disable()
            else:
                result = func(*args, **kwargs)
            return result

        return inner

    def write_profiling_stats_to_file(self, file_path: str, app_root: str) -> None:
        stats = pstats.Stats(self.profiler)
        stats.sort_stats("calls")

        # Normalize app_root to use forward slashes
        app_root = app_root.replace('\\', '/')

        with open(file_path, "w") as f:
            f.write(
                f"{'Calls':>10} {'Total Time':>15} {'Per Call':>15} {'Cumulative Time':>20} {'Per Call (Cum)':>20} Function\n"
            )
            f.write("-" * 85 + "\n")

            stats_list = [
                (nc, tt, tt / nc if nc else 0, ct, ct / cc if cc else 0, func)
                for func, (cc, nc, tt, ct, callers) in stats.stats.items()
            ]

            stats_list.sort(key=lambda x: x[0], reverse=True)  # Sorting by number of calls

            for nc, tt, percall_tt, ct, percall_ct, func in stats_list:
                file_name, line_number, func_name = func
                f.write(
                    f"{nc:>10} {tt:15.6f} {percall_tt:15.6f} {ct:20.6f} {percall_ct:20.6f} {file_name}:{line_number}({func_name})\n"
                )
