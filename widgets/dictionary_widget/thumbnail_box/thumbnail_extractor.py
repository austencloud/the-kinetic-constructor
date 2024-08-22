import os


class ThumbnailExtractor:
    
    @staticmethod
    def find_thumbnails(word_dir: str) -> list[str]:
        thumbnails = []
        for root, _, files in os.walk(word_dir):
            if "__pycache__" in root:
                continue
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    thumbnails.append(os.path.join(root, file))
        return thumbnails
    
