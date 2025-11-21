# smart_home_assistant.py
# 100% OFFLINE Smart Home Voice Assistant
# Intent + Device + Multiple Indices (numbers, rooms, "all")

import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification
import joblib
import os

# ====================== CHARGEMENT MODÈLES ======================
device = torch.device("cpu")  # ou "cuda" si tu as GPU

# --- Modèle 1 : Intent + Device (deux têtes) ---
class TinyBERTTwoHeads(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = AutoModel.from_pretrained("./models/tinybert_intent_device")
        hidden = self.bert.config.hidden_size
        self.dropout = nn.Dropout(0.1)
        self.intent_head = nn.Linear(hidden, 7)   # 7 intents
        self.device_head = nn.Linear(hidden, 9)   # 9 devices

    def forward(self, input_ids, attention_mask=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled = self.dropout(outputs[1])
        return self.intent_head(pooled), self.device_head(pooled)

# Labels
intents = ["lock", "unlock", "open", "close", "turn_on", "turn_off", "unknown"]
devices = ["door", "window", "light", "TV", "fan", "heater", "thermostat", "security camera", "air conditioner"]
id2intent = {i: name for i, name in enumerate(intents)}
id2device = {i: name for i, name in enumerate(devices)}

print("Chargement du modèle Intent + Device...")
tokenizer_id = AutoTokenizer.from_pretrained("./models/tinybert_intent_device")
model_id = TinyBERTTwoHeads()
model_id.load_state_dict(torch.load("./models/tinybert_intent_device/pytorch_model.bin", map_location=device))
model_id.eval()

# --- Modèle 2 : Indices (multi-label) ---
print("Chargement du modèle Indices...")
tokenizer_idx = AutoTokenizer.from_pretrained("./models/tinybert_index")
model_idx = AutoModelForSequenceClassification.from_pretrained("./models/tinybert_index")
mlb = joblib.load("./models/tinybert_index/mlb.pkl")
model_idx.eval()

print("Les deux modèles sont chargés ! Assistant prêt !\n")

# ====================== FONCTIONS DE PRÉDICTION ======================
def predict_intent_device(text: str):
    if not text.strip():
        return "unknown", "unknown"
    inputs = tokenizer_id(text.lower(), truncation=True, padding=True, max_length=64, return_tensors="pt")
    with torch.no_grad():
        intent_logits, device_logits = model_id(inputs["input_ids"], inputs["attention_mask"])
    intent = id2intent[intent_logits.argmax(dim=1).item()]
    device_name = id2device[device_logits.argmax(dim=1).item()]
    return intent, device_name

def predict_indices(text: str, threshold: float = 0.25):
    inputs = tokenizer_idx(text, truncation=True, padding=True, max_length=64, return_tensors="pt")
    with torch.no_grad():
        logits = model_idx(**inputs).logits
        probs = torch.sigmoid(logits).cpu().numpy()[0]
    predicted = [mlb.classes_[i] for i, p in enumerate(probs) if p > threshold]
    predicted = sorted(predicted)
    return predicted if predicted else ["none"]

# ====================== FONCTION PRINCIPALE ======================
def understand_command(command: str):
    intent, device = predict_intent_device(command)
    indices = predict_indices(command)
    
    return {
        "command": command,
        "intent": intent,
        "device": device,
        "indices": indices
    }

# ====================== TEST EN LIVE ======================
if __name__ == "__main__":
    tests = [
        "turn off the first and second lights in the kitchen",
        "open all doors in garage",
        "lock the front door",
        "turn on the nineteenth fan",
        "close every window in the bedroom",
        "deactivate the attic air conditioner",
        "hey, switch on all fans please"
    ]

    print("🏠 SMART HOME VOICE ASSISTANT - 100% OFFLINE\n")
    for cmd in tests:
        result = understand_command(cmd)
        print(f"🎤  \"{cmd}\"")
        print(f"    → Intent : {result['intent']}")
        print(f"    → Device : {result['device']}")
        print(f"    → Indices: {result['indices']}\n")