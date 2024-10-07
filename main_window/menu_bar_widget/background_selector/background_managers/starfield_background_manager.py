import random
from main_window.menu_bar_widget.background_selector.background_managers.background_manager import (
    BackgroundManager,
)
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

class StarfieldBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stars = [
            (
                random.random(),
                random.random(),
                random.random() * 2 + 1,
                random.choice([QColor(255, 255, 255), QColor(255, 255, 0)]),
            )
            for _ in range(100)
        ]
        self.twinkle_state = [
            random.uniform(0.8, 1.0) for _ in range(100)
        ]  # Subtle twinkle

        # Initialize comet variables
        self.comet_active = False
        self.comet = {
            "x": 0,
            "y": 0,
            "size": 15,
            "dx": 0,
            "dy": 0,
            "speed": 0.005,
            "tail": [],
        }
        self.comet_timer = 10  # More frequent comet appearance

    def animate_background(self):
        # Update stars
        self.stars = [
            (x, y, z - 0.02, color) for x, y, z, color in self.stars if z > 0.1
        ]
        if len(self.stars) < 100:
            self.stars.append(
                (
                    random.random(),
                    random.random(),
                    2,
                    random.choice([QColor(255, 255, 255), QColor(255, 255, 0)]),
                )
            )
        self.twinkle_state = [random.uniform(0.8, 1.0) for _ in range(len(self.stars))]

        # Handle comet appearance and movement
        if self.comet_active:
            self.move_comet()
        else:
            self.comet_timer -= 1
            if self.comet_timer <= 0:
                self.activate_comet()

        self.update_required.emit()

    def activate_comet(self):
        """Activate the comet by setting its initial position and properties."""
        self.comet_active = True
        
        # Adjust starting position so it's closer to the visible screen
        start_position_options = [
            (random.uniform(-0.1, 0), random.uniform(0.1, 0.9)),  # Coming from the left
            (random.uniform(1.0, 1.1), random.uniform(0.1, 0.9)),  # Coming from the right
            (random.uniform(0.1, 0.9), random.uniform(-0.1, 0)),  # Coming from the top
            (random.uniform(0.1, 0.9), random.uniform(1.0, 1.1)),  # Coming from the bottom
        ]
        start_x, start_y = random.choice(start_position_options)

        # Randomly set direction and speed for diagonal movement, more controlled
        dx = random.uniform(-0.5, 0.5)  # Reduced horizontal randomness
        dy = random.uniform(-0.5, 0.5)  # Reduced vertical randomness
        normalization_factor = (dx**2 + dy**2) ** 0.5  # Normalize diagonal movement
        dx /= normalization_factor
        dy /= normalization_factor

        # Log to verify starting positions
        print(f"Comet starting at ({start_x}, {start_y}) with direction ({dx}, {dy})")

        self.comet = {
            "x": start_x,
            "y": start_y,
            "size": random.uniform(10, 20),  # Comet size
            "dx": dx,
            "dy": dy,
            "speed": random.uniform(0.003, 0.008),  # Comet speed
            "tail": [],
        }

    def move_comet(self):
        """Move the comet based on its direction and manage its tail effect."""
        comet = self.comet
        comet["x"] += comet["dx"] * comet["speed"]
        comet["y"] += comet["dy"] * comet["speed"]
        comet["tail"].append((comet["x"], comet["y"], comet["size"]))

        # Limit the tail length for a smooth trail effect
        if len(comet["tail"]) > 20:
            comet["tail"].pop(0)

        # If the comet moves out of view, deactivate it
        if (
            comet["x"] < -0.2
            or comet["x"] > 1.2
            or comet["y"] < -0.2
            or comet["y"] > 1.2
        ):
            print("Comet deactivated")  # Log to check if comet is deactivated
            self.comet_active = False
            self.comet_timer = random.randint(50, 150)  # Reduced time before the next comet

    def paint_comet(self, painter: QPainter, widget: QWidget):
        """Draw the comet and its tail on the screen."""
        if not self.comet_active:
            return

        comet = self.comet
        comet_x = int(comet["x"] * widget.width())
        comet_y = int(comet["y"] * widget.height())

        # Draw the comet tail
        painter.setPen(Qt.PenStyle.NoPen)
        for i, (tx, ty, size) in enumerate(comet["tail"]):
            opacity = (i + 1) / len(comet["tail"])  # Tail fades out
            painter.setOpacity(opacity)
            tail_x = int(tx * widget.width())
            tail_y = int(ty * widget.height())
            painter.setBrush(QColor(255, 255, 255, int(255 * opacity)))
            painter.drawEllipse(tail_x, tail_y, int(size), int(size))

        # Draw the comet itself (brighter, at the head of the tail)
        painter.setOpacity(1.0)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(comet_x, comet_y, int(comet["size"]), int(comet["size"]))

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Paint black background
        painter.fillRect(widget.rect(), QColor(0, 0, 0))

        # Paint stars
        for i, (x, y, z, color) in enumerate(self.stars):
            star_size = int((1 - z) * 5)
            xpos = int(x * widget.width())
            ypos = int(y * widget.height())
            painter.setBrush(color)
            if self.twinkle_state[i] > 0.95:  # Subtle twinkle effect
                star_size += 1
            painter.drawEllipse(xpos, ypos, star_size, star_size)

        # Paint the comet if it's active
        self.paint_comet(painter, widget)
