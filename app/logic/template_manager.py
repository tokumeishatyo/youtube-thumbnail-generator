# -*- coding: utf-8 -*-
"""
テンプレート管理ロジック
サムネイルテンプレートの定義と管理
"""

import os
import yaml
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class TextElement:
    """テキスト要素の定義"""
    id: str
    label: str  # UIに表示するラベル
    default_text: str = ""
    position: tuple = (640, 360)  # (x, y)
    font_size: int = 48
    font_color: str = "#FFFFFF"
    anchor: str = "center"
    stroke_width: int = 2
    stroke_color: str = "#000000"
    shadow: bool = True


@dataclass
class CharacterSlot:
    """キャラクタースロットの定義"""
    id: str
    position: tuple = (200, 360)  # (x, y)
    size: tuple = (400, 600)  # (width, height)
    anchor: str = "center"


@dataclass
class ThumbnailTemplate:
    """サムネイルテンプレートの定義"""
    id: str
    name: str
    description: str = ""
    background_color: str = "#1a1a2e"
    background_gradient: Optional[Dict] = None
    text_elements: List[TextElement] = field(default_factory=list)
    character_slots: List[CharacterSlot] = field(default_factory=list)
    labels: List[Dict] = field(default_factory=list)


# デフォルトテンプレート定義
DEFAULT_TEMPLATES = {
    "new_song": ThumbnailTemplate(
        id="new_song",
        name="新曲発表",
        description="新曲リリース告知用のテンプレート",
        background_color="#1a1a2e",
        background_gradient={"direction": "bottom", "color": "#000000", "opacity": 0.6},
        text_elements=[
            TextElement(
                id="title",
                label="曲名",
                default_text="新曲タイトル",
                position=(800, 300),
                font_size=72,
                font_color="#FFFFFF",
                anchor="left",
                stroke_width=3,
                stroke_color="#000000",
                shadow=True
            ),
            TextElement(
                id="artist",
                label="アーティスト名",
                default_text="彩瀬こよみ",
                position=(800, 400),
                font_size=36,
                font_color="#FFD700",
                anchor="left",
                stroke_width=2,
                stroke_color="#000000",
                shadow=True
            ),
            TextElement(
                id="date",
                label="公開日",
                default_text="○月○日公開",
                position=(800, 480),
                font_size=28,
                font_color="#FFFFFF",
                anchor="left",
                stroke_width=1,
                stroke_color="#000000",
                shadow=False
            ),
        ],
        character_slots=[
            CharacterSlot(
                id="main_character",
                position=(300, 400),
                size=(450, 600),
                anchor="center"
            )
        ],
        labels=[
            {
                "text": "NEW",
                "position": (50, 50),
                "bg_color": "#FF0000",
                "text_color": "#FFFFFF",
                "font_size": 32
            }
        ]
    ),

    "cover": ThumbnailTemplate(
        id="cover",
        name="カバー曲",
        description="カバー曲用のテンプレート",
        background_color="#2d132c",
        background_gradient={"direction": "bottom", "color": "#000000", "opacity": 0.5},
        text_elements=[
            TextElement(
                id="title",
                label="曲名",
                default_text="カバー曲タイトル",
                position=(800, 280),
                font_size=64,
                font_color="#FFFFFF",
                anchor="left",
                stroke_width=3,
                stroke_color="#000000",
                shadow=True
            ),
            TextElement(
                id="original",
                label="原曲アーティスト",
                default_text="原曲: ○○○",
                position=(800, 370),
                font_size=28,
                font_color="#CCCCCC",
                anchor="left",
                stroke_width=1,
                stroke_color="#000000",
                shadow=False
            ),
            TextElement(
                id="artist",
                label="歌唱者",
                default_text="歌: 彩瀬こよみ",
                position=(800, 420),
                font_size=32,
                font_color="#FFD700",
                anchor="left",
                stroke_width=2,
                stroke_color="#000000",
                shadow=True
            ),
        ],
        character_slots=[
            CharacterSlot(
                id="main_character",
                position=(300, 400),
                size=(450, 600),
                anchor="center"
            )
        ],
        labels=[
            {
                "text": "COVER",
                "position": (50, 50),
                "bg_color": "#9C27B0",
                "text_color": "#FFFFFF",
                "font_size": 32
            }
        ]
    ),

    "utatte_mita": ThumbnailTemplate(
        id="utatte_mita",
        name="歌ってみた",
        description="歌ってみた動画用のテンプレート",
        background_color="#0d47a1",
        background_gradient={"direction": "bottom", "color": "#000000", "opacity": 0.5},
        text_elements=[
            TextElement(
                id="title",
                label="曲名",
                default_text="曲名",
                position=(800, 300),
                font_size=64,
                font_color="#FFFFFF",
                anchor="left",
                stroke_width=3,
                stroke_color="#000000",
                shadow=True
            ),
            TextElement(
                id="artist",
                label="歌唱者",
                default_text="彩瀬こよみ",
                position=(800, 400),
                font_size=36,
                font_color="#00E5FF",
                anchor="left",
                stroke_width=2,
                stroke_color="#000000",
                shadow=True
            ),
        ],
        character_slots=[
            CharacterSlot(
                id="main_character",
                position=(300, 400),
                size=(450, 600),
                anchor="center"
            )
        ],
        labels=[
            {
                "text": "歌ってみた",
                "position": (50, 50),
                "bg_color": "#2196F3",
                "text_color": "#FFFFFF",
                "font_size": 28
            }
        ]
    ),

    "mv": ThumbnailTemplate(
        id="mv",
        name="MV公開",
        description="ミュージックビデオ公開用のテンプレート",
        background_color="#1b1b1b",
        background_gradient={"direction": "bottom", "color": "#000000", "opacity": 0.7},
        text_elements=[
            TextElement(
                id="title",
                label="曲名",
                default_text="曲名",
                position=(640, 550),
                font_size=72,
                font_color="#FFFFFF",
                anchor="center",
                stroke_width=3,
                stroke_color="#000000",
                shadow=True
            ),
            TextElement(
                id="artist",
                label="アーティスト名",
                default_text="彩瀬こよみ",
                position=(640, 630),
                font_size=36,
                font_color="#FFD700",
                anchor="center",
                stroke_width=2,
                stroke_color="#000000",
                shadow=True
            ),
        ],
        character_slots=[
            CharacterSlot(
                id="main_character",
                position=(640, 300),
                size=(500, 500),
                anchor="center"
            )
        ],
        labels=[
            {
                "text": "MV",
                "position": (50, 50),
                "bg_color": "#E91E63",
                "text_color": "#FFFFFF",
                "font_size": 36
            }
        ]
    ),

    "live": ThumbnailTemplate(
        id="live",
        name="LIVE告知",
        description="ライブ配信告知用のテンプレート",
        background_color="#b71c1c",
        background_gradient={"direction": "bottom", "color": "#000000", "opacity": 0.6},
        text_elements=[
            TextElement(
                id="title",
                label="配信タイトル",
                default_text="歌枠配信",
                position=(800, 280),
                font_size=56,
                font_color="#FFFFFF",
                anchor="left",
                stroke_width=3,
                stroke_color="#000000",
                shadow=True
            ),
            TextElement(
                id="date",
                label="日時",
                default_text="○月○日 20:00〜",
                position=(800, 370),
                font_size=36,
                font_color="#FFEB3B",
                anchor="left",
                stroke_width=2,
                stroke_color="#000000",
                shadow=True
            ),
            TextElement(
                id="description",
                label="説明",
                default_text="みんな来てね!",
                position=(800, 450),
                font_size=28,
                font_color="#FFFFFF",
                anchor="left",
                stroke_width=1,
                stroke_color="#000000",
                shadow=False
            ),
        ],
        character_slots=[
            CharacterSlot(
                id="main_character",
                position=(300, 400),
                size=(450, 600),
                anchor="center"
            )
        ],
        labels=[
            {
                "text": "LIVE",
                "position": (50, 50),
                "bg_color": "#F44336",
                "text_color": "#FFFFFF",
                "font_size": 36
            }
        ]
    ),
}


class TemplateManager:
    """テンプレート管理クラス"""

    def __init__(self, templates_dir: str = "templates"):
        """
        Args:
            templates_dir: テンプレートディレクトリのパス
        """
        self.templates_dir = templates_dir
        self.templates: Dict[str, ThumbnailTemplate] = {}
        self._load_default_templates()
        self._load_custom_templates()

    def _load_default_templates(self):
        """デフォルトテンプレートを読み込み"""
        self.templates.update(DEFAULT_TEMPLATES)

    def _load_custom_templates(self):
        """カスタムテンプレートをYAMLから読み込み"""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir, exist_ok=True)
            return

        for filename in os.listdir(self.templates_dir):
            if filename.endswith((".yaml", ".yml")):
                filepath = os.path.join(self.templates_dir, filename)
                try:
                    template = self._load_template_from_yaml(filepath)
                    if template:
                        self.templates[template.id] = template
                except Exception as e:
                    print(f"テンプレート読み込みエラー ({filename}): {e}")

    def _load_template_from_yaml(self, filepath: str) -> Optional[ThumbnailTemplate]:
        """YAMLファイルからテンプレートを読み込み"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            text_elements = []
            for te_data in data.get("text_elements", []):
                text_elements.append(TextElement(
                    id=te_data["id"],
                    label=te_data.get("label", te_data["id"]),
                    default_text=te_data.get("default_text", ""),
                    position=tuple(te_data.get("position", [640, 360])),
                    font_size=te_data.get("font_size", 48),
                    font_color=te_data.get("font_color", "#FFFFFF"),
                    anchor=te_data.get("anchor", "center"),
                    stroke_width=te_data.get("stroke_width", 2),
                    stroke_color=te_data.get("stroke_color", "#000000"),
                    shadow=te_data.get("shadow", True)
                ))

            character_slots = []
            for cs_data in data.get("character_slots", []):
                character_slots.append(CharacterSlot(
                    id=cs_data["id"],
                    position=tuple(cs_data.get("position", [200, 360])),
                    size=tuple(cs_data.get("size", [400, 600])),
                    anchor=cs_data.get("anchor", "center")
                ))

            return ThumbnailTemplate(
                id=data["id"],
                name=data["name"],
                description=data.get("description", ""),
                background_color=data.get("background_color", "#1a1a2e"),
                background_gradient=data.get("background_gradient"),
                text_elements=text_elements,
                character_slots=character_slots,
                labels=data.get("labels", [])
            )

        except Exception as e:
            print(f"YAML読み込みエラー: {e}")
            return None

    def get_template(self, template_id: str) -> Optional[ThumbnailTemplate]:
        """テンプレートを取得"""
        return self.templates.get(template_id)

    def get_all_templates(self) -> Dict[str, ThumbnailTemplate]:
        """全テンプレートを取得"""
        return self.templates

    def get_template_names(self) -> List[str]:
        """テンプレート名のリストを取得"""
        return [t.name for t in self.templates.values()]

    def get_template_by_name(self, name: str) -> Optional[ThumbnailTemplate]:
        """名前からテンプレートを取得"""
        for template in self.templates.values():
            if template.name == name:
                return template
        return None

    def save_template(self, template: ThumbnailTemplate, filename: str = None) -> bool:
        """テンプレートをYAMLファイルに保存"""
        try:
            if filename is None:
                filename = f"{template.id}.yaml"

            filepath = os.path.join(self.templates_dir, filename)

            data = {
                "id": template.id,
                "name": template.name,
                "description": template.description,
                "background_color": template.background_color,
                "background_gradient": template.background_gradient,
                "text_elements": [
                    {
                        "id": te.id,
                        "label": te.label,
                        "default_text": te.default_text,
                        "position": list(te.position),
                        "font_size": te.font_size,
                        "font_color": te.font_color,
                        "anchor": te.anchor,
                        "stroke_width": te.stroke_width,
                        "stroke_color": te.stroke_color,
                        "shadow": te.shadow
                    }
                    for te in template.text_elements
                ],
                "character_slots": [
                    {
                        "id": cs.id,
                        "position": list(cs.position),
                        "size": list(cs.size),
                        "anchor": cs.anchor
                    }
                    for cs in template.character_slots
                ],
                "labels": template.labels
            }

            os.makedirs(self.templates_dir, exist_ok=True)

            with open(filepath, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

            return True

        except Exception as e:
            print(f"テンプレート保存エラー: {e}")
            return False
