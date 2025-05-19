import json
from pathlib import Path
from typing import Dict, List, Optional

class TemplateManager:
    def __init__(self, template_dir: str = "data/templates"):
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self._templates: Dict[str, str] = {}
        self._load_templates()
        
    def _load_templates(self) -> None:
        """Load all template files from the template directory."""
        for file in self.template_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    templates = json.load(f)
                    self._templates.update(templates)
            except json.JSONDecodeError:
                continue
                
    def save_template(self, name: str, content: str) -> bool:
        """Save a new template or update existing one."""
        self._templates[name] = content
        return self._save_to_file()
        
    def get_template(self, name: str) -> Optional[str]:
        """Retrieve a template by name."""
        return self._templates.get(name)
        
    def list_templates(self) -> List[str]:
        """Get list of available templates."""
        return list(self._templates.keys())
        
    def delete_template(self, name: str) -> bool:
        """Delete a template."""
        if name in self._templates:
            del self._templates[name]
            return self._save_to_file()
        return False
        
    def _save_to_file(self) -> bool:
        """Save all templates to file."""
        try:
            with open(self.template_dir / "templates.json", 'w', encoding='utf-8') as f:
                json.dump(self._templates, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False