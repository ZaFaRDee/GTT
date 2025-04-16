import os
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

torch.set_num_threads(1)

# Mahalliy model papkasi
model_path = "models/finbert"
remote_model = "yiyanghkust/finbert-tone"

# Modelni birinchi marta internetdan yuklab, keyin saqlash
if not os.path.exists(model_path):
    print("🔄 FinBERT modeli internetdan yuklanmoqda...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(remote_model)
    model = AutoModelForSequenceClassification.from_pretrained(remote_model)
    os.makedirs(model_path, exist_ok=True)
    tokenizer.save_pretrained(model_path)
    model.save_pretrained(model_path)
else:
    print("✅ FinBERT modeli diskdan yuklanmoqda...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Modelni baholash rejimiga o‘tkazish
model.eval()

def analyze_with_finbert(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        sentiment = torch.argmax(probs).item()

    label_map = {
        0: "🔴 Negative",
        1: "🟡 Neutral",
        2: "🟢 Positive"
    }
    return label_map[sentiment], probs[0][sentiment].item()
