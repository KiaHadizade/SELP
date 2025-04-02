import pybullet as p
import pybullet_data
import numpy as np
import time
import csv

# راه‌اندازی PyBullet
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())  
p.setGravity(0, 0, -9.8)

# بارگذاری زمین و ربات
plane_id = p.loadURDF("plane.urdf")
robot_id = p.loadURDF("r2d2.urdf", basePosition=[0, 0, 0.5])

# اضافه کردن موانع
obstacles = []
positions = [[1, 1, 0.1], [-1, -1, 0.1], [0.5, -0.5, 0.1]]
for pos in positions:
    obstacle_id = p.loadURDF("cube_small.urdf", basePosition=pos)
    obstacles.append(obstacle_id)

# متغیرهای ذخیره داده‌ها
data = []
header = ["time", "x", "y", "z", "vx", "vy", "vz", "ax", "ay", "az", "collision", "action_x", "action_y"]

# زمان شروع
start_time = time.time()

# حلقه شبیه‌سازی
for i in range(1000):
    current_time = time.time() - start_time  # زمان نسبی
    
    # گرفتن موقعیت و سرعت ربات
    pos, _ = p.getBasePositionAndOrientation(robot_id)
    vel = p.getBaseVelocity(robot_id)

    # تولید یک حرکت تصادفی
    action = np.random.uniform(-0.1, 0.1, 2)
    new_pos = [pos[0] + action[0], pos[1] + action[1], pos[2]]
    p.resetBasePositionAndOrientation(robot_id, new_pos, [0, 0, 0, 1])

    # بررسی برخورد با موانع
    collision = 0
    for obs in obstacles:
        obs_pos, _ = p.getBasePositionAndOrientation(obs)
        if np.linalg.norm(new_pos[:2] - np.array(obs_pos[:2])) < 0.2:
            collision = 1
            break

    # محاسبه شتاب (تقریباً)
    acc = [(vel[0][0] - action[0]), (vel[0][1] - action[1]), vel[0][2]]

    # ذخیره داده‌ها
    data.append([current_time, pos[0], pos[1], pos[2], vel[0][0], vel[0][1], vel[0][2], acc[0], acc[1], acc[2], collision, action[0], action[1]])

    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()

# ذخیره داده‌ها در فایل CSV
with open("robot_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

print("✅ داده‌های شبیه‌سازی در فایل robot_data.csv ذخیره شد! 🎉")
