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
        "--demo",
        default=False,
        action="store_true",
        help="演示模式（不需要 ADB 设备）",
    )
    parser.add_argument(
        "--server",
        help="服务端设备 ID（用于监听语音）",
    )
    parser.add_argument(
        "--client",
        help="客户端设备 ID（用于拍照）",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("🎲 魔方对话服务")
    print("=" * 60)

    if args.demo:
        print("📍 模式: 演示模式")
        service = ChatService()
        service.demo_mode()
    else:
        print(f"📍 服务端设备: {args.server}")
        print(f"📍 客户端设备: {args.client}")
        print("=" * 60)

        adb = AdbHelper(
            server_device=args.server,
            client_device=args.client,
        )
        service = ChatService(adb_helper=adb)
        service.start()


if __name__ == "__main__":
    main()
