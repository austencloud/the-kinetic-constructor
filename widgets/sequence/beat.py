from widgets.graph_editor.pictograph.pictograph import Pictograph


class Beat(Pictograph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._beat = 0