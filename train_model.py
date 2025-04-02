import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1️⃣ داده‌ها رو از CSV بخون
df = pd.read_csv("robot_data.csv")

# 2️⃣ ورودی‌ها و خروجی‌ها
X = df[["x", "y", "vx", "vy", "collision"]].values
y = df[["action_x", "action_y"]].values

# 3️⃣ نرمال‌سازی داده‌ها
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X = scaler_X.fit_transform(X)
y = scaler_y.fit_transform(y)

# 4️⃣ تقسیم داده‌ها به آموزش و تست
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5️⃣ تعریف مدل شبکه عصبی
class RobotNN(nn.Module):
    def __init__(self):
        super(RobotNN, self).__init__()
        self.fc1 = nn.Linear(5, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 6️⃣ ساخت مدل و تنظیمات
model = RobotNN()
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

# 7️⃣ تبدیل داده‌ها به Tensor
X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.float32)

# 8️⃣ آموزش مدل
for epoch in range(1000):
    optimizer.zero_grad()
    output = model(X_train_t)
    loss = criterion(output, y_train_t)
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"Epoch {epoch}: Loss = {loss.item()}")

# 9️⃣ ذخیره مدل آموزش‌دیده
torch.save(model.state_dict(), "robot_model.pth")
print("✅ مدل ذخیره شد! 🎉")
