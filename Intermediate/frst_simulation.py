import pybullet as p
import pybullet_data
import time

# راه‌اندازی شبیه‌ساز PyBullet
physicsClient = p.connect(p.GUI)  # باز کردن GUI
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # مسیر داده‌های PyBullet
p.setGravity(0, 0, -9.8)  # تنظیم گرانش

# بارگذاری زمین و یک جعبه متحرک
plane_id = p.loadURDF("plane.urdf")  
robot_id = p.loadURDF("r2d2.urdf", basePosition=[0, 0, 0.5])  # بارگذاری یک ربات

# اجرای شبیه‌ساز برای چند ثانیه
for _ in range(1000):
    p.stepSimulation()
    time.sleep(1./240.)

# پایان شبیه‌سازی
p.disconnect()
