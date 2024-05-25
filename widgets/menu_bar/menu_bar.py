from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenuBar
from Enums.PropTypes import PropType
from PyQt6.QtGui import QAction, QActionGroup

if TYPE_CHECKING:
    from ..main_widget.main_widget import MainWidget


class MainWindowMenuBar(QMenuBar):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self.glyph_visibility_manager = (
            self.main_widget.main_window.settings_manager.glyph_visibility_manager
        )
        self.grid_visibility_manager = (
            self.main_widget.main_window.settings_manager.grid_visibility_manager
        )

        self._setup_menu()
        self._setup_settings_menu()
        self._setup_visibility_menu()
        self._setup_prop_type_menu()
        self._setup_backgrounds_menu()

    def _setup_backgrounds_menu(self):
        backgrounds_menu = self.addMenu("Backgrounds")
        background_action_group = QActionGroup(self)
        background_action_group.setExclusive(True)

        # List of background managers available
        background_types = [
            "Rainbow",
            "Starfield",
            "Particle",
            "Aurora",
            "AttractionParticles",
            "AuroraBorealis",
            "WaterRipples",
        ]
        current_bg = self.main_widget.main_window.settings_manager.get_setting(
            "background_type", default="Rainbow"
        )

        for bg_type in background_types:
            action = QAction(bg_type, self, checkable=True)
            action.setChecked(current_bg == bg_type)
            action.triggered.connect(
                lambda checked, bg=bg_type: (
                    self.set_background_type(bg) if checked else None
                )
            )
            backgrounds_menu.addAction(action)
            background_action_group.addAction(action)

    def set_background_type(self, bg_type: str):
        self.main_widget.main_window.settings_manager.set_setting(
            "background_type", bg_type
        )
        self.main_widget.apply_background(bg_type)

    def _setup_prop_type_menu(self):
        prop_type_menu = self.addMenu("Prop Type")
        prop_type_action_group = QActionGroup(self)
        prop_type_action_group.setExclusive(True)

        for prop_type in PropType:
            action = QAction(prop_type.name, self, checkable=True)
            action.triggered.connect(
                lambda checked, pt=prop_type: self.set_prop_type(pt)
            )
            prop_type_menu.addAction(action)
            prop_type_action_group.addAction(action)

            if self.main_widget.prop_type == prop_type:
                action.setChecked(True)

    def _setup_settings_menu(self):
        settings_menu = self.addMenu("Settings")
        preferences_action = QAction("Preferences", self)
        preferences_action.triggered.connect(self.open_preferences_dialog)
        settings_menu.addAction(preferences_action)

    def _setup_visibility_menu(self):
        visibility_menu = self.addMenu("Visibility")

        # Glyph visibility toggles
        for glyph_type in ["VTG", "TKA", "Elemental", "EndPosition"]:
            action = QAction(f"{glyph_type} Glyph", self, checkable=True)
            action.setChecked(
                self.glyph_visibility_manager.get_glyph_visibility(glyph_type)
            )
            action.triggered.connect(
                lambda checked, gt=glyph_type: self.toggle_glyph_visibility(gt, checked)
            )
            visibility_menu.addAction(action)

        non_radial_action = QAction("Non-Radial Points", self, checkable=True)
        non_radial_action.setChecked(
            self.main_widget.main_window.settings_manager.grid_visibility_manager.non_radial_visible
        )
        non_radial_action.triggered.connect(
            self.grid_visibility_manager.toggle_visibility
        )
        visibility_menu.addAction(non_radial_action)

    def toggle_glyph_visibility(self, glyph_type: str, visible: bool):
        self.glyph_visibility_manager = self.glyph_visibility_manager
        self.glyph_visibility_manager.set_glyph_visibility(glyph_type, visible)
        self.glyph_visibility_manager.apply_glyph_visibility()

    def set_prop_type(self, prop_type: PropType):
        self.main_widget.prop_type_selector.on_prop_type_changed(prop_type.name)
        print(f"Prop type set to: {prop_type.name}")

    def open_preferences_dialog(self):
        self.preferences_dialog = self.main_widget.layout_options_dialog
        self.preferences_dialog.load_initial_settings()
        self.preferences_dialog.exec()

    def _setup_menu(self):
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)


# I'm going to make a list of all the things I want to make better about my program currently, and I want you to turn that rambling into a coherent and easily structured set of Things that I need to do.

# We need to make it so the drop down, which selects the amount of beats that are in a given sequence is more intuitive and pretty to look at and user friendly. Maybe there can be some sort of options panel with three lines as an icon to indicate that the user can change the dynamics of the specific sequence they're working with right now. We also need to make it so that the user can see their sequence growing gradually As they add individual pictographs, Instead of having the beat frame be sixteen pictographs by default.

# We need to incorporate the rest of the circular word Checker that uses the logic to develop the rest of the word once we've already made the first rotation of it The first version of this will just be a rotational permutation creator. This needs to have a magic wand icon that lives with the rest of the icons and the builder tab.

# The image export dialog needs to be a lot more intuitive and user friendly. We need to make it so we fix the add start position option so that it properly Creates an image with a start position and updates the thumbnail. And we also need to make it so That we have a pretty layout for all of the information that the user can add to the pictograph sequence. And also, we want to make it so that it automatically puts that information, including the user's initials. And the date into the sequence that's being exported. Inside this image export dialog, the user should have the option to change their visibility for the image they're going to be exporting. We should reuse the visibility manager to do this.

# Inside the dictionary tab, we need to make it so that the Numbers and letters that are displayed on the left panel actually caused the user to snap to their desired location inside the scroll area. We also need to fix the bug which is causing it to expand the programs height indefinitely because there's so many letters in the alphabet that it needs to include. We need to have a better system than that. Maybe we can just make the letters smaller And that should fix it. We also need to redesign the sorter so that it's also an options panel. There's many elements of functionality we want to add to the sorter. For instance, we want to sort out sequences that have reversals.

# We need to implement a whole system of analyzing a sequence to determine whether or not it has prop reversals, FULL REVERSALS, OR HAND REVERSALS. This information can be stored within the sequences json data. Then when we're sorting our sequences within the dictionary tab, we can simply access that data and filter out only the options which have the desired reversals inside them. Either that or we can implement a system of analyzing each given sequence to determine whether or not it does have reversals. I think it would make more sense to store this data ahead of time as a boolean value, because it would probably be less workload and reduce the overhead computationally.

# We also want to redesign the dictionary sorter tab to be intuitive and easy to Comprehend. Maybe we could start with a open up dialog, and then we could try to work towards increasing the accessibility by making it live within a widget that is right above the scroll area.

# Also, right now, all of my thumbnails that I've exported are super high res. And it's causing my program to be rather slow. I think I can cut the size of the pictographs by like a 3rd and it would probably be just fine. Perhaps I can explore displaying these pictographs as svgs, rather than image files. Maybe that would Solve this problem if every single collection of pictographs is Its own svg, then we could access that svg data rather than having to create new graphics views repeatedly.

# There's a minor error right now where when I change the visibility of the non radial points, it doesn't impact the start position in the beat frame. We need to add the logic to also change the beat frame's Visibility as soon as we make that change.

# Inside the dictionary right now, we're just showing variation 1 or variation 2 for the different variations, and I'd like to give the user the ability to give specific names to their variations. it would be cool if when they click the variation it switches between these custom name that the user has given them and the variation number for indexing.

# I think it would be great if there was an automatic way for the program to fix words such that there is a standardized form of a circular word. The standard form should take whatever letter comes earliest in the alphabet and put it at the beginning of the sequence. This would involve making it clear to the user that their word has been automatically modified to follow this standardized naming convention.

# It would be really nice if inside the dictionary tab there's a way to select your favorites and then a way to immediately access all that you've starred. I'm thinking in the preview area There could be a star button which allows you to favorite that specific variation of that specific word so that it shows up in the favorites panel. We also need to make it so It properly puts things in alphabetical order according to the way I've set them up in the kinetic alphabet. It should take into account the dashes, and it should take into account alphabetical gamma being the type six letters. And this specific order of the type 2 and 3 and 4 and five letters.

# It would be great if the user had the ability to modify the way that all the pictographs look within their thumbnails in the dictionary tab. I want to create a way for the program to automatically save all variations of a Specific sequence in all prop types as images (or svg's more preferably). It should have a dynamic system for saving these within subfolders that should allow it to easily access the new vgs when the user changes the prop type of the overall program. Right now my program is using image thumbnails to display in the dictionary tab. But I think if they were to use these svg files and have them sorted in a really easy to access way, then we could make it more efficient. Also, I believe it will take up a lot of storage space. To develop an image for every single prop type As soon as the user wants to save a sequence. I'm thinking if this is all stored in textual data, then it could be more efficient. But I'm really not sure. I don't know if there are benefits or drawbacks to changing everything to be svgs. Maybe it would work just to have a smaller image file. I'm wondering if in order to use SVG I'm going to need to create new graphics views for every single instance a displaying the humbnail in the dictionary. My program is currently set up to assemble all of these different components using a queue graphic scene and a set of rules that it's given from a dictionary file. However, in this new setup that I'm suggesting, I'm suggesting once we assemble a pictograph We save it as svg data. And the program should know whether it should look for the existing svg data or assemble a pictograph to create it. Then it should display this svg data, basically in the exact same way it displays an image. And I'm wondering if I'm able to do that without creating a queue graphics view and a scene to make it So that it has to create an entire instance of that class every single time it needs to set one up. I want the image that is exported from the image export manager to actually be an SVG itself that it just loads as an image from the text data. Is that feasible or is that Going to cause more issues in terms of functionality because of having to set up a coordinate system for every single image?


# write me the bullet point list

# - Make the drop down for selecting the amount of beats in a sequence more intuitive and user friendly
# - Make it so the user can see their sequence growing gradually as they add individual pictographs
# - Incorporate the circular word checker to develop the rest of the word once the first rotation is made
# - Redesign the image export dialog to be more intuitive and user friendly
# - Fix the add start position option to properly create an image with a start position and update the thumbnail
# - Redesign the dictionary tab to be more intuitive and user friendly
# - Implement a system of analyzing a sequence to determine whether or not it has prop reversals, full reversals, or hand reversals
# - Redesign the dictionary sorter tab to be more intuitive and user friendly
# - Fix the bug causing the dictionary tab to expand the programs height indefinitely
# - Reduce the size of the pictographs to improve program performance
# - Implement a system of automatically fixing words to follow a standardized naming convention
# - Implement a system of allowing the user to give specific names to their variations
# - Implement a system of allowing the user to select their favorites and access them easily
# - Implement a system of allowing the user to modify the way pictographs look within their thumbnails
# - Implement a system of automatically saving all variations of a specific sequence in all prop types as images or svgs
