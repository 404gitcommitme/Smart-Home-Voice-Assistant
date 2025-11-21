# 🏠 Full Offline Smart Home Voice Assistant

**Two ultra-light TinyBERT models for natural voice command understanding — 100% offline, <60 MB total, <100 ms on CPU**

```python
understand_command("turn off all lights in the kitchen")
→ {'intent': 'turn_off', 'device': 'light', 'indices': ['all', 'kitchen']}
```

> No cloud · No internet · No latency  
> Works even after the apocalypse 🌍

---

## ✨ Features

### 🧠 Natural Language Understanding (Offline)

**Intent Recognition:**
- `turn_on`, `turn_off`, `open`, `close`, `lock`, `unlock`

**Device Detection:**
- Light, door, window, fan, TV, air conditioner, security camera, thermostat, heater

**Smart Multi-Index Extraction:**
- **Numbers:** "one", "first", "19th", "twenty-fifth", etc.
- **Rooms:** kitchen, bedroom, living room, garage, attic, basement
- **Multiple indices:** "fourth and fifteenth fan" → `['4', '15']`
- **"all" + room:** "turn off all lights in the kitchen" → `['all', 'kitchen']`

### ⚙️ Technical Highlights

- Trained on **50,000+ real + synthetic commands**
- Two **TinyBERT (4-layer)** models
- Runs perfectly on **Raspberry Pi 4/5**, old laptops, or any CPU
- **0% cloud dependency** → fully private & secure

---

## 🚀 Live Demo

```python
>>> understand_command("open the seventh door in garage")
{'intent': 'open', 'device': 'door', 'indices': ['7', 'garage']}

>>> understand_command("please turn off every fan in the bedroom")
{'intent': 'turn_off', 'device': 'fan', 'indices': ['all', 'bedroom']}
```

---

## ⚡ Quick Start

```bash
git clone https://github.com/yourusername/Smart-Home-Voice-Assistant.git
cd Smart-Home-Voice-Assistant
pip install -r requirements.txt
python smart_home_assistant.py
```

---

## 📁 Project Structure

```
Smart-Home-Voice-Assistant/
├── models/
│   ├── tinybert_intent_device/
│   └── tinybert_index/
├── smart_home_assistant.py
├── requirements.txt
└── README.md
```

---

## 🛠 Usage in Your Project

```python
from smart_home_assistant import understand_command

result = understand_command(user_voice_text)

if result["intent"] == "turn_on" and result["device"] == "light":
    if "all" in result["indices"]:
        turn_on_all_lights()
    else:
        for idx in result["indices"]:
            if idx.isdigit():
                turn_on_light(int(idx))
            else:
                turn_on_lights_in_room(idx)
```

---

## 🎯 Why This Project?

- ✅ Full voice → structured command pipeline
- ✅ Ultra-light, edge-AI friendly
- ✅ CPU-only, fast inference
- ✅ Perfect for ML, NLP, IoT, and robotics projects

---

## 📄 License

MIT License - feel free to use in your projects!

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## ⭐ Support

If you find this project useful, please give it a star on GitHub!
