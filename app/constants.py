# -*- coding: utf-8 -*-
"""
YouTubeサムネイル生成ツール - 定数定義
"""

# アプリケーション情報
APP_NAME = "YouTube Thumbnail Generator"
APP_VERSION = "1.0.0"

# YouTubeサムネイルサイズ
THUMBNAIL_WIDTH = 1280
THUMBNAIL_HEIGHT = 720

# SNSバナーサイズ（Phase 2用）
BANNER_SIZES = {
    "YouTube サムネイル": (1280, 720),
    "Twitter/X ヘッダー": (1500, 500),
    "YouTube チャンネルアート": (2560, 1440),
    "ニコニコ ヘッダー": (1280, 300),
}

# テンプレートタイプ
TEMPLATE_TYPES = [
    "新曲発表",
    "カバー曲",
    "歌ってみた",
    "MV公開",
    "LIVE告知",
]

# デフォルトカラー
COLORS = {
    "primary": "#1E88E5",
    "secondary": "#FFC107",
    "accent": "#FF5722",
    "text_light": "#FFFFFF",
    "text_dark": "#212121",
    "background": "#F5F5F5",
}

# フォント設定
DEFAULT_FONTS = {
    "title": ("Hiragino Sans", 72, "bold"),
    "subtitle": ("Hiragino Sans", 36, "normal"),
    "label": ("Hiragino Sans", 24, "normal"),
}

# UIサイズ
UI_SETTINGS = {
    "window_width": 1400,
    "window_height": 900,
    "preview_scale": 0.5,  # プレビュー表示のスケール
    "sidebar_width": 250,
}

# ファイルパス
PATHS = {
    "templates": "templates",
    "characters": "characters",
    "output": "output",
}

# API設定
API_MODEL = "gemini-2.0-flash-preview-image-generation"
