import cProfile
import pstats
import os
from typing import Any, Callable, Optional, List


class Profiler:
    def __init__(self, exclude_modules: Optional[List[str]] = None) -> None:
        self.profiler = cProfile.Profile()
        self.exclude_modules = exclude_modules or []
        # Ensure the profiler's module itself is excluded.
        self.exclude_modules.append('profiler')

    def enable(self) -> None:
        self.profiler.enable()

    def disable(self) -> None:
        self.profiler.disable()

    def runcall(self, func: Callable[..., Any]) -> Any:
        # Wrap the function call with the profiler.
        return self.profiler.runcall(func)

    def write_profiling_stats_to_file(self, file_path: str, app_root: str) -> None:
        stats = pstats.Stats(self.profiler)
        stats.dump_stats(file_path)  # Dumping the stats for potential external use.
        
        # Normalize the app_root path to use consistent separators
        app_root = os.path.normpath(app_root)

        with open(file_path, "w") as f:
            # Organize by number of calls
            f.write("Organized by number of calls:\n\n")
            self._write_stats_section(f, stats, 'ncalls', app_root)
            f.write("\n\n")
            # Organize by total time
            f.write("Organized by total time:\n\n")
            self._write_stats_section(f, stats, 'tottime', app_root)

    def _write_stats_section(self, file, stats, sort_by: str, app_root: str) -> None:
        # Sort the statistics by the specified sort key
        stats.sort_stats(sort_by)
        
        # Prepare the header for the output
        header = "{:>10} {:>15} {:>15} {:>20} {:>20} Function\n".format(
            "Calls", "Total Time", "Per Call", "Cumulative Time", "Per Call (Cum)"
        )
        file.write(header)
        file.write("-" * 85 + "\n")

        for func, func_stats in stats.stats.items():
            # Only include functions from our application
            if app_root in os.path.normpath(func[0]):
                total_calls, _, total_time, cumulative_time, _ = func_stats
                # If the function is part of the main loop, count it as one call.
                # This heuristic assumes that each main loop function is wrapped exactly once.
                if total_calls > 1 and '__main__' in func[0]:
                    total_calls = 1
                per_call_time = total_time / total_calls
                per_call_cumulative = cumulative_time / total_calls
                # Format the output string
                output = "{:>10} {:>15.6f} {:>15.6f} {:>20.6f} {:>20.6f} {}\n".format(
                    total_calls, total_time, per_call_time, cumulative_time, per_call_cumulative, 
                    f"{os.path.basename(func[0])}:{func[1]}({func[2]})"
                )
                file.write(output)
