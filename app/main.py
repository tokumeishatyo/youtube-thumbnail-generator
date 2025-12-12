# -*- coding: utf-8 -*-
"""
YouTubeサムネイル生成ツール
メインエントリーポイント
"""

import os
import sys

# アプリケーションのルートパスを設定
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_ROOT)

from ui.main_window import MainWindow


def main():
    """メイン関数"""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
