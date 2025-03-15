import os
import time
import subprocess
from datetime import datetime

# 配置参数
TARGET_TIMES = ["07:00", "08:00", "21:00"]  # 目标下课时间列表（24小时制）
PROCESS_NAMES = ["SeewoWhiteboard.exe", "POWERPNT.EXE", "WINWORD.EXE"]  # 要关闭上课的的进程名
CHECK_INTERVAL = 30  # 检查间隔（秒）

def kill_process(process_name):
    """尝试结束指定进程"""
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", process_name],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"已成功结束进程：{process_name}")
    except subprocess.CalledProcessError:
        print(f"未找到进程：{process_name} 或结束失败")

def should_trigger():
    """检查当前时间是否在目标时间列表中"""
    current_time = datetime.now().strftime("%H:%M")
    return current_time in TARGET_TIMES

def main():
    last_trigger_time = None
    print("自动关闭程序已启动...")
    print(f"监控时间点：{TARGET_TIMES}")
    print(f"监控进程：{PROCESS_NAMES}")
    
    while True:
        try:
            current_time = datetime.now().strftime("%H:%M")
            
            if should_trigger() and current_time != last_trigger_time:
                print(f"\n触发时间 {current_time}，开始结束进程...")
                for process in PROCESS_NAMES:
                    kill_process(process)
                last_trigger_time = current_time
                print("处理完成，等待下一个时间点...")
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n程序已手动退出")
            break

if __name__ == "__main__":
    # 请求管理员权限（仅限Windows）
    try:
        import ctypes
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            print("请以管理员身份运行此脚本！")
            time.sleep(5)
            exit()
    except:
        pass
    
    main()