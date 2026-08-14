"""怪物偵測即時預覽：抓指定視窗畫面，用訓練好的 YOLO 模型偵測怪物，
把框與置信度疊在畫面上，終端同步印出每隻怪的座標與匹配度。

用途：快速驗證一個訓練好的模型在真實遊戲畫面上的偵測效果，
不跑整條 capture→perceive→decide→execute 管道，只看偵測這一層。

用法：
  # 用 config/default.yaml 的視窗標題與模型路徑
  python tools/detect_mobs.py

  # 指定模型（.pt 或 .onnx）
  python tools/detect_mobs.py --model runs/mobs/mobs6/weights/best.onnx

  # 指定視窗標題（子字串比對，不分大小寫）
  python tools/detect_mobs.py --title "新楓之谷"

  # 只存一張標註圖，不開視窗（適合截圖離線看）
  python tools/detect_mobs.py --snapshot out.png

按 q 離開。
"""
import argparse
import os
import sys
import time

import cv2

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maplebot.capture import WindowCapture  # noqa: E402
from maplebot.config import load_config  # noqa: E402
from maplebot.vision.mobs import Mob  # noqa: E402
from maplebot.vision.yolo_mobs import YoloMobDetector  # noqa: E402

WINDOW = "maplebot detect (q to quit)"
MAX_DISPLAY_W = 1280


def _draw_mobs(frame, mobs):
    """把每隻怪畫成黃框 + 中心十字 + 置信度文字。回傳標註後的畫面。"""
    for mob in mobs:
        x1 = mob.cx - mob.w // 2
        y1 = mob.cy - mob.h // 2
        x2 = mob.cx + mob.w // 2
        y2 = mob.cy + mob.h // 2
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.drawMarker(frame, (mob.cx, mob.cy), (0, 0, 255),
                       cv2.MARKER_CROSS, 18, 2)
        label = f"{mob.name} {mob.score:.2f}"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 255, 255), -1)
        cv2.putText(frame, label, (x1 + 2, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
    return frame


def _report(mobs):
    """終端印出這一幀的偵測摘要。"""
    print(f"偵測到 {len(mobs)} 個怪物")
    for i, mob in enumerate(mobs):
        print(f"  [{i + 1}] {mob.name} ({mob.cx},{mob.cy}) "
              f"{mob.w}x{mob.h} 匹配度 {mob.score:.3f}")


def main() -> int:
    ap = argparse.ArgumentParser(description="YOLO 怪物偵測即時預覽")
    ap.add_argument("--config", default="config/default.yaml")
    ap.add_argument("--title", default="",
                    help="視窗標題子字串；留空則用 config 的 window.title")
    ap.add_argument("--model", default="",
                    help="YOLO 模型路徑(.pt/.onnx)；留空則用 config 的 yolo_model")
    ap.add_argument("--confidence", type=float, default=None,
                    help="信心門檻；留空則用 config 的 yolo_confidence")
    ap.add_argument("--imgsz", type=int, default=None,
                    help="推理解析度；留空用模型預設")
    ap.add_argument("--device", default="", help="推理裝置(0/cpu)；留空自動")
    ap.add_argument("--snapshot", default="",
                    help="只抓一幀存成標註圖後結束，不開視窗")
    args = ap.parse_args()

    cfg = load_config(args.config)
    title = args.title or cfg.window_title
    model = args.model or cfg.vision.get("yolo_model", "")
    confidence = args.confidence if args.confidence is not None \
        else cfg.vision.get("yolo_confidence", 0.5)
    imgsz = args.imgsz or cfg.vision.get("yolo_imgsz") or None

    if not model:
        print("錯誤：未指定模型。請用 --model 指定 .pt 或 .onnx，"
              "或在 config/local.yaml 設定 vision.yolo_model")
        return 2

    print(f"視窗標題: {title}")
    print(f"模型: {model}")
    print(f"信心門檻: {confidence}")
    cap = WindowCapture(title, cfg.capture_method)
    print(f"擷取尺寸: {cap.size[0]}x{cap.size[1]}｜擷取方式: {cap.method}")
    if cap.method == "screen":
        print("[!] 此客戶端不支援 PrintWindow，改用螢幕擷取："
              "任何蓋住遊戲的視窗都會被拍進去")

    detector = YoloMobDetector(model, confidence=confidence,
                               device=args.device, imgsz=imgsz)
    print(f"偵測器: {detector.explain()}")
    print("按 q 離開\n")

    if args.snapshot:
        frame = cap.grab()
        mobs = detector.detect(frame)
        annotated = _draw_mobs(frame.copy(), mobs)
        cv2.imwrite(args.snapshot, annotated)
        print(f"已存標註圖: {args.snapshot}")
        _report(mobs)
        return 0

    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
    disp_w = min(cap.size[0], MAX_DISPLAY_W)
    scale = disp_w / cap.size[0]
    disp_h = int(cap.size[1] * scale)
    cv2.resizeWindow(WINDOW, disp_w, disp_h)

    fps_n, fps_t0 = 0, 0.0
    while True:
        t0 = time.monotonic()
        frame = cap.grab()
        mobs = detector.detect(frame)
        annotated = _draw_mobs(frame.copy(), mobs)

        dt = time.monotonic() - t0
        fps = 1.0 / max(dt, 1e-6)
        cv2.putText(annotated, f"{fps:.1f} FPS | {len(mobs)} mobs",
                    (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 0), 2, cv2.LINE_AA)

        shown = annotated if annotated.shape[1] <= disp_w else \
            cv2.resize(annotated, (disp_w, disp_h))
        cv2.imshow(WINDOW, shown)

        if time.monotonic() - fps_t0 >= 0.5:
            _report(mobs)
            fps_t0 = time.monotonic()
        fps_n += 1

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break
        if cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) < 1:
            break
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    sys.exit(main())
