## Sample 646

**Source**: `UR_Program_Analysis_v0\docs\PHASE2_SPEC.md` L526

```python
# ── 常數 ──
UR30_DH_PARAMS: list[dict]  # [{"a": float, "d": float, "alpha": float}, ...]

# ── 正向運動學 ──
def forward_kinematics(
    joints: list[float],
    dh_params: list[dict] | None = None
) -> list[float]:
    """由關節角度計算末端姿態。
    
    Args:
        joints: [j1, j2, j3, j4, j5, j6]（弧度）
        dh_params: 可選 DH 參數覆蓋，None 使用 UR30 預設
    Returns:
        [x, y, z, rx, ry, rz]（公尺, 弧度 — axis-angle 表示法）
    """

def forward_kinematics_matrix(
    joints: list[float],
    dh_params: list[dict] | None = None
) -> 'numpy.ndarray':
    """由關節角度計算 4x4 齊次變換矩陣。
    
    Returns:
        4x4 numpy array
    """

# ── 逆向運動學 ──
def inverse_kinematics(
    pose: list[float],
    q_near: list[float] | None = None,
    dh_params: list[dict] | None = None
) -> list[list[float]]:
    """由末端姿態計算關節角度（最多 8 組解）。
    
    Args:
        pose: [x, y, z, rx, ry, rz]（公尺, axis-angle 弧度）
        q_near: 偏好解（選最接近此組的解），None 則回傳所有解
        dh_params: 可選 DH 參數覆蓋
    Returns:
        關節角度解的列表，每個解為 [j1..j6]
        如果 q_near 有值，只回傳最接近的一組（list 長度 1）
    """

# ── 工具函式 ──
def pose_to_matrix(pose: list[float]) -> 'numpy.ndarray':
    """axis-angle pose → 4x4 齊次矩陣。"""

def matrix_to_pose(matrix: 'numpy.ndarray') -> list[float]:
    """4x4 齊次矩陣 → axis-angle pose。"""

def rotation_vector_to_matrix(rvec: list[float]) -> 'numpy.ndarray':
    """axis-angle [rx, ry, rz] → 3x3 旋轉矩陣（Rodrigues 公式）。"""

def matrix_to_rotation_vector(R: 'numpy.ndarray') -> list[float]:
    """3x3 旋轉矩陣 → axis-angle [rx, ry, rz]。"""

# ── 驗證函式 ──
def validate_waypoint(
    waypoint: 'URWaypoint',
    tolerance_mm: float = 1.0,
    tolerance_deg: float = 1.0
) -> dict:
    """驗證一個 waypoint 的 pose 和 joints 是否一致。
    
    用 FK(joints) 計算出 pose，與宣告的 pose 比較。
    
    Args:
        waypoint: URWaypoint 物件
        tolerance_mm: 位置容差（毫米）
        tolerance_deg: 角度容差（度）
    Returns:
        {
            "name": str,
            "valid": bool,
            "position_error_mm": float,
            "orientation_error_deg": float,
            "fk_pose": list[float],    # FK 計算的 pose
            "declared_pose": list[float],  # 宣告的 pose
            "details": str  # 人類可讀的描述
        }
    """

def validate_all_waypoints(
    project: 'URProject',
    tolerance_mm: float = 1.0,
    tolerance_deg: float = 1.0
) -> list[dict]:
    """驗證專案中所有 waypoint。
    
    Returns:
        驗證結果列表（同 validate_waypoint 的 return 格式）
        只包含有 pose 和 joints 都有值的 waypoint
    """

def generate_validation_report(results: list[dict]) -> str:
    """產生 Markdown 格式的驗證報告。
    
    報告結構：
    ## Waypoint FK/IK 驗證報告
    - 統計：總數 / 通過 / 失敗 / 跳過（缺 pose 或 joints）
    - 失敗清單（表格：名稱、位置誤差、角度誤差、來源檔案）
    - 通過清單（摘要）
    """
```

