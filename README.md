# Text Summarizer

A web-based text summarization app powered by a fine-tuned **T5 transformer model**, served via **FastAPI** with a clean responsive frontend.

---

## Features

- Summarizes long text and dialogues into concise summaries
- Responsive UI — works on desktop, tablet, and mobile
- GPU acceleration support — NVIDIA CUDA, Apple Silicon MPS, and CPU fallback
- Beam search decoding for higher quality summaries
- Repetition penalty to avoid redundant output

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, Uvicorn |
| AI Model | T5 (fine-tuned), Hugging Face Transformers |
| Deep Learning | PyTorch |
| Frontend | HTML5, CSS3, Vanilla JavaScript |

---

## Project Structure

```
text-summarizer-t5/
├── appy.py                  # FastAPI backend — routes, model inference
├── index.html               # Frontend UI template (served via Jinja2)
├── index.css                # Responsive stylesheet
├── index.js                 # Frontend logic — fetch API calls
└── saved_summary_model/     # Fine-tuned T5 model weights (not included)
    ├── config.json
    ├── tokenizer_config.json
    └── pytorch_model.bin
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/text-summarizer-t5.git
cd text-summarizer-t5
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn transformers torch
```

### 3. Add your fine-tuned T5 model

Place your model folder at the project root:

```
./saved_summary_model/
```

> The model is not included in this repository due to file size.  
> You can fine-tune your own using the [SAMSum dataset](https://huggingface.co/datasets/samsum) or download a pre-trained variant from Hugging Face.

### 4. Run the server

```bash
uvicorn appy:app --reload
```

### 5. Open in your browser

```
http://localhost:8000
```

---

## API Reference

### `POST /summarize`

Accepts a JSON body and returns a summary.

**Request:**
```json
{
  "text": "Your long text or dialogue goes here..."
}
```

**Response:**
```json
{
  "summary": "Concise summary of the input text."
}
```

### `GET /`

Serves the frontend UI.

---

## How It Works

1. User enters text in the input box and clicks **Summarize**
2. The frontend sends a `POST` request to `/summarize` with the input text
3. The backend cleans the text, prepends the `"summarize: "` task prefix required by T5
4. The tokenized input is passed to the fine-tuned T5 model
5. Beam search generates the summary, which is decoded and returned
6. The summary is displayed in the output box

---

## Device Support

The app automatically detects and uses the best available device:

```
NVIDIA GPU  →  torch.device("cuda")
Apple GPU   →  torch.device("mps")
CPU         →  torch.device("cpu")
```

---

## Notes

- Minimum recommended input: 3–4 sentences for meaningful summaries
- Input is capped at 512 tokens; longer text is truncated
- Output is capped at 200 tokens

---

## .gitignore

Make sure to add the following to avoid pushing large model files:

```
saved_summary_model/
__pycache__/
*.pyc
.env
```
