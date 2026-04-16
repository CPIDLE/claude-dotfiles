## Sample 141

**Source**: `HaloScan_v0\docs\03_感測器融合提案.md` L187

```
4x 魚眼相機（USB3）
│
├─ 魚眼影像前處理（去畸變 / 等距投影正規化）
│
├─ 語意分割推論（YOLOv8-seg / ERFNet）
│  輸出：每個 pixel 的類別標籤
│  類別：人員 / AGV / 台車 / 物料 / FOUP / 地板 / 牆壁 / 未知
│
├─ 3D 投影匹配
│  LiDAR 點雲 --> 座標轉換 --> 投影至魚眼影像平面
│  每個 3D 點獲得對應的語意標籤
│
├─ 標記融合
│  將語意標記的 3D 點雲與 CropBox 安全區交叉比對
│  輸出：安全區內物件的類別資訊
│
└─ 發佈 ROS Topic
   /perception/labeled_objects  (custom msg: 類別 + 位置 + 信心度)
   /perception/fisheye_images   (sensor_msgs/CompressedImage, 事件觸發時記錄)
```

