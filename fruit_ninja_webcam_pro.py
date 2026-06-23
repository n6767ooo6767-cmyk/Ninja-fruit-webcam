import cv2
import numpy as np
import random
import math
import time
import json
from pathlib import Path

WIDTH = 960
HEIGHT = 720

CONFIG_FILE = Path("purple_controller_config.json")
HIGH_SCORE_FILE = Path("fruit_ninja_high_score.txt")

DEFAULT_LOWER = np.array([120, 60, 60])
DEFAULT_UPPER = np.array([165, 255, 255])

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

if not cap.isOpened():
    print("Camera did not open")
    exit()

objects = []
trail = []

score = 0
lives = 3
game_over = False
last_spawn = time.time()
spawn_delay = 0.8
combo = 0
last_slice_time = 0

fruit_names = ["APPLE", "MELON", "ORANGE", "KIWI", "LEMON"]

def load_high_score():
    if HIGH_SCORE_FILE.exists():
        try:
            return int(HIGH_SCORE_FILE.read_text().strip())
        except Exception:
            return 0
    return 0

def save_high_score(value):
    HIGH_SCORE_FILE.write_text(str(value), encoding="utf-8")

high_score = load_high_score()

def load_color_config():
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            lower = np.array(data["lower"], dtype=np.uint8)
            upper = np.array(data["upper"], dtype=np.uint8)
            return lower, upper
        except Exception:
            pass
    return DEFAULT_LOWER.copy(), DEFAULT_UPPER.copy()

def save_color_config(lower, upper):
    data = {
        "lower": [int(x) for x in lower],
        "upper": [int(x) for x in upper],
    }
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

color_lower, color_upper = load_color_config()

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def spawn_object():
    is_bomb = random.random() < 0.18
    obj = {
        "x": float(random.randint(120, WIDTH - 120)),
        "y": float(HEIGHT + 60),
        "vx": random.uniform(-4, 4),
        "vy": random.uniform(-19, -14),
        "r": 35 if not is_bomb else 38,
        "bomb": is_bomb,
        "name": "BOMB" if is_bomb else random.choice(fruit_names),
        "alive": True
    }
    objects.append(obj)

def draw_object(frame, obj):
    x = int(obj["x"])
    y = int(obj["y"])
    r = int(obj["r"])

    if obj["bomb"]:
        cv2.circle(frame, (x, y), r, (35, 35, 35), -1)
        cv2.circle(frame, (x, y), r, (0, 0, 255), 4)
        cv2.line(frame, (x - 15, y - 15), (x + 15, y + 15), (0, 0, 255), 4)
        cv2.line(frame, (x + 15, y - 15), (x - 15, y + 15), (0, 0, 255), 4)
    else:
        colors = {
            "APPLE": (0, 0, 255),
            "MELON": (0, 180, 0),
            "ORANGE": (0, 150, 255),
            "KIWI": (40, 180, 40),
            "LEMON": (0, 255, 255),
        }
        color = colors.get(obj["name"], (180, 0, 255))
        cv2.circle(frame, (x, y), r, color, -1)
        cv2.circle(frame, (x, y), r, (255, 255, 255), 3)
        cv2.putText(frame, obj["name"][0], (x - 12, y + 13),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

def calibrate_color(frame):
    global color_lower, color_upper

    cx = WIDTH // 2
    cy = HEIGHT // 2
    size = 40

    roi = frame[cy - size:cy + size, cx - size:cx + size]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    h = int(np.median(hsv_roi[:, :, 0]))
    s = int(np.median(hsv_roi[:, :, 1]))
    v = int(np.median(hsv_roi[:, :, 2]))

    h_margin = 15
    s_margin = 70
    v_margin = 70

    lower_h = max(0, h - h_margin)
    upper_h = min(179, h + h_margin)

    color_lower = np.array([lower_h, max(40, s - s_margin), max(40, v - v_margin)], dtype=np.uint8)
    color_upper = np.array([upper_h, min(255, s + s_margin), min(255, v + v_margin)], dtype=np.uint8)

    save_color_config(color_lower, color_upper)
    print("Controller color calibrated:", color_lower.tolist(), color_upper.tolist())

def reset_game():
    global score, lives, game_over, last_spawn, spawn_delay, combo, last_slice_time
    objects.clear()
    trail.clear()
    score = 0
    lives = 3
    game_over = False
    last_spawn = time.time()
    spawn_delay = 0.8
    combo = 0
    last_slice_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    display = frame.copy()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_lower, color_upper)

    mask = cv2.GaussianBlur(mask, (9, 9), 0)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=3)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    controller_x = None
    controller_y = None

    if contours and not game_over:
        biggest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(biggest)

        if area > 500:
            x, y, w, h = cv2.boundingRect(biggest)
            controller_x = x + w // 2
            controller_y = y + h // 2

            trail.append((controller_x, controller_y, time.time()))

            cv2.rectangle(display, (x, y), (x + w, y + h), (180, 0, 255), 2)
            cv2.circle(display, (controller_x, controller_y), 18, (255, 255, 255), -1)
            cv2.circle(display, (controller_x, controller_y), 28, (180, 0, 255), 4)

    trail = [(x, y, t) for x, y, t in trail if time.time() - t < 0.35]

    for i in range(1, len(trail)):
        x1, y1, _ = trail[i - 1]
        x2, y2, _ = trail[i]
        cv2.line(display, (x1, y1), (x2, y2), (255, 255, 255), 10)
        cv2.line(display, (x1, y1), (x2, y2), (180, 0, 255), 4)

    if not game_over and time.time() - last_spawn > spawn_delay:
        spawn_object()
        last_spawn = time.time()
        spawn_delay = max(0.35, spawn_delay * 0.985)

    sliced_this_frame = 0

    if not game_over:
        for obj in objects:
            obj["x"] += obj["vx"]
            obj["y"] += obj["vy"]
            obj["vy"] += 0.55

            for tx, ty, _ in trail:
                if distance(tx, ty, obj["x"], obj["y"]) < obj["r"] + 20:
                    if obj["bomb"]:
                        lives -= 1
                        combo = 0
                    else:
                        score += 1
                        sliced_this_frame += 1
                    obj["alive"] = False
                    break

            if obj["y"] > HEIGHT + 100:
                obj["alive"] = False
                if not obj["bomb"]:
                    lives -= 1
                    combo = 0

    if sliced_this_frame > 0:
        if time.time() - last_slice_time < 0.6:
            combo += sliced_this_frame
        else:
            combo = sliced_this_frame
        last_slice_time = time.time()

        if combo >= 3:
            score += 1

    objects = [obj for obj in objects if obj["alive"]]

    for obj in objects:
        draw_object(display, obj)

    if lives <= 0:
        game_over = True
        if score > high_score:
            high_score = score
            save_high_score(high_score)

    cv2.putText(display, "FRUIT NINJA WEBCAM PRO", (25, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (180, 0, 255), 3)

    cv2.putText(display, f"SCORE: {score}", (25, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 3)

    cv2.putText(display, f"HIGH SCORE: {high_score}", (25, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 255, 255), 2)

    cv2.putText(display, f"LIVES: {lives}", (25, 170),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)

    if combo >= 3:
        cv2.putText(display, f"COMBO x{combo}", (WIDTH - 260, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 255), 3)

    if controller_x is None and not game_over:
        cv2.putText(display, "SHOW PURPLE CONTROLLER", (25, HEIGHT - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 0, 255), 3)
    else:
        cv2.putText(display, "CONTROLLER FOUND", (25, HEIGHT - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 0, 255), 3)

    cv2.rectangle(display, (WIDTH // 2 - 40, HEIGHT // 2 - 40),
                  (WIDTH // 2 + 40, HEIGHT // 2 + 40), (255, 255, 255), 2)

    cv2.putText(display, "C: calibrate | R: restart | Q: quit", (25, HEIGHT - 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if game_over:
        cv2.putText(display, "GAME OVER", (WIDTH // 2 - 190, HEIGHT // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

        cv2.putText(display, "Press R to restart or Q to quit",
                    (WIDTH // 2 - 270, HEIGHT // 2 + 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

    cv2.imshow("Fruit Ninja Webcam PRO", display)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord("r"):
        reset_game()

    if key == ord("c"):
        calibrate_color(frame)

cap.release()
cv2.destroyAllWindows()
