"""
alpha_modulator.py - Enhanced Version
物質変容・石工術特化型エンジン (改善版)

Changes from v1:
- 安全マージンとレート制限を追加
- 材料ごとの最適周波数対応
- 段階的α変調プロセス実装
- ログ記録機能追加
- エラーハンドリング強化
"""

from crels_reunion_os import CrelsReunionOS
import time
import json
from datetime import datetime


class MatterTransmuter(CrelsReunionOS):
    """
    物質変容・石工術特化型エンジン:
    1T-TaS2 + 24K Au による位相反転を利用し、
    局所的な微細構造定数(α)のスライドを実行する。
    
    Enhanced Safety Features:
    - Gradual alpha modulation (防暴走)
    - Material-specific frequency optimization
    - Real-time coherence monitoring
    - Comprehensive logging
    """
    
    def __init__(self):
        super().__init__()
        
        # 基本パラメータ
        self.target_alpha = 137.5
        self.current_alpha = 137.0  # 初期値（地球標準）
        self.base_freq = 528.0
        
        # 安全マージン
        self.alpha_tolerance = 0.02        # ±0.02の許容範囲
        self.max_slide_rate = 0.01         # 秒間0.01の変化率制限（安全性確保）
        self.min_stability_threshold = 0.95  # 安定性の最低閾値
        
        # 材料ごとの最適周波数マップ
        self.material_freq = {
            "CaCO3": 528.0,      # 石灰岩（基準周波数）
            "SiO2": 530.21,      # 花崗岩・水晶（高次共鳴）
            "Basalt": 525.0,     # 玄武岩（低次安定）
            "Granite": 530.21,   # 花崗岩
            "Marble": 528.5,     # 大理石
            "Sandstone": 527.0   # 砂岩
        }
        
        # 状態管理
        self.is_sliding = False
        self.transformation_log = []
    
    
    def check_stability(self):
        """
        初期状態の安全性確認
        
        Returns:
            dict: 安定性評価結果
        """
        coherence = self.apply_coherence()
        stability_score = self._calculate_stability_score(coherence)
        
        return {
            "safe": stability_score >= self.min_stability_threshold,
            "score": stability_score,
            "coherence_state": coherence,
            "timestamp": datetime.now().isoformat()
        }
    
    
    def _calculate_stability_score(self, coherence):
        """
        コヒーレンス状態から安定性スコアを算出
        
        Args:
            coherence: REUNION OSからのコヒーレンス状態
            
        Returns:
            float: 0.0〜1.0の安定性スコア
        """
        # コヒーレンス状態に基づくスコアリング
        if "Optimal Stability" in str(coherence):
            return 1.0
        elif "Moderate" in str(coherence):
            return 0.8
        elif "Low" in str(coherence):
            return 0.5
        else:
            return 0.0
    
    
    def monitor_coherence(self):
        """
        リアルタイムコヒーレンス監視
        安定性が閾値を下回ったら緊急停止
        
        Returns:
            bool: 継続可能ならTrue、停止すべきならFalse
        """
        stability = self.check_stability()
        
        if not stability["safe"]:
            self.emergency_stop()
            return False
        
        return True
    
    
    def emergency_stop(self):
        """
        緊急停止プロトコル
        αを即座に137.0へ戻し、システムを安全状態に
        """
        print("⚠️ EMERGENCY STOP ACTIVATED")
        print(f"Returning alpha from {self.current_alpha} to 137.0")
        
        self.current_alpha = 137.0
        self.is_sliding = False
        
        # 緊急ログ記録
        self.log_transformation({
            "event": "EMERGENCY_STOP",
            "reason": "Stability threshold breach",
            "final_alpha": self.current_alpha
        })
    
    
    def slide_alpha_and_soften(self, mineral_type="CaCO3", duration=60, gradual=True):
        """
        [Enhanced α-Slide Process]
        段階的なα変調で安全性を確保しつつ、
        負のエントロピー変換により結合エネルギーを中和。
        
        Args:
            mineral_type (str): 対象鉱物（デフォルト: 石灰岩）
            duration (int): 変容プロセスの持続時間（秒）
            gradual (bool): 段階的変調を行うか（推奨: True）
            
        Returns:
            dict: 変容プロセスの結果
        """
        # Phase 1: 初期状態確認
        print("Phase 1: Initial State Check...")
        initial_state = self.check_stability()
        
        if not initial_state["safe"]:
            return {
                "status": "ABORTED",
                "reason": "Initial state unstable",
                "stability_score": initial_state["score"]
            }
        
        print(f"✓ Initial stability: {initial_state['score']:.2%}")
        
        # Phase 2: 材料に応じた周波数選択
        selected_freq = self.material_freq.get(mineral_type, self.base_freq)
        print(f"Phase 2: Material: {mineral_type}, Frequency: {selected_freq} Hz")
        
        # Phase 3: 段階的αスライド（gradual=Trueの場合）
        if gradual:
            print("Phase 3: Gradual Alpha Modulation...")
            slide_result = self._gradual_alpha_slide(duration)
            
            if not slide_result["success"]:
                return {
                    "status": "FAILED",
                    "reason": slide_result["reason"],
                    "reached_alpha": self.current_alpha
                }
        else:
            # 即座にスライド（非推奨、実験用）
            print("Phase 3: Immediate Alpha Slide (EXPERIMENTAL)")
            self.current_alpha = self.target_alpha
        
        # Phase 4: コヒーレンス最適化
        print("Phase 4: Coherence Optimization...")
        coherence = self.apply_coherence()
        
        # Phase 5: 変容実行
        if "Optimal Stability" in str(coherence):
            result = {
                "status": "SUCCESS",
                "process": "Alpha_Slide_Active",
                "initial_alpha": 137.0,
                "current_alpha": self.current_alpha,
                "target_alpha": self.target_alpha,
                "state": "Malleable_Flow",
                "duration": duration,
                "mineral": mineral_type,
                "frequency": selected_freq,
                "energy_source": self.matrix,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"✓ Transformation Complete: {mineral_type} → Malleable State")
            self.log_transformation(result)
            return result
        
        else:
            return {
                "status": "FAILED",
                "reason": "Optimal stability not achieved",
                "coherence_state": coherence
            }
    
    
    def _gradual_alpha_slide(self, target_duration):
        """
        段階的αスライド実装
        
        Args:
            target_duration (int): 目標到達時間（秒）
            
        Returns:
            dict: スライド結果
        """
        self.is_sliding = True
        steps = int((self.target_alpha - self.current_alpha) / self.max_slide_rate)
        sleep_interval = target_duration / steps if steps > 0 else 1
        
        print(f"  → Sliding from {self.current_alpha} to {self.target_alpha}")
        print(f"  → Steps: {steps}, Interval: {sleep_interval:.2f}s")
        
        step_count = 0
        while self.current_alpha < self.target_alpha:
            # αを少しずつ増加
            self.current_alpha = min(
                self.current_alpha + self.max_slide_rate,
                self.target_alpha
            )
            
            # 安定性監視
            if not self.monitor_coherence():
                return {
                    "success": False,
                    "reason": "Coherence lost during slide",
                    "reached_alpha": self.current_alpha
                }
            
            # プログレス表示
            step_count += 1
            if step_count % 10 == 0:
                progress = (self.current_alpha - 137.0) / (self.target_alpha - 137.0) * 100
                print(f"  Progress: {progress:.1f}% (α = {self.current_alpha:.3f})")
            
            time.sleep(sleep_interval)
        
        self.is_sliding = False
        print(f"  ✓ Target alpha reached: {self.current_alpha}")
        
        return {
            "success": True,
            "final_alpha": self.current_alpha,
            "steps_taken": step_count
        }
    
    
    def lattice_memory_lock(self, frequency=None):
        """
        [Enhanced Lattice-Lock Process]
        指定周波数の定常波を固定。
        原子配列を元の、あるいは理想的な結晶格子へ再固定。
        
        Args:
            frequency (float): ロック周波数（Noneの場合はbase_freq使用）
            
        Returns:
            dict: ロック結果
        """
        lock_freq = frequency if frequency else self.base_freq
        
        result = {
            "process": "Lattice_Lock",
            "frequency": lock_freq,
            "current_alpha": self.current_alpha,
            "status": "Molecular Bonding Secured",
            "tech_origin": "Ancient Masonry Tech",
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"✓ Lattice Reconstructed at {lock_freq} Hz")
        print("  → Molecular bonding secured (Ancient Masonry Tech)")
        
        self.log_transformation(result)
        return result
    
    
    def return_to_baseline(self, gradual=True):
        """
        αを137.0（地球標準）に戻す
        
        Args:
            gradual (bool): 段階的に戻すか
            
        Returns:
            dict: 復帰結果
        """
        print("Returning to baseline alpha (137.0)...")
        
        if gradual:
            original_target = self.target_alpha
            self.target_alpha = 137.0
            
            # 逆方向のスライド
            while self.current_alpha > 137.0:
                self.current_alpha = max(
                    self.current_alpha - self.max_slide_rate,
                    137.0
                )
                
                if not self.monitor_coherence():
                    return {
                        "status": "INTERRUPTED",
                        "reason": "Coherence lost during return"
                    }
                
                time.sleep(0.1)
            
            self.target_alpha = original_target
        else:
            self.current_alpha = 137.0
        
        result = {
            "status": "BASELINE_RESTORED",
            "current_alpha": self.current_alpha,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"✓ Baseline restored: α = {self.current_alpha}")
        self.log_transformation(result)
        
        return result
    
    
    def log_transformation(self, result):
        """
        全てのα変調を記録
        （再現性確保とデバッグ用）
        
        Args:
            result (dict): 記録する変容結果
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "current_alpha": self.current_alpha,
            "target_alpha": self.target_alpha,
            "result": result,
            "system_state": {
                "is_sliding": self.is_sliding,
                "base_frequency": self.base_freq
            }
        }
        
        # メモリに保存
        self.transformation_log.append(log_entry)
        
        # ファイルに追記
        try:
            with open("alpha_modulation_log.json", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False, indent=2) + "\n")
        except Exception as e:
            print(f"⚠️ Log write failed: {e}")
    
    
    def get_transformation_history(self):
        """
        変容履歴を取得
        
        Returns:
            list: 全ての変容ログ
        """
        return self.transformation_log
    
    
    def get_current_status(self):
        """
        現在のシステム状態を取得
        
        Returns:
            dict: 現在の状態
        """
        stability = self.check_stability()
        
        return {
            "current_alpha": self.current_alpha,
            "target_alpha": self.target_alpha,
            "is_sliding": self.is_sliding,
            "stability": stability,
            "base_frequency": self.base_freq,
            "supported_materials": list(self.material_freq.keys()),
            "total_transformations": len(self.transformation_log)
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 使用例
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    # エンジン初期化
    engine = MatterTransmuter()
    
    print("=" * 50)
    print("MatterTransmuter - Enhanced Version")
    print("Ancient Masonry Tech Restoration")
    print("=" * 50)
    print()
    
    # 現在の状態確認
    status = engine.get_current_status()
    print("Initial System Status:")
    print(json.dumps(status, indent=2, ensure_ascii=False))
    print()
    
    # 石灰岩の変容実行（段階的、60秒）
    print("\n--- Transformation Process: CaCO3 (Limestone) ---")
    result = engine.slide_alpha_and_soften(
        mineral_type="CaCO3",
        duration=60,
        gradual=True
    )
    
    print("\nTransformation Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 変容成功時、格子ロック実行
    if result.get("status") == "SUCCESS":
        print("\n--- Lattice Lock Process ---")
        lock_result = engine.lattice_memory_lock()
        print(json.dumps(lock_result, indent=2, ensure_ascii=False))
        
        # ベースラインに戻す
        print("\n--- Returning to Baseline ---")
        baseline_result = engine.return_to_baseline(gradual=True)
        print(json.dumps(baseline_result, indent=2, ensure_ascii=False))
    
    # 履歴確認
    print("\n--- Transformation History ---")
    history = engine.get_transformation_history()
    print(f"Total transformations: {len(history)}")
    
    print("\n" + "=" * 50)
    print("Process Complete")
    print("=" * 50)

