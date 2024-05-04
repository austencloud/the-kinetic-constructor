from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.sequence_image_export_manager import (
        SequenceImageExportManager,
    )


class ImageExportLayoutManager:
    def __init__(self, image_export_manager: "SequenceImageExportManager"):
        self.image_export_manager = image_export_manager
        self.beat_frame = image_export_manager.beat_frame

    @property
    def include_start_pos(self):
        # Dynamically fetch the current setting from the export manager
        return self.image_export_manager.include_start_pos

    def calculate_layout(self, filled_beat_count: int) -> tuple[int, int]:
        """
        Determine the layout by delegating to the specific method based on whether the start position is included.
        """
        if self.include_start_pos:
            return self.calculate_layout_with_start(filled_beat_count)
        else:
            return self.calculate_layout_without_start(filled_beat_count)

    def calculate_layout_with_start(self, filled_beat_count: int) -> tuple[int, int]:
        """
        Calculate layout considering an additional column for the start position.
        """
        return self.calculate_optimal_layout(
            filled_beat_count, self.get_layout_options_with_start()
        )

    def calculate_layout_without_start(self, filled_beat_count: int) -> tuple[int, int]:
        """
        Calculate layout without the start position affecting the column count.
        """
        return self.calculate_optimal_layout(
            filled_beat_count, self.get_layout_options_without_start()
        )

    def calculate_optimal_layout(
        self, beat_count: int, layout_options: dict
    ) -> tuple[int, int]:
        """
        Shared logic for calculating layout which can be customized further using provided layout options.
        """
        if beat_count in layout_options:
            return layout_options[beat_count]
        else:
            column_count = min(
                beat_count // self.beat_frame.ROW_COUNT + 1,
                self.beat_frame.COLUMN_COUNT,
            )
            row_count = min(
                (beat_count + column_count - 1) // column_count,
                self.beat_frame.ROW_COUNT,
            )
            return column_count, row_count

    def get_layout_options_with_start(self) -> dict[int, tuple[int, int]]:
        """
        Layout options when including the start position in the layout.
        """
        return {
            0: (1, 1),
            1: (2, 1),
            2: (3, 1),
            3: (4, 1),
            4: (3, 2),
            5: (4, 2),
            6: (4, 2),
            7: (5, 2),
            8: (5, 2),
            9: (4, 3),
            10: (5, 3),
            11: (5, 3),
            12: (4, 4),
            13: (5, 4),
            14: (5, 4),
            15: (5, 4),
            16: (5, 4),
        }

    def get_layout_options_without_start(self) -> dict[int, tuple[int, int]]:
        """
        Define or adjust layout options for various counts of filled beats without the start position.
        Customize this as needed if different from layouts with start position.
        """
        return {
            0: (1, 1),
            1: (1, 1),
            2: (2, 1),
            3: (3, 1),
            4: (4, 1),
            5: (3, 2),
            6: (3, 2),
            7: (4, 2),
            8: (4, 2),
            9: (3, 3),
            10: (5, 2),
            11: (4, 3),
            12: (3, 4),
            13: (4, 4),
            14: (4, 4),
            15: (4, 4),
            16: (4, 4),
        }
