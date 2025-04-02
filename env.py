import gym
import pybullet as p
import pybullet_data
import numpy as np
from gym import spaces

class RobotEnv(gym.Env):
    def __init__(self):
        super(RobotEnv, self).__init__()

        # راه‌اندازی PyBullet
        self.physicsClient = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)

        # بارگذاری زمین و ربات
        self.plane_id = p.loadURDF("plane.urdf")
        self.robot_id = p.loadURDF("r2d2.urdf", basePosition=[0, 0, 0.5])

        # لیست موانع
        self.obstacles = []
        self._create_obstacles()

        # موقعیت هدف
        self.GOAL_POSITION = np.array([2, 2])
        self.BOUNDARY = 3

        # تعریف فضای اکشن و وضعیت
        self.action_space = spaces.Box(low=-0.1, high=0.1, shape=(2,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-self.BOUNDARY, high=self.BOUNDARY, shape=(2,), dtype=np.float32)

    def _create_obstacles(self):
        """اضافه کردن موانع در محیط"""
        positions = [[1, 1, 0.1], [-1, -1, 0.1], [0.5, -0.5, 0.1]]
        for pos in positions:
            obstacle_id = p.loadURDF("cube_small.urdf", basePosition=pos)
            self.obstacles.append(obstacle_id)

    def reset(self):
        """ریست کردن محیط"""
        p.resetBasePositionAndOrientation(self.robot_id, [0, 0, 0.5], [0, 0, 0, 1])
        return np.array([0, 0], dtype=np.float32)

    def step(self, action):
        """اجرای حرکت و بررسی برخورد با موانع"""
        pos, _ = p.getBasePositionAndOrientation(self.robot_id)
        new_pos = np.array([pos[0] + action[0], pos[1] + action[1]])

        # بررسی خروج از محدوده
        if not (-self.BOUNDARY <= new_pos[0] <= self.BOUNDARY and -self.BOUNDARY <= new_pos[1] <= self.BOUNDARY):
            return new_pos, -10, True, {}

        # حرکت ربات
        p.resetBasePositionAndOrientation(self.robot_id, [new_pos[0], new_pos[1], 0.5], [0, 0, 0, 1])

        # بررسی برخورد با موانع
        for obs in self.obstacles:
            obs_pos, _ = p.getBasePositionAndOrientation(obs)
            if np.linalg.norm(new_pos - np.array(obs_pos[:2])) < 0.2:
                return new_pos, -50, True, {}  # جریمه سنگین برای برخورد

        # بررسی رسیدن به هدف
        done = np.linalg.norm(new_pos - self.GOAL_POSITION) < 0.2
        reward = 100 if done else -1  # رسیدن به هدف = پاداش

        return new_pos, reward, done, {}

    def render(self, mode="human"):
        """اجرای شبیه‌ساز در GUI"""
        p.disconnect()
        self.physicsClient = p.connect(p.GUI)
