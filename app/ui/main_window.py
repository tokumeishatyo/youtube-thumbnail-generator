# -*- coding: utf-8 -*-
"""
メインウィンドウ
YouTubeサムネイル生成ツールのメインUI
"""

import os
import sys
import threading
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk

# パスの設定
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import (
    APP_NAME, APP_VERSION, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT,
    UI_SETTINGS, TEMPLATE_TYPES, COLORS, PATHS
)
from logic.image_composer import ImageComposer
from logic.template_manager import TemplateManager, ThumbnailTemplate


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

        # マネージャー初期化
        self.template_manager = TemplateManager(os.path.join(self.base_path, PATHS["templates"]))
        self.image_composer = ImageComposer(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)

        # 状態変数
        self.current_template: ThumbnailTemplate = None
        self.character_image_path: str = None
        self.background_image_path: str = None
        self.preview_image: ImageTk.PhotoImage = None
        self.text_entries: dict = {}

        # API Key
        self.api_key: str = ""

        # UIの構築
        self._setup_ui()

        # 初期テンプレートを選択
        self._select_template("新曲発表")

    def _setup_ui(self):
        """UIをセットアップ"""
        # メインコンテナ
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 3列レイアウト
        self.main_container.grid_columnconfigure(0, weight=1)  # 左列（設定）
        self.main_container.grid_columnconfigure(1, weight=2)  # 中列（編集）
        self.main_container.grid_columnconfigure(2, weight=2)  # 右列（プレビュー）
        self.main_container.grid_rowconfigure(0, weight=1)

        # 左列：設定パネル
        self._setup_settings_panel()

        # 中列：編集パネル
        self._setup_editor_panel()

        # 右列：プレビューパネル
        self._setup_preview_panel()

    def _setup_settings_panel(self):
        """設定パネルのセットアップ"""
        self.settings_frame = ctk.CTkFrame(self.main_container)
        self.settings_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # スクロール可能フレーム
        self.settings_scroll = ctk.CTkScrollableFrame(self.settings_frame)
        self.settings_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # === テンプレート選択 ===
        template_label = ctk.CTkLabel(
            self.settings_scroll, text="テンプレート",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        template_label.pack(pady=(10, 5), anchor="w")

        template_names = self.template_manager.get_template_names()
        self.template_var = ctk.StringVar(value=template_names[0] if template_names else "")

        for name in template_names:
            btn = ctk.CTkRadioButton(
                self.settings_scroll, text=name, variable=self.template_var,
                value=name, command=lambda n=name: self._select_template(n)
            )
            btn.pack(pady=2, anchor="w", padx=10)

        # セパレータ
        sep1 = ctk.CTkFrame(self.settings_scroll, height=2, fg_color="gray50")
        sep1.pack(fill="x", pady=15)

        # === キャラクター選択 ===
        char_label = ctk.CTkLabel(
            self.settings_scroll, text="キャラクター画像",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        char_label.pack(pady=(10, 5), anchor="w")

        self.char_path_label = ctk.CTkLabel(
            self.settings_scroll, text="未選択",
            text_color="gray60", wraplength=200
        )
        self.char_path_label.pack(pady=2, anchor="w", padx=10)

        char_btn = ctk.CTkButton(
            self.settings_scroll, text="画像を選択",
            command=self._select_character_image
        )
        char_btn.pack(pady=5, anchor="w", padx=10)

        # プリセットキャラクター
        preset_label = ctk.CTkLabel(
            self.settings_scroll, text="プリセット:",
            text_color="gray70"
        )
        preset_label.pack(pady=(10, 2), anchor="w", padx=10)

        # ワークスペースの画像を探す
        self._setup_preset_characters()

        # セパレータ
        sep2 = ctk.CTkFrame(self.settings_scroll, height=2, fg_color="gray50")
        sep2.pack(fill="x", pady=15)

        # === 背景設定 ===
        bg_label = ctk.CTkLabel(
            self.settings_scroll, text="背景",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        bg_label.pack(pady=(10, 5), anchor="w")

        self.bg_mode_var = ctk.StringVar(value="color")

        bg_color_radio = ctk.CTkRadioButton(
            self.settings_scroll, text="単色", variable=self.bg_mode_var,
            value="color", command=self._on_bg_mode_change
        )
        bg_color_radio.pack(pady=2, anchor="w", padx=10)

        bg_image_radio = ctk.CTkRadioButton(
            self.settings_scroll, text="画像", variable=self.bg_mode_var,
            value="image", command=self._on_bg_mode_change
        )
        bg_image_radio.pack(pady=2, anchor="w", padx=10)

        bg_ai_radio = ctk.CTkRadioButton(
            self.settings_scroll, text="AI生成", variable=self.bg_mode_var,
            value="ai", command=self._on_bg_mode_change
        )
        bg_ai_radio.pack(pady=2, anchor="w", padx=10)

        # 背景画像選択ボタン
        self.bg_image_btn = ctk.CTkButton(
            self.settings_scroll, text="背景画像を選択",
            command=self._select_background_image,
            state="disabled"
        )
        self.bg_image_btn.pack(pady=5, anchor="w", padx=10)

        self.bg_path_label = ctk.CTkLabel(
            self.settings_scroll, text="",
            text_color="gray60", wraplength=200
        )
        self.bg_path_label.pack(pady=2, anchor="w", padx=10)

        # AI生成プロンプト
        self.ai_prompt_label = ctk.CTkLabel(
            self.settings_scroll, text="背景プロンプト:",
            text_color="gray70"
        )
        self.ai_prompt_label.pack(pady=(10, 2), anchor="w", padx=10)
        self.ai_prompt_label.pack_forget()  # 初期状態では非表示

        self.ai_prompt_entry = ctk.CTkTextbox(
            self.settings_scroll, height=60, width=200
        )
        self.ai_prompt_entry.pack(pady=2, anchor="w", padx=10)
        self.ai_prompt_entry.insert("1.0", "夕焼けの教室、窓から差し込む光")
        self.ai_prompt_entry.pack_forget()  # 初期状態では非表示

        self.ai_generate_btn = ctk.CTkButton(
            self.settings_scroll, text="背景を生成",
            command=self._generate_ai_background,
            fg_color="#FF5722"
        )
        self.ai_generate_btn.pack(pady=5, anchor="w", padx=10)
        self.ai_generate_btn.pack_forget()  # 初期状態では非表示

        # セパレータ
        sep3 = ctk.CTkFrame(self.settings_scroll, height=2, fg_color="gray50")
        sep3.pack(fill="x", pady=15)

        # === API Key設定 ===
        api_label = ctk.CTkLabel(
            self.settings_scroll, text="API Key",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        api_label.pack(pady=(10, 5), anchor="w")

        self.api_key_entry = ctk.CTkEntry(
            self.settings_scroll, placeholder_text="Google AI API Key",
            show="*", width=200
        )
        self.api_key_entry.pack(pady=5, anchor="w", padx=10)

    def _setup_preset_characters(self):
        """プリセットキャラクターボタンをセットアップ"""
        # ワークスペースの画像を探す
        preset_images = []
        for filename in os.listdir(self.base_path):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                preset_images.append(filename)

        if preset_images:
            for img_name in preset_images[:5]:  # 最大5つ
                btn = ctk.CTkButton(
                    self.settings_scroll,
                    text=img_name[:20] + "..." if len(img_name) > 20 else img_name,
                    command=lambda p=img_name: self._load_preset_character(p),
                    width=180, height=28,
                    fg_color="gray30", hover_color="gray40"
                )
                btn.pack(pady=2, anchor="w", padx=10)

    def _setup_editor_panel(self):
        """編集パネルのセットアップ"""
        self.editor_frame = ctk.CTkFrame(self.main_container)
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # スクロール可能フレーム
        self.editor_scroll = ctk.CTkScrollableFrame(self.editor_frame)
        self.editor_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # タイトル
        editor_title = ctk.CTkLabel(
            self.editor_scroll, text="テキスト編集",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        editor_title.pack(pady=(10, 15), anchor="w")

        # テキスト入力フィールド（テンプレート選択時に動的に生成）
        self.text_fields_frame = ctk.CTkFrame(self.editor_scroll, fg_color="transparent")
        self.text_fields_frame.pack(fill="x", pady=5)

        # セパレータ
        sep = ctk.CTkFrame(self.editor_scroll, height=2, fg_color="gray50")
        sep.pack(fill="x", pady=15)

        # レイアウト調整
        layout_title = ctk.CTkLabel(
            self.editor_scroll, text="レイアウト調整",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        layout_title.pack(pady=(10, 10), anchor="w")

        # キャラクター位置
        char_pos_frame = ctk.CTkFrame(self.editor_scroll, fg_color="transparent")
        char_pos_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(char_pos_frame, text="キャラ位置 X:").pack(side="left", padx=(0, 5))
        self.char_x_slider = ctk.CTkSlider(
            char_pos_frame, from_=0, to=THUMBNAIL_WIDTH,
            command=self._on_layout_change
        )
        self.char_x_slider.set(300)
        self.char_x_slider.pack(side="left", fill="x", expand=True, padx=5)

        char_pos_y_frame = ctk.CTkFrame(self.editor_scroll, fg_color="transparent")
        char_pos_y_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(char_pos_y_frame, text="キャラ位置 Y:").pack(side="left", padx=(0, 5))
        self.char_y_slider = ctk.CTkSlider(
            char_pos_y_frame, from_=0, to=THUMBNAIL_HEIGHT,
            command=self._on_layout_change
        )
        self.char_y_slider.set(400)
        self.char_y_slider.pack(side="left", fill="x", expand=True, padx=5)

        # キャラクターサイズ
        char_size_frame = ctk.CTkFrame(self.editor_scroll, fg_color="transparent")
        char_size_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(char_size_frame, text="キャラサイズ:").pack(side="left", padx=(0, 5))
        self.char_size_slider = ctk.CTkSlider(
            char_size_frame, from_=100, to=800,
            command=self._on_layout_change
        )
        self.char_size_slider.set(450)
        self.char_size_slider.pack(side="left", fill="x", expand=True, padx=5)

        # プレビュー更新ボタン
        update_btn = ctk.CTkButton(
            self.editor_scroll, text="プレビュー更新",
            command=self._update_preview,
            fg_color=COLORS["primary"]
        )
        update_btn.pack(pady=20)

    def _setup_preview_panel(self):
        """プレビューパネルのセットアップ"""
        self.preview_frame = ctk.CTkFrame(self.main_container)
        self.preview_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        # タイトル
        preview_title = ctk.CTkLabel(
            self.preview_frame, text="プレビュー",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        preview_title.pack(pady=(10, 10))

        # サイズ表示
        size_label = ctk.CTkLabel(
            self.preview_frame, text=f"{THUMBNAIL_WIDTH} x {THUMBNAIL_HEIGHT}px",
            text_color="gray60"
        )
        size_label.pack(pady=(0, 10))

        # プレビュー画像表示エリア
        self.preview_canvas = ctk.CTkLabel(
            self.preview_frame, text="",
            width=int(THUMBNAIL_WIDTH * UI_SETTINGS["preview_scale"]),
            height=int(THUMBNAIL_HEIGHT * UI_SETTINGS["preview_scale"]),
            fg_color="gray20"
        )
        self.preview_canvas.pack(pady=10, padx=10)

        # 出力ボタン
        btn_frame = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        png_btn = ctk.CTkButton(
            btn_frame, text="PNG出力",
            command=lambda: self._save_image("PNG"),
            fg_color="#4CAF50"
        )
        png_btn.pack(side="left", padx=5)

        jpeg_btn = ctk.CTkButton(
            btn_frame, text="JPEG出力",
            command=lambda: self._save_image("JPEG"),
            fg_color="#2196F3"
        )
        jpeg_btn.pack(side="left", padx=5)

    def _select_template(self, template_name: str):
        """テンプレートを選択"""
        template = self.template_manager.get_template_by_name(template_name)
        if template:
            self.current_template = template
            self._update_text_fields()
            self._update_preview()

    def _update_text_fields(self):
        """テキスト入力フィールドを更新"""
        # 既存のフィールドを削除
        for widget in self.text_fields_frame.winfo_children():
            widget.destroy()
        self.text_entries.clear()

        if not self.current_template:
            return

        # テンプレートのテキスト要素に基づいてフィールドを生成
        for text_element in self.current_template.text_elements:
            field_frame = ctk.CTkFrame(self.text_fields_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=5)

            label = ctk.CTkLabel(field_frame, text=f"{text_element.label}:")
            label.pack(anchor="w")

            entry = ctk.CTkEntry(field_frame, width=300)
            entry.insert(0, text_element.default_text)
            entry.pack(fill="x", pady=2)
            entry.bind("<KeyRelease>", lambda e: self._update_preview())

            self.text_entries[text_element.id] = entry

    def _select_character_image(self):
        """キャラクター画像を選択"""
        filepath = filedialog.askopenfilename(
            title="キャラクター画像を選択",
            filetypes=[
                ("画像ファイル", "*.png *.jpg *.jpeg *.webp"),
                ("すべてのファイル", "*.*")
            ],
            initialdir=self.base_path
        )
        if filepath:
            self.character_image_path = filepath
            self.char_path_label.configure(text=os.path.basename(filepath))
            self._update_preview()

    def _load_preset_character(self, filename: str):
        """プリセットキャラクターを読み込み"""
        filepath = os.path.join(self.base_path, filename)
        if os.path.exists(filepath):
            self.character_image_path = filepath
            self.char_path_label.configure(text=filename)
            self._update_preview()

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

    def _on_bg_mode_change(self):
        """背景モード変更時の処理"""
        mode = self.bg_mode_var.get()

        if mode == "image":
            self.bg_image_btn.configure(state="normal")
            self.ai_prompt_label.pack_forget()
            self.ai_prompt_entry.pack_forget()
            self.ai_generate_btn.pack_forget()
        elif mode == "ai":
            self.bg_image_btn.configure(state="disabled")
            self.ai_prompt_label.pack(pady=(10, 2), anchor="w", padx=10)
            self.ai_prompt_entry.pack(pady=2, anchor="w", padx=10)
            self.ai_generate_btn.pack(pady=5, anchor="w", padx=10)
        else:
            self.bg_image_btn.configure(state="disabled")
            self.ai_prompt_label.pack_forget()
            self.ai_prompt_entry.pack_forget()
            self.ai_generate_btn.pack_forget()

        self._update_preview()

    def _generate_ai_background(self):
        """AI背景を生成"""
        api_key = self.api_key_entry.get()
        if not api_key:
            messagebox.showwarning("警告", "API Keyを入力してください。")
            return

        prompt = self.ai_prompt_entry.get("1.0", "end-1c")
        if not prompt.strip():
            messagebox.showwarning("警告", "プロンプトを入力してください。")
            return

        # TODO: AI背景生成の実装
        messagebox.showinfo("情報", "AI背景生成機能は開発中です。")

    def _on_layout_change(self, value=None):
        """レイアウト変更時の処理"""
        self._update_preview()

    def _update_preview(self):
        """プレビューを更新"""
        if not self.current_template:
            return

        # 新しいコンポーザーを作成
        self.image_composer = ImageComposer(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)

        # 背景を設定
        bg_mode = self.bg_mode_var.get()
        if bg_mode == "image" and self.background_image_path:
            self.image_composer.set_background_image(self.background_image_path)
        else:
            self.image_composer.create_canvas(self.current_template.background_color)

        # グラデーションオーバーレイを追加
        if self.current_template.background_gradient:
            self.image_composer.add_gradient_overlay(
                direction=self.current_template.background_gradient.get("direction", "bottom"),
                color=self.current_template.background_gradient.get("color", "#000000"),
                opacity=self.current_template.background_gradient.get("opacity", 0.5)
            )

        # キャラクターを追加
        if self.character_image_path:
            char_x = int(self.char_x_slider.get())
            char_y = int(self.char_y_slider.get())
            char_size = int(self.char_size_slider.get())

            self.image_composer.add_character(
                self.character_image_path,
                position=(char_x, char_y),
                size=(char_size, int(char_size * 1.3)),
                anchor="center"
            )

        # ラベルを追加
        for label_data in self.current_template.labels:
            self.image_composer.add_label(
                text=label_data.get("text", ""),
                position=tuple(label_data.get("position", [50, 50])),
                bg_color=label_data.get("bg_color", "#FF0000"),
                text_color=label_data.get("text_color", "#FFFFFF"),
                font_size=label_data.get("font_size", 24)
            )

        # テキストを追加
        for text_element in self.current_template.text_elements:
            text = self.text_entries.get(text_element.id)
            if text:
                text_content = text.get()
            else:
                text_content = text_element.default_text

            self.image_composer.add_text(
                text=text_content,
                position=text_element.position,
                font_size=text_element.font_size,
                font_color=text_element.font_color,
                anchor=text_element.anchor,
                stroke_width=text_element.stroke_width,
                stroke_color=text_element.stroke_color,
                shadow=text_element.shadow
            )

        # プレビュー画像を更新
        preview_img = self.image_composer.get_image()
        if preview_img:
            # スケールダウン
            preview_width = int(THUMBNAIL_WIDTH * UI_SETTINGS["preview_scale"])
            preview_height = int(THUMBNAIL_HEIGHT * UI_SETTINGS["preview_scale"])
            preview_img = preview_img.resize(
                (preview_width, preview_height),
                Image.Resampling.LANCZOS
            )

            # CTkImageを使用
            self.preview_image = ctk.CTkImage(
                light_image=preview_img,
                dark_image=preview_img,
                size=(preview_width, preview_height)
            )
            self.preview_canvas.configure(image=self.preview_image)

    def _save_image(self, format: str):
        """画像を保存"""
        if not self.image_composer.get_image():
            messagebox.showwarning("警告", "保存する画像がありません。")
            return

        # 出力ディレクトリ
        output_dir = os.path.join(self.base_path, PATHS["output"])
        os.makedirs(output_dir, exist_ok=True)

        # ファイルダイアログ
        extension = ".png" if format == "PNG" else ".jpg"
        default_name = f"thumbnail{extension}"

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
