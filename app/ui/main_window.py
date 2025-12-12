# -*- coding: utf-8 -*-
"""
メインウィンドウ
YouTubeサムネイル生成ツールのメインUI
"""

import os
import sys
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk

# パスの設定
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import (
    APP_NAME, APP_VERSION, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT,
    UI_SETTINGS, COLORS, PATHS
)
from logic.image_composer import ImageComposer


# テキストスタイルプリセット
TEXT_STYLES = {
    "インパクト": {
        "font_size_title": 80,
        "font_size_artist": 56,
        "font_color": "#FFFFFF",
        "stroke_width": 8,
        "stroke_color": "#000000",
        "shadow": True,
        "shadow_color": "#000000",
        "shadow_offset": (4, 4),
    },
    "ポップ": {
        "font_size_title": 72,
        "font_size_artist": 48,
        "font_color": "#FFEB3B",
        "stroke_width": 6,
        "stroke_color": "#E91E63",
        "shadow": True,
        "shadow_color": "#000000",
        "shadow_offset": (3, 3),
    },
    "シンプル": {
        "font_size_title": 64,
        "font_size_artist": 40,
        "font_color": "#FFFFFF",
        "stroke_width": 3,
        "stroke_color": "#000000",
        "shadow": False,
        "shadow_color": "#000000",
        "shadow_offset": (2, 2),
    },
    "エレガント": {
        "font_size_title": 60,
        "font_size_artist": 36,
        "font_color": "#FFFFFF",
        "stroke_width": 2,
        "stroke_color": "#333333",
        "shadow": True,
        "shadow_color": "#666666",
        "shadow_offset": (2, 2),
    },
    "ネオン": {
        "font_size_title": 72,
        "font_size_artist": 48,
        "font_color": "#00FFFF",
        "stroke_width": 4,
        "stroke_color": "#FF00FF",
        "shadow": True,
        "shadow_color": "#0000FF",
        "shadow_offset": (3, 3),
    },
}

# テキスト配置プリセット
TEXT_POSITIONS = {
    "左上": {"title": (50, 120), "artist": (50, 220), "anchor": "left"},
    "左中": {"title": (50, 300), "artist": (50, 400), "anchor": "left"},
    "左下": {"title": (50, 480), "artist": (50, 580), "anchor": "left"},
    "中央": {"title": (640, 300), "artist": (640, 420), "anchor": "center"},
    "右寄せ": {"title": (1230, 300), "artist": (1230, 400), "anchor": "right"},
}


class MainWindow(ctk.CTk):
    """メインウィンドウクラス"""

    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{UI_SETTINGS['window_width']}x{UI_SETTINGS['window_height']}")

        # CustomTkinter設定
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 基本パスの設定
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # 状態変数
        self.background_image_path: str = None
        self.preview_image = None
        self.image_composer = ImageComposer(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)

        # UIの構築
        self._setup_ui()

        # 初期プレビュー
        self._update_preview()

    def _setup_ui(self):
        """UIをセットアップ"""
        # メインコンテナ
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 3列レイアウト
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=2)
        self.main_container.grid_columnconfigure(2, weight=2)
        self.main_container.grid_rowconfigure(0, weight=1)

        # 左列：設定パネル
        self._setup_settings_panel()

        # 中列：テキスト入力パネル
        self._setup_text_panel()

        # 右列：プレビューパネル
        self._setup_preview_panel()

    def _setup_settings_panel(self):
        """設定パネルのセットアップ"""
        self.settings_frame = ctk.CTkFrame(self.main_container)
        self.settings_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        settings_scroll = ctk.CTkScrollableFrame(self.settings_frame)
        settings_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # === 背景画像 ===
        bg_label = ctk.CTkLabel(
            settings_scroll, text="背景画像",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        bg_label.pack(pady=(10, 5), anchor="w")

        self.bg_path_label = ctk.CTkLabel(
            settings_scroll, text="未選択",
            text_color="gray60", wraplength=200
        )
        self.bg_path_label.pack(pady=2, anchor="w", padx=10)

        bg_btn = ctk.CTkButton(
            settings_scroll, text="画像を選択",
            command=self._select_background_image
        )
        bg_btn.pack(pady=5, anchor="w", padx=10)

        # プリセット背景
        self._setup_preset_backgrounds(settings_scroll)

        # セパレータ
        sep1 = ctk.CTkFrame(settings_scroll, height=2, fg_color="gray50")
        sep1.pack(fill="x", pady=15)

        # === テキストスタイル ===
        style_label = ctk.CTkLabel(
            settings_scroll, text="テキストスタイル",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        style_label.pack(pady=(10, 5), anchor="w")

        self.style_var = ctk.StringVar(value="インパクト")
        for style_name in TEXT_STYLES.keys():
            btn = ctk.CTkRadioButton(
                settings_scroll, text=style_name,
                variable=self.style_var, value=style_name,
                command=self._update_preview
            )
            btn.pack(pady=2, anchor="w", padx=10)

        # セパレータ
        sep2 = ctk.CTkFrame(settings_scroll, height=2, fg_color="gray50")
        sep2.pack(fill="x", pady=15)

        # === テキスト配置 ===
        pos_label = ctk.CTkLabel(
            settings_scroll, text="テキスト配置",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        pos_label.pack(pady=(10, 5), anchor="w")

        self.position_var = ctk.StringVar(value="左上")
        for pos_name in TEXT_POSITIONS.keys():
            btn = ctk.CTkRadioButton(
                settings_scroll, text=pos_name,
                variable=self.position_var, value=pos_name,
                command=self._update_preview
            )
            btn.pack(pady=2, anchor="w", padx=10)

    def _setup_preset_backgrounds(self, parent):
        """プリセット背景ボタンをセットアップ"""
        preset_label = ctk.CTkLabel(
            parent, text="プリセット:",
            text_color="gray70"
        )
        preset_label.pack(pady=(10, 2), anchor="w", padx=10)

        # ワークスペースの画像を探す
        preset_images = []
        for filename in os.listdir(self.base_path):
            if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
                preset_images.append(filename)

        if preset_images:
            for img_name in preset_images[:6]:
                display_name = img_name[:18] + "..." if len(img_name) > 18 else img_name
                btn = ctk.CTkButton(
                    parent,
                    text=display_name,
                    command=lambda p=img_name: self._load_preset_background(p),
                    width=180, height=28,
                    fg_color="gray30", hover_color="gray40"
                )
                btn.pack(pady=2, anchor="w", padx=10)

    def _setup_text_panel(self):
        """テキスト入力パネルのセットアップ"""
        self.text_frame = ctk.CTkFrame(self.main_container)
        self.text_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        text_scroll = ctk.CTkScrollableFrame(self.text_frame)
        text_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # タイトル
        panel_title = ctk.CTkLabel(
            text_scroll, text="テキスト入力",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        panel_title.pack(pady=(10, 15), anchor="w")

        # === メインテキスト ===
        main_label = ctk.CTkLabel(
            text_scroll, text="メインテキスト（装飾あり）",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4FC3F7"
        )
        main_label.pack(pady=(10, 5), anchor="w")

        # 曲タイトル
        ctk.CTkLabel(text_scroll, text="曲タイトル:").pack(anchor="w", padx=5)
        self.title_entry = ctk.CTkEntry(text_scroll, width=350, height=35)
        self.title_entry.insert(0, "秋風のプロミス")
        self.title_entry.pack(fill="x", pady=(2, 10), padx=5)
        self.title_entry.bind("<KeyRelease>", lambda e: self._update_preview())

        # アーティスト名
        ctk.CTkLabel(text_scroll, text="アーティスト名:").pack(anchor="w", padx=5)
        self.artist_entry = ctk.CTkEntry(text_scroll, width=350, height=35)
        self.artist_entry.insert(0, "彩瀬こよみ")
        self.artist_entry.pack(fill="x", pady=(2, 10), padx=5)
        self.artist_entry.bind("<KeyRelease>", lambda e: self._update_preview())

        # セパレータ
        sep = ctk.CTkFrame(text_scroll, height=2, fg_color="gray50")
        sep.pack(fill="x", pady=15)

        # === オプションテキスト ===
        opt_label = ctk.CTkLabel(
            text_scroll, text="オプションテキスト（定型）",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#81C784"
        )
        opt_label.pack(pady=(10, 5), anchor="w")

        # 副題/キャッチコピー
        self.subtitle_var = ctk.BooleanVar(value=True)
        subtitle_check = ctk.CTkCheckBox(
            text_scroll, text="副題/キャッチコピー",
            variable=self.subtitle_var,
            command=self._update_preview
        )
        subtitle_check.pack(anchor="w", padx=5)

        self.subtitle_entry = ctk.CTkEntry(text_scroll, width=350)
        self.subtitle_entry.insert(0, "新人AIシンガーソングライター")
        self.subtitle_entry.pack(fill="x", pady=(2, 10), padx=5)
        self.subtitle_entry.bind("<KeyRelease>", lambda e: self._update_preview())

        # 公開日
        self.date_var = ctk.BooleanVar(value=False)
        date_check = ctk.CTkCheckBox(
            text_scroll, text="公開日",
            variable=self.date_var,
            command=self._update_preview
        )
        date_check.pack(anchor="w", padx=5)

        self.date_entry = ctk.CTkEntry(text_scroll, width=350)
        self.date_entry.insert(0, "12月15日公開")
        self.date_entry.pack(fill="x", pady=(2, 10), padx=5)
        self.date_entry.bind("<KeyRelease>", lambda e: self._update_preview())

        # 曲の説明
        self.desc_var = ctk.BooleanVar(value=False)
        desc_check = ctk.CTkCheckBox(
            text_scroll, text="曲の説明",
            variable=self.desc_var,
            command=self._update_preview
        )
        desc_check.pack(anchor="w", padx=5)

        self.desc_entry = ctk.CTkEntry(text_scroll, width=350)
        self.desc_entry.insert(0, "デビュー曲")
        self.desc_entry.pack(fill="x", pady=(2, 10), padx=5)
        self.desc_entry.bind("<KeyRelease>", lambda e: self._update_preview())

        # セパレータ
        sep2 = ctk.CTkFrame(text_scroll, height=2, fg_color="gray50")
        sep2.pack(fill="x", pady=15)

        # プレビュー更新ボタン
        update_btn = ctk.CTkButton(
            text_scroll, text="プレビュー更新",
            command=self._update_preview,
            fg_color=COLORS["primary"],
            height=40
        )
        update_btn.pack(pady=10, fill="x", padx=5)

    def _setup_preview_panel(self):
        """プレビューパネルのセットアップ"""
        self.preview_frame = ctk.CTkFrame(self.main_container)
        self.preview_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        # タイトル
        preview_title = ctk.CTkLabel(
            self.preview_frame, text="プレビュー",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        preview_title.pack(pady=(10, 5))

        size_label = ctk.CTkLabel(
            self.preview_frame, text=f"{THUMBNAIL_WIDTH} x {THUMBNAIL_HEIGHT}px",
            text_color="gray60"
        )
        size_label.pack(pady=(0, 10))

        # プレビュー画像表示
        preview_width = int(THUMBNAIL_WIDTH * UI_SETTINGS["preview_scale"])
        preview_height = int(THUMBNAIL_HEIGHT * UI_SETTINGS["preview_scale"])

        self.preview_canvas = ctk.CTkLabel(
            self.preview_frame, text="背景画像を選択してください",
            width=preview_width,
            height=preview_height,
            fg_color="gray20"
        )
        self.preview_canvas.pack(pady=10, padx=10)

        # 出力ボタン
        btn_frame = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        png_btn = ctk.CTkButton(
            btn_frame, text="PNG出力",
            command=lambda: self._save_image("PNG"),
            fg_color="#4CAF50", width=120
        )
        png_btn.pack(side="left", padx=5)

        jpeg_btn = ctk.CTkButton(
            btn_frame, text="JPEG出力",
            command=lambda: self._save_image("JPEG"),
            fg_color="#2196F3", width=120
        )
        jpeg_btn.pack(side="left", padx=5)

    def _select_background_image(self):
        """背景画像を選択"""
        filepath = filedialog.askopenfilename(
            title="背景画像を選択",
            filetypes=[
                ("画像ファイル", "*.png *.jpg *.jpeg *.webp"),
                ("すべてのファイル", "*.*")
            ],
            initialdir=self.base_path
        )
        if filepath:
            self.background_image_path = filepath
            self.bg_path_label.configure(text=os.path.basename(filepath))
            self._update_preview()

    def _load_preset_background(self, filename: str):
        """プリセット背景を読み込み"""
        filepath = os.path.join(self.base_path, filename)
        if os.path.exists(filepath):
            self.background_image_path = filepath
            self.bg_path_label.configure(text=filename)
            self._update_preview()

    def _update_preview(self):
        """プレビューを更新"""
        # 新しいコンポーザーを作成
        self.image_composer = ImageComposer(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)

        # 背景を設定
        if self.background_image_path:
            self.image_composer.set_background_image(self.background_image_path)
        else:
            self.image_composer.create_canvas("#1a1a2e")

        # スタイルと位置を取得
        style = TEXT_STYLES.get(self.style_var.get(), TEXT_STYLES["インパクト"])
        position = TEXT_POSITIONS.get(self.position_var.get(), TEXT_POSITIONS["左上"])

        # オプションテキストのY位置オフセット計算
        y_offset = 0

        # 副題（オプション）
        if self.subtitle_var.get():
            subtitle_text = self.subtitle_entry.get()
            if subtitle_text:
                subtitle_y = position["title"][1] - 60
                self.image_composer.add_text(
                    text=subtitle_text,
                    position=(position["title"][0], subtitle_y),
                    font_size=28,
                    font_color="#FFFFFF",
                    anchor=position["anchor"],
                    stroke_width=2,
                    stroke_color="#000000",
                    shadow=False
                )

        # 曲タイトル（メイン）
        title_text = self.title_entry.get()
        if title_text:
            self.image_composer.add_text(
                text=title_text,
                position=position["title"],
                font_size=style["font_size_title"],
                font_color=style["font_color"],
                anchor=position["anchor"],
                stroke_width=style["stroke_width"],
                stroke_color=style["stroke_color"],
                shadow=style["shadow"],
                shadow_offset=style["shadow_offset"],
                shadow_color=style["shadow_color"]
            )

        # アーティスト名（メイン）
        artist_text = self.artist_entry.get()
        if artist_text:
            self.image_composer.add_text(
                text=artist_text,
                position=position["artist"],
                font_size=style["font_size_artist"],
                font_color=style["font_color"],
                anchor=position["anchor"],
                stroke_width=style["stroke_width"],
                stroke_color=style["stroke_color"],
                shadow=style["shadow"],
                shadow_offset=style["shadow_offset"],
                shadow_color=style["shadow_color"]
            )

        # 曲の説明（オプション）
        if self.desc_var.get():
            desc_text = self.desc_entry.get()
            if desc_text:
                desc_y = position["artist"][1] + 70
                self.image_composer.add_text(
                    text=desc_text,
                    position=(position["artist"][0], desc_y),
                    font_size=24,
                    font_color="#FFFFFF",
                    anchor=position["anchor"],
                    stroke_width=2,
                    stroke_color="#000000",
                    shadow=False
                )

        # 公開日（オプション）
        if self.date_var.get():
            date_text = self.date_entry.get()
            if date_text:
                # 右下に配置
                self.image_composer.add_text(
                    text=date_text,
                    position=(1230, 670),
                    font_size=24,
                    font_color="#FFEB3B",
                    anchor="right",
                    stroke_width=2,
                    stroke_color="#000000",
                    shadow=False
                )

        # プレビュー画像を更新
        preview_img = self.image_composer.get_image()
        if preview_img:
            preview_width = int(THUMBNAIL_WIDTH * UI_SETTINGS["preview_scale"])
            preview_height = int(THUMBNAIL_HEIGHT * UI_SETTINGS["preview_scale"])
            preview_img = preview_img.resize(
                (preview_width, preview_height),
                Image.Resampling.LANCZOS
            )

            self.preview_image = ctk.CTkImage(
                light_image=preview_img,
                dark_image=preview_img,
                size=(preview_width, preview_height)
            )
            self.preview_canvas.configure(image=self.preview_image, text="")

    def _save_image(self, format: str):
        """画像を保存"""
        if not self.image_composer.get_image():
            messagebox.showwarning("警告", "保存する画像がありません。")
            return

        output_dir = os.path.join(self.base_path, PATHS["output"])
        os.makedirs(output_dir, exist_ok=True)

        extension = ".png" if format == "PNG" else ".jpg"
        title = self.title_entry.get() or "thumbnail"
        # ファイル名に使えない文字を除去
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        default_name = f"{safe_title}{extension}"

        filepath = filedialog.asksaveasfilename(
            title=f"{format}形式で保存",
            defaultextension=extension,
            initialfile=default_name,
            initialdir=output_dir,
            filetypes=[
                (f"{format}ファイル", f"*{extension}"),
                ("すべてのファイル", "*.*")
            ]
        )

        if filepath:
            if self.image_composer.save(filepath, format):
                messagebox.showinfo("完了", f"画像を保存しました:\n{filepath}")
            else:
                messagebox.showerror("エラー", "画像の保存に失敗しました。")
