import pybullet as p
import pybullet_data
import time
import numpy as np

# راه‌اندازی PyBullet
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())  
p.setGravity(0, 0, -9.8)

# بارگذاری زمین و ربات
plane_id = p.loadURDF("plane.urdf")
robot_id = p.loadURDF("r2d2.urdf", basePosition=[0, 0, 0.5])

# نقاط کلیدی
GOAL_POSITION = np.array([2, 2])  # نقطه هدف
BOUNDARY = 3  # محدوده مجاز برای حرکت

# تابع بررسی LTL: آیا در محدوده هست؟
def check_bounds(position):
    x, y, _ = position
    return -BOUNDARY <= x <= BOUNDARY and -BOUNDARY <= y <= BOUNDARY

# تابع بررسی LTL: آیا به هدف رسیدیم؟
def check_goal(position):
    return np.linalg.norm(position[:2] - GOAL_POSITION) < 0.2

# حلقه اصلی شبیه‌سازی
for _ in range(1000):
    pos, _ = p.getBasePositionAndOrientation(robot_id)  # موقعیت ربات
    
    # بررسی قوانین LTL
    if not check_bounds(pos):
        print("🚨 خارج از محدوده!")
        break
    if check_goal(pos):
        print("🎯 به هدف رسیدیم!")
        break

    # حرکت تصادفی (فعلاً)
    action = np.random.uniform(-0.1, 0.1, 2)
    new_pos = [pos[0] + action[0], pos[1] + action[1], pos[2]]
    p.resetBasePositionAndOrientation(robot_id, new_pos, [0, 0, 0, 1])
    
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()
