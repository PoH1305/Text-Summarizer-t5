from fastapi import FastAPI
from fastapi import Request
from pydantic import BaseModel
from transformers import T5Tokenizer, T5ForConditionalGeneration
import re
import torch
from fastapi.templating import Jinja2Templates # UI part
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


# initialization of APP
app = FastAPI( title = "App Summarizer", description = "Text Summarizer Using T5 Model", version = "1.0")

# model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("./saved_summary_model")
tokenizer = T5Tokenizer.from_pretrained("./saved_summary_model")

# device configuration
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Using NVIDIA GPU: {torch.cuda.get_device_name(0)}")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Using Apple Silicon GPU")
else:
    device = torch.device("cpu")
    print("CPU")

model.to(device)

# Templating
templates = Jinja2Templates(directory = ".")
app.mount("/static", StaticFiles(directory="."), name="static")

# input Schema for Dialogue
class DialogueInput(BaseModel):
    text: str

# Cleaning the text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"<.*?>"," ", text)
    text = re.sub(r"\r\n", " ", text)
    text = text.strip().lower()
    return text

# Summarization function
def summarize_dialogue(dialogue: str) -> str:
    dialogue = clean_text(dialogue)
    dialogue = "summarize: " + clean_text(dialogue)

    # Tokenization
    inputs = tokenizer(
        text = dialogue,
        max_length = 512,
        truncation = True,
        padding = "max_length",
        return_tensors = "pt"
    )

    # Move input tensors to the same device as the model
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    # summary generation
    targets = model.generate(
        input_ids = inputs["input_ids"],
        attention_mask = inputs["attention_mask"],
        max_length = 200,
        num_beams = 4,
        early_stopping = True,
        repetition_penalty = 2.0  # Added repetition penalty
    )

    # Decoding
    summary = tokenizer.decode(
        targets[0],
        skip_special_tokens = True
    )
    return summary

@app.post("/summarize")
async def summarize(dialogue_input : DialogueInput):
    my_summary = summarize_dialogue(dialogue_input.text)
    return {"summary" : my_summary}

@app.get("/", response_class = HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})