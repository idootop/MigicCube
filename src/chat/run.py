#!/usr/bin/env python3

"""
魔方对话服务入口
"""

import argparse
import os
import sys

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat import ChatService
from chat.adb import AdbHelper


def main():
    parser = argparse.ArgumentParser(description="魔方对话服务")
    parser.add_argument(
        "--server",
        help="服务端设备 ID（用于监听语音指令）",
    )
    parser.add_argument(
        "--client",
        help="客户端设备 ID（用于拍照）",
    )
    parser.add_argument(
        "--tts",
        help="TTS 接口地址，比如 http://192.168.31.125:8080/tts.wav",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("🎲 魔方对话服务")
    print("=" * 60)

    print(f"📍 服务端设备: {args.server}")
    print(f"📍 客户端设备: {args.client}")
    print(f"📍 TTS 接口地址: {args.tts}")
    print("=" * 60)

    adb = AdbHelper(
        server_device=args.server,
        client_device=args.client,
        tts_api=args.tts,
    )

    service = ChatService(adb_helper=adb)
    service.start()


if __name__ == "__main__":
    main()
