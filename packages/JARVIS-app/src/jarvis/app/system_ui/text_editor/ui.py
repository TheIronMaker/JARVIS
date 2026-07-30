# The format of this would have to be cross platform and GUI rendering
# Could create links to zeromq without going into PySide6 details

from jarvis.core_modules.nodes import Node
from jarvis.core_modules.network import Subscriber, Publisher


class TextEditorUI(Node):
    def __init__(self, id:str=None):
        
        super().__init__(id, )
        self.load_manifest(f"app/system_ui/text_editor/builds/{self.id}/manifest.json")
        if not self.manifest: return False

        self.create_coms()
        #print(self.subs)


editor = TextEditorUI("019fb08a-c80f-7379-a666-ad7ea34f1511")
print(editor.module_dir)
