import torch
import pybullet as p
import pybullet_data
import time
from train_model import RobotNN

model = RobotNN()
model.load_state_dict(torch.load("robot_model.pth"))
model.eval()

# راه‌اندازی PyBullet
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())  
p.setGravity(0, 0, -9.8)

# بارگذاری ربات
plane_id = p.loadURDF("plane.urdf")
robot_id = p.loadURDF("r2d2.urdf", basePosition=[0, 0, 0.5])

# اجرای کنترل ربات با مدل هوش مصنوعی
for i in range(500):
    pos, _ = p.getBasePositionAndOrientation(robot_id)
    vel = p.getBaseVelocity(robot_id)

    # آماده‌سازی داده برای مدل
    state = torch.tensor([[pos[0], pos[1], vel[0][0], vel[0][1], 0]], dtype=torch.float32)
    
    # پیش‌بینی حرکت بعدی با مدل
    action = model(state).detach().numpy().flatten()

    # اعمال حرکت به ربات
    new_pos = [pos[0] + action[0], pos[1] + action[1], pos[2]]
    p.resetBasePositionAndOrientation(robot_id, new_pos, [0, 0, 0, 1])

    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()
print("🚀 ربات با مدل یادگیری ماشینی حرکت کرد! 🎉")
