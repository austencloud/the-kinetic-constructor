from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.settings_manager.settings_manager import SettingsManager

class SequenceSharingSettings:
    DEFAULT_SEQUENCE_SHARING_SETTINGS = {"emails": []}  # Store emails in a list

    def __init__(self, settings_manager:" SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.emails = settings_manager.settings.get("sequence_sharing", {}).get(
            "emails", []
        )

    def add_email(self, email):
        if email not in self.emails:
            self.emails.append(email)
            self.settings_manager.save_sequence_sharing_settings(
                {"emails": self.emails}
            )

    def get_saved_emails(self):
        return self.emails
