from typing import TYPE_CHECKING
from PyQt6.QtCore import QSettings, QObject, pyqtSignal
from .builder_settings import BuilderSettings
from .sequence_sharing_settings import SequenceSharingSettings
from .write_tab_settings import WriteTabSettings
from .dictionary_settings import DictionarySettings
from .image_export_settings import ImageExportSettings
from .sequence_layout_settings import SequenceLayoutSettings
from .user_profile_settings.user_profile_settings import UserProfileSettings
from .global_settings.global_settings import GlobalSettings
from .visibility_settings.visibility_settings import VisibilitySettings

if TYPE_CHECKING:
    from main_window.main_window import MainWindow


class SettingsManager(QObject):
    background_changed = pyqtSignal(str)

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()
        self.main_window = main_window
        self.settings = QSettings("settings.ini", QSettings.Format.IniFormat)

        self.global_settings = GlobalSettings(self)
        self.image_export = ImageExportSettings(self)
        self.users = UserProfileSettings(self)
        self.visibility = VisibilitySettings(self)
        self.dictionary_settings = DictionarySettings(self)
        self.sequence_layout = SequenceLayoutSettings(self)
        self.builder_settings = BuilderSettings(self)
        self.sequence_sharing = SequenceSharingSettings(self)
        self.write_tab_settings = WriteTabSettings(self)
