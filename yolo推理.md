vision:
  mob_detector: yolo
  yolo_model: weights/best.pt
  yolo_confidence: 0.6


训练完成！ONNX CPU 推理 52.6ms/帧，远低于 125ms 预算，AMD 游戏机完全够用。

  结果汇总

  ┌───────────────┬─────────────────────────────────────────────┐
  │     项目      │                     值                      │
  ├───────────────┼─────────────────────────────────────────────┤
  │ 模型          │ yolo11n (单类: mob)                         │
  ├───────────────┼─────────────────────────────────────────────┤
  │ 训练数据      │ 588 张合成图（61 种精灵图）                 │
  ├───────────────┼─────────────────────────────────────────────┤
  │ ONNX 推理速度 │ 52.6ms/帧（CPU，预算 125ms）                │
  ├───────────────┼─────────────────────────────────────────────┤
  │ 模型文件      │ runs/mobs/mobs6/weights/best.onnx (10.2 MB) │
  └───────────────┴─────────────────────────────────────────────┘

  部署到 AMD 游戏机步骤

  游戏机上执行：

  # 1. 装 ONNX Runtime（不需要 torch）
  pip install onnxruntime

  # 2. 复制模型文件
  # 从这台电脑复制 best.onnx 到游戏机 maplebot 项目下
  3. 修改 config/local.yaml：

  vision:
    mob_detector: yolo
    yolo_model: runs/mobs/mobs6/weights/best.onnx
    yolo_confidence: 0.5

  4. 验证：

  python tools/debug_view.py --snapshot check.png

  主要优势：
  - 不再把宠物当怪（训练集里没有宠物）
  - CPU 推理 52ms，比描边检测更稳定
  - 换地图只要精灵图重新训练即可

  需要我把 best.onnx 复制到某个位置，或者帮你写一个给 AMD 游戏机的部署说明 bat 文件吗？
