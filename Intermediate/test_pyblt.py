import pybullet as p
import pybullet_data
import time

# ایجاد یک شبیه‌ساز و لود کردن زمین
physicsClient = p.connect(p.GUI)  # یا p.DIRECT برای اجرا بدون GUI
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # مسیر داده‌ها
p.loadURDF("plane.urdf")  # بارگذاری سطح زمین

# اجرای شبیه‌ساز برای چند ثانیه
for _ in range(1000):
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()
