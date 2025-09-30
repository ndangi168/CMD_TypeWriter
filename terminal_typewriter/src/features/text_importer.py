import os
from typing import List, Dict, Any, Optional
from pathlib import Path


class TextImporter:
    """Handle importing custom text files for typing practice."""
    
    def __init__(self, texts_dir: str = None):
        if texts_dir is None:
            texts_dir = os.path.join(os.getcwd(), "terminal_typewriter", "data", "texts")
        self.texts_dir = Path(texts_dir)
        self.texts_dir.mkdir(parents=True, exist_ok=True)

    def import_text_file(self, file_path: str, difficulty: str = "custom", name: str = None) -> Dict[str, Any]:
        """Import a text file and save it for use in typing tests."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {"success": False, "error": "File not found"}
            
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                return {"success": False, "error": "File is empty"}
            
            # Generate name if not provided
            if name is None:
                name = file_path.stem
            
            # Save to texts directory
            import_file = self.texts_dir / f"{name}_{difficulty}.txt"
            with open(import_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Calculate word count
            word_count = len(content.split())
            
            return {
                "success": True,
                "name": name,
                "difficulty": difficulty,
                "word_count": word_count,
                "file_path": str(import_file),
                "content": content
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def import_text_content(self, content: str, name: str, difficulty: str = "custom") -> Dict[str, Any]:
        """Import text content directly from string."""
        try:
            content = content.strip()
            if not content:
                return {"success": False, "error": "Content is empty"}
            
            # Save to texts directory
            import_file = self.texts_dir / f"{name}_{difficulty}.txt"
            with open(import_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Calculate word count
            word_count = len(content.split())
            
            return {
                "success": True,
                "name": name,
                "difficulty": difficulty,
                "word_count": word_count,
                "file_path": str(import_file),
                "content": content
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_imported_texts(self) -> List[Dict[str, Any]]:
        """List all imported text files."""
        imported_texts = []
        
        for text_file in self.texts_dir.glob("*.txt"):
            try:
                with open(text_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse filename to extract name and difficulty
                name_difficulty = text_file.stem
                if '_' in name_difficulty:
                    name, difficulty = name_difficulty.rsplit('_', 1)
                else:
                    name = name_difficulty
                    difficulty = "custom"
                
                word_count = len(content.split())
                
                imported_texts.append({
                    "name": name,
                    "difficulty": difficulty,
                    "word_count": word_count,
                    "file_path": str(text_file),
                    "content": content
                })
                
            except Exception:
                continue  # Skip files that can't be read
        
        return imported_texts

    def get_text_by_name(self, name: str, difficulty: str = "custom") -> Optional[str]:
        """Get imported text content by name and difficulty."""
        text_file = self.texts_dir / f"{name}_{difficulty}.txt"
        
        if text_file.exists():
            try:
                with open(text_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception:
                pass
        
        return None

    def delete_imported_text(self, name: str, difficulty: str = "custom") -> bool:
        """Delete an imported text file."""
        text_file = self.texts_dir / f"{name}_{difficulty}.txt"
        
        try:
            if text_file.exists():
                text_file.unlink()
                return True
        except Exception:
            pass
        
        return False

    def get_available_texts(self) -> Dict[str, List[str]]:
        """Get available texts organized by difficulty."""
        texts_by_difficulty = {}
        
        for text_info in self.list_imported_texts():
            difficulty = text_info["difficulty"]
            if difficulty not in texts_by_difficulty:
                texts_by_difficulty[difficulty] = []
            texts_by_difficulty[difficulty].append(text_info["name"])
        
        return texts_by_difficulty

    def format_texts_list(self) -> str:
        """Format imported texts for display."""
        imported_texts = self.list_imported_texts()
        
        if not imported_texts:
            return "No custom texts imported yet."
        
        lines = ["📝 Custom Imported Texts:", ""]
        
        # Group by difficulty
        by_difficulty = {}
        for text in imported_texts:
            diff = text["difficulty"]
            if diff not in by_difficulty:
                by_difficulty[diff] = []
            by_difficulty[diff].append(text)
        
        for difficulty, texts in by_difficulty.items():
            lines.append(f"  {difficulty.capitalize()}:")
            for text in texts:
                lines.append(f"    • {text['name']} ({text['word_count']} words)")
        
        return "\n".join(lines)
