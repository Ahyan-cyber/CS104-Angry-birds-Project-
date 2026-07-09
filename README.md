# Angry Birds (Dual Play) 🐦💥

A 2-player competitive remake of *Angry Birds* built using **Pygame Community Edition (pygame-ce)** for the CS104 project (Spring 2024-25). Instead of fighting pigs, players face off against each other in a turn-based tactical battle to see who can collapse the opponent's fort first!

---

## 🎮 Game Concept & Rules
* **Dual Play:** Two players are provided with their own distinct set of birds and a unique fort of blocks.
* **Turn-Based Combat:** Players take alternate turns aiming and launching their birds.
* **Objective:** The first player to completely destroy the opponent's fort is declared the winner! 
* **Mechanics:** Drag the mouse pointer over your bird, pull back to adjust your launch velocity (up to a fixed limit), and release to fire.

---

## 🚀 Features & Mechanics

### 🧱 Destructible Blocks
The game implements three distinct types of blocks, each having a baseline of **300 hitpoints**, but varying vulnerabilities to specific bird classes:
* **Ice Blocks:** Extremely fragile against Blue birds.
* **Wood Blocks:** Vulnerable to Yellow birds.
* **Stone Blocks:** Vulnerable to Black birds.

### 🦅 Bird Classes & Damage Grid
Birds are randomly generated and distributed to both players. Choosing the right bird for the right block maximizes your destructive output:

| Bird Type | Specialization | Ice Damage | Wood Damage | Stone Damage |
| :--- | :--- | :---: | :---: | :---: |
| ❤️ **Red** | All-Rounder (The Hero) | 100 | 100 | 100 |
| 💛 **Yellow (Chuck)** | Wood Shatterer | 50 | **200** | 50 |
| 💙 **Blue** | Ice Breaker | **200** | 50 | 50 |
| 🖤 **Black (Bomb)** | Stone Buster | 50 | 50 | **200** |

### 🍏 Realistic Physics Engine
Built from scratch without heavy external physics libraries:
* **Gravity & Projectile Motion:** Simulated using an iterative method with a constant gravitational acceleration (`g`).
* **Elastic Collisions:** Features a custom `BOUNCE_DAMPENING` constant that realistically reduces and reverses bird velocity upon impacting surfaces.
* **Anti-Crowding:** Birds vanish immediately after their terminal block collision to keep the playing arena clear.

---

## 📁 Directory Structure
```text
├── resources/        # Sound effects, fonts, and external utilities
├── images/           # Cropped and scaled sprite sheets, backgrounds, and game UI assets
├── main.py           # Core entry point managing the main game loop, screens, and states
├── params.py         # Central configuration containing global variables and game constraints
├── bird.py           # Class definitions, unique damage attributes, and launch math for birds
└── block.py          # Class definitions, asset binding, and health tracking for forts
