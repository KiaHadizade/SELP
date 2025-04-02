🔹 1.
    Installing PyBullet
🔹 2.
    ✔ اگر می‌خوای GUI (رابط گرافیکی) برای شبیه‌سازی داشته باشی، Visual Studio C++ Build Tools رو نصب کن.
    ✔ می‌تونی اینو توی PowerShell اجرا کنی:
    `winget install Microsoft.VisualStudio.2022.BuildTools`
🔹 3.
    Run and test test_pyblt.py file to check if PyBullet currectly installed
🔹 4.
    Running first Simulation in PyBullet
    قبل از اینکه به LTL برسیم، اول باید یک محیط ساده در PyBullet راه‌اندازی کنیم. این یک زمین ساده + ربات رو لود می‌کنه.
    📌 اجرای یک شبیه‌سازی ساده با یک ربات URDF (مثلاً یک جعبه متحرک):
    Run frst_simulation.py
    ✅ بعد از اجرای این کد، یک ربات r2d2 رو روی زمین می‌بینی که شبیه‌سازی شده! 😃
🔹 5.
    حالا چطور LTL رو روی PyBullet اجرا کنیم؟

    📌 مرحله ۱: تعریف دستورات LTL برای ربات
    مثلاً می‌خوایم بگیم:
    "همیشه در محدوده بمان" → □ (stay_in_bounds)
    "بالاخره به نقطه هدف برس" → ◇ (GOAL)
    📌 پس اول باید نقاط محیط رو مشخص کنیم:
    `
        GOAL_POSITION = [2, 2]  # نقطه هدف در مختصات (x, y)
        BOUNDARY = 3  # محدوده حرکت ربات
    `

    📌 مرحله ۲: اضافه کردن کد کنترل LTL
    حالا باید ربات رو طوری حرکت بدیم که قوانین LTL رو رعایت کنه.
    📌 کد کنترل ربات بر اساس LTL:
    Run scnd_simulation.py
🔹 6.
    حالا این کد دقیقاً چیکار می‌کنه؟
    ✅ LTL رو بررسی می‌کنه:

    اگر از محدوده خارج شد، متوقف می‌شه (□ stay_in_bounds)

    اگر به نقطه هدف رسید، متوقف می‌شه (◇ GOAL)

    ✅ ربات رو در محیط حرکت می‌ده:

    حرکت تصادفی داره (فعلاً)

    در هر مرحله، بررسی می‌کنه که آیا باید متوقف بشه یا نه

    ✅ اجرای شبیه‌سازی در PyBullet:

    p.stepSimulation() → شبیه‌سازی یک قدم جلو می‌ره

    p.getBasePositionAndOrientation(robot_id) → موقعیت ربات رو می‌گیره

    p.resetBasePositionAndOrientation() → موقعیت جدید به ربات می‌ده