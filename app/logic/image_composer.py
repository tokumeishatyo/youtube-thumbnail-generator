# -*- coding: utf-8 -*-
"""
画像合成ロジック
サムネイル画像の合成処理
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Optional, Tuple, Dict, Any


class ImageComposer:
    """サムネイル画像の合成クラス"""

    def __init__(self, width: int = 1280, height: int = 720):
        """
        Args:
            width: 出力画像の幅
            height: 出力画像の高さ
        """
        self.width = width
        self.height = height
        self.canvas: Optional[Image.Image] = None

    def create_canvas(self, background_color: str = "#1a1a2e") -> Image.Image:
        """
        新しいキャンバスを作成

        Args:
            background_color: 背景色（16進数カラーコード）

        Returns:
            PIL.Image: 作成されたキャンバス
        """
        self.canvas = Image.new("RGBA", (self.width, self.height), background_color)
        return self.canvas

    def set_background_image(self, image_path: str, fit_mode: str = "cover") -> bool:
        """
        背景画像を設定

        Args:
            image_path: 背景画像のパス
            fit_mode: フィットモード ("cover", "contain", "stretch")

        Returns:
            bool: 成功したかどうか
        """
        try:
            bg_image = Image.open(image_path).convert("RGBA")

            if fit_mode == "cover":
                # アスペクト比を維持しつつ、キャンバスを完全に覆う
                bg_ratio = bg_image.width / bg_image.height
                canvas_ratio = self.width / self.height

                if bg_ratio > canvas_ratio:
                    new_height = self.height
                    new_width = int(new_height * bg_ratio)
                else:
                    new_width = self.width
                    new_height = int(new_width / bg_ratio)

                bg_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # 中央でクロップ
                left = (new_width - self.width) // 2
                top = (new_height - self.height) // 2
                bg_image = bg_image.crop((left, top, left + self.width, top + self.height))

            elif fit_mode == "contain":
                # アスペクト比を維持しつつ、キャンバス内に収める
                bg_image.thumbnail((self.width, self.height), Image.Resampling.LANCZOS)

            elif fit_mode == "stretch":
                bg_image = bg_image.resize((self.width, self.height), Image.Resampling.LANCZOS)

            if self.canvas is None:
                self.canvas = Image.new("RGBA", (self.width, self.height))

            # 背景画像を配置
            if fit_mode == "contain":
                x = (self.width - bg_image.width) // 2
                y = (self.height - bg_image.height) // 2
                self.canvas.paste(bg_image, (x, y))
            else:
                self.canvas = bg_image

            return True

        except Exception as e:
            print(f"背景画像の設定エラー: {e}")
            return False

    def set_background_from_pil(self, pil_image: Image.Image, fit_mode: str = "cover") -> bool:
        """
        PIL画像から背景を設定

        Args:
            pil_image: PIL画像オブジェクト
            fit_mode: フィットモード

        Returns:
            bool: 成功したかどうか
        """
        try:
            bg_image = pil_image.convert("RGBA")

            if fit_mode == "cover":
                bg_ratio = bg_image.width / bg_image.height
                canvas_ratio = self.width / self.height

                if bg_ratio > canvas_ratio:
                    new_height = self.height
                    new_width = int(new_height * bg_ratio)
                else:
                    new_width = self.width
                    new_height = int(new_width / bg_ratio)

                bg_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                left = (new_width - self.width) // 2
                top = (new_height - self.height) // 2
                bg_image = bg_image.crop((left, top, left + self.width, top + self.height))

            elif fit_mode == "stretch":
                bg_image = bg_image.resize((self.width, self.height), Image.Resampling.LANCZOS)

            self.canvas = bg_image
            return True

        except Exception as e:
            print(f"背景設定エラー: {e}")
            return False

    def add_character(
        self,
        image_path: str,
        position: Tuple[int, int] = (0, 0),
        size: Optional[Tuple[int, int]] = None,
        anchor: str = "topleft"
    ) -> bool:
        """
        キャラクター画像を追加

        Args:
            image_path: キャラクター画像のパス
            position: 配置位置 (x, y)
            size: リサイズ後のサイズ (width, height)、Noneの場合は元のサイズ
            anchor: アンカーポイント ("topleft", "center", "bottomright" など)

        Returns:
            bool: 成功したかどうか
        """
        try:
            char_image = Image.open(image_path).convert("RGBA")

            if size:
                char_image = char_image.resize(size, Image.Resampling.LANCZOS)

            x, y = position

            # アンカーポイントに基づいて位置を調整
            if "center" in anchor:
                x -= char_image.width // 2
            elif "right" in anchor:
                x -= char_image.width

            if "center" in anchor or anchor == "center":
                y -= char_image.height // 2
            elif "bottom" in anchor:
                y -= char_image.height

            if self.canvas is None:
                self.create_canvas()

            self.canvas.paste(char_image, (x, y), char_image)
            return True

        except Exception as e:
            print(f"キャラクター追加エラー: {e}")
            return False

    def add_character_from_pil(
        self,
        pil_image: Image.Image,
        position: Tuple[int, int] = (0, 0),
        size: Optional[Tuple[int, int]] = None,
        anchor: str = "topleft"
    ) -> bool:
        """
        PIL画像からキャラクターを追加
        """
        try:
            char_image = pil_image.convert("RGBA")

            if size:
                char_image = char_image.resize(size, Image.Resampling.LANCZOS)

            x, y = position

            if "center" in anchor:
                x -= char_image.width // 2
            elif "right" in anchor:
                x -= char_image.width

            if "center" in anchor or anchor == "center":
                y -= char_image.height // 2
            elif "bottom" in anchor:
                y -= char_image.height

            if self.canvas is None:
                self.create_canvas()

            self.canvas.paste(char_image, (x, y), char_image)
            return True

        except Exception as e:
            print(f"キャラクター追加エラー: {e}")
            return False

    def add_text(
        self,
        text: str,
        position: Tuple[int, int],
        font_size: int = 48,
        font_color: str = "#FFFFFF",
        font_path: Optional[str] = None,
        anchor: str = "topleft",
        stroke_width: int = 0,
        stroke_color: str = "#000000",
        shadow: bool = False,
        shadow_offset: Tuple[int, int] = (3, 3),
        shadow_color: str = "#000000"
    ) -> bool:
        """
        テキストを追加

        Args:
            text: 追加するテキスト
            position: 配置位置 (x, y)
            font_size: フォントサイズ
            font_color: フォント色
            font_path: フォントファイルのパス（Noneの場合はデフォルト）
            anchor: アンカーポイント
            stroke_width: 縁取りの太さ
            stroke_color: 縁取りの色
            shadow: 影をつけるかどうか
            shadow_offset: 影のオフセット
            shadow_color: 影の色

        Returns:
            bool: 成功したかどうか
        """
        try:
            if self.canvas is None:
                self.create_canvas()

            draw = ImageDraw.Draw(self.canvas)

            # フォントの読み込み
            try:
                if font_path and os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    # システムフォントを探す
                    font_candidates = [
                        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
                        "/System/Library/Fonts/Hiragino Sans GB.ttc",
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                        "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
                    ]
                    font = None
                    for candidate in font_candidates:
                        if os.path.exists(candidate):
                            font = ImageFont.truetype(candidate, font_size)
                            break
                    if font is None:
                        font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()

            # テキストのバウンディングボックスを取得
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x, y = position

            # アンカーポイントに基づいて位置を調整
            if "center" in anchor:
                x -= text_width // 2
            elif "right" in anchor:
                x -= text_width

            if anchor == "center":
                y -= text_height // 2
            elif "bottom" in anchor:
                y -= text_height

            # 影を描画
            if shadow:
                shadow_x = x + shadow_offset[0]
                shadow_y = y + shadow_offset[1]
                draw.text((shadow_x, shadow_y), text, font=font, fill=shadow_color)

            # テキストを描画
            if stroke_width > 0:
                draw.text(
                    (x, y), text, font=font, fill=font_color,
                    stroke_width=stroke_width, stroke_fill=stroke_color
                )
            else:
                draw.text((x, y), text, font=font, fill=font_color)

            return True

        except Exception as e:
            print(f"テキスト追加エラー: {e}")
            return False

    def add_label(
        self,
        text: str,
        position: Tuple[int, int],
        bg_color: str = "#FF0000",
        text_color: str = "#FFFFFF",
        font_size: int = 24,
        padding: Tuple[int, int] = (20, 10),
        border_radius: int = 5
    ) -> bool:
        """
        ラベル（背景付きテキスト）を追加

        Args:
            text: ラベルテキスト
            position: 配置位置
            bg_color: 背景色
            text_color: テキスト色
            font_size: フォントサイズ
            padding: パディング (horizontal, vertical)
            border_radius: 角丸の半径

        Returns:
            bool: 成功したかどうか
        """
        try:
            if self.canvas is None:
                self.create_canvas()

            # テキストサイズを計算
            temp_draw = ImageDraw.Draw(self.canvas)
            try:
                font_candidates = [
                    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                ]
                font = None
                for candidate in font_candidates:
                    if os.path.exists(candidate):
                        font = ImageFont.truetype(candidate, font_size)
                        break
                if font is None:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()

            bbox = temp_draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # ラベルサイズ
            label_width = text_width + padding[0] * 2
            label_height = text_height + padding[1] * 2

            # ラベル画像を作成
            label_img = Image.new("RGBA", (label_width, label_height), (0, 0, 0, 0))
            label_draw = ImageDraw.Draw(label_img)

            # 角丸四角形を描画
            label_draw.rounded_rectangle(
                [(0, 0), (label_width - 1, label_height - 1)],
                radius=border_radius,
                fill=bg_color
            )

            # テキストを描画
            text_x = padding[0]
            text_y = padding[1]
            label_draw.text((text_x, text_y), text, font=font, fill=text_color)

            # キャンバスに合成
            x, y = position
            self.canvas.paste(label_img, (x, y), label_img)

            return True

        except Exception as e:
            print(f"ラベル追加エラー: {e}")
            return False

    def add_gradient_overlay(
        self,
        direction: str = "bottom",
        color: str = "#000000",
        opacity: float = 0.5
    ) -> bool:
        """
        グラデーションオーバーレイを追加

        Args:
            direction: グラデーションの方向 ("top", "bottom", "left", "right")
            color: グラデーションの色
            opacity: 最大不透明度（0.0〜1.0）

        Returns:
            bool: 成功したかどうか
        """
        try:
            if self.canvas is None:
                self.create_canvas()

            # カラーをRGBに変換
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

            # グラデーション画像を作成
            gradient = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))

            for i in range(self.height if direction in ["top", "bottom"] else self.width):
                if direction == "bottom":
                    alpha = int(255 * opacity * (i / self.height))
                    y = i
                    for x in range(self.width):
                        gradient.putpixel((x, y), (r, g, b, alpha))
                elif direction == "top":
                    alpha = int(255 * opacity * (1 - i / self.height))
                    y = i
                    for x in range(self.width):
                        gradient.putpixel((x, y), (r, g, b, alpha))
                elif direction == "right":
                    alpha = int(255 * opacity * (i / self.width))
                    x = i
                    for y in range(self.height):
                        gradient.putpixel((x, y), (r, g, b, alpha))
                elif direction == "left":
                    alpha = int(255 * opacity * (1 - i / self.width))
                    x = i
                    for y in range(self.height):
                        gradient.putpixel((x, y), (r, g, b, alpha))

            self.canvas = Image.alpha_composite(self.canvas, gradient)
            return True

        except Exception as e:
            print(f"グラデーション追加エラー: {e}")
            return False

    def get_image(self) -> Optional[Image.Image]:
        """
        合成された画像を取得

        Returns:
            PIL.Image: 合成された画像、またはNone
        """
        return self.canvas

    def save(self, output_path: str, format: str = "PNG") -> bool:
        """
        画像を保存

        Args:
            output_path: 出力パス
            format: 出力形式 ("PNG", "JPEG")

        Returns:
            bool: 成功したかどうか
        """
        try:
            if self.canvas is None:
                return False

            if format.upper() == "JPEG":
                # JPEGの場合はRGBに変換
                rgb_image = self.canvas.convert("RGB")
                rgb_image.save(output_path, format="JPEG", quality=95)
            else:
                self.canvas.save(output_path, format="PNG")

            return True

        except Exception as e:
            print(f"保存エラー: {e}")
            return False
