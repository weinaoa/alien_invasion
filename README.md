
# 飞机射击外星人小游戏

这是一个用 **Python** 编写的经典 2D 飞机射击外星人小游戏，玩家可以操纵自己的战机在屏幕底部移动，并发射子弹消灭不断入侵的外星人。游戏画面简洁，逻辑清晰，非常适合初学者练习 Python 和 Pygame 游戏开发。

## 🛠 开发环境

- **语言**: Python 3
- **依赖库**:
  - [pygame]
- **操作系统**: Windows 

### 安装依赖

```bash
pip install pygame
```

### 运行游戏

```bash
python main.py
```

## 🎮 游戏玩法

- 玩家通过 **左右方向键** 控制飞机移动
- 按 **空格键** 发射子弹
- 子弹击中外星人时，外星人被消灭并获得积分
- 外星人会逐渐下移，若有外星人到达屏幕底部，游戏结束
- 随着游戏进行，外星人数量和移动速度会逐渐增加，挑战难度升级

## 📁 项目结构

```
alien_invasion_game/
│
├── main.py             # 游戏主程序入口
├── settings.py         # 游戏配置参数（窗口大小、颜色、速度等）
├── ship.py             # 玩家飞机类
├── bullet.py           # 子弹类
├── alien.py            # 外星人类
├── game_stats.py       # 记录分数和游戏状态
├── images/             # 存放飞机和外星人图片
│   ├── ship.png
│   ├── alien.png
│
└── README.md           # 项目介绍文档
```

## 🖼 游戏截图

![游戏截图](images/screenshot.png)

## ✨ 功能亮点

- 基于 **Pygame** 框架，代码简洁易读
- 多个外星人阵列的生成与移动逻辑
- 飞机碰撞检测与游戏结束机制
- 支持分数统计和关卡递增

## 🚀 后续可扩展功能

- 增加音效和背景音乐
- 支持不同类型的敌人和道具
- 加入主菜单、暂停、关卡选择等界面
- 支持排行榜和多玩家模式

## 📚 学习参考

本项目参考了 Python 入门经典教程《Python编程：从入门到实践》中“外星人入侵”项目，并进行了优化与扩展，适合学习 Python 游戏开发基础。

---
