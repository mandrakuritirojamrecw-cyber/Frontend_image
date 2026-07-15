import sys
import os
import gradio as gr
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "Backend")
)
import requests
import io

BACKEND_URL = "http://127.0.0.1:8000/generate-story"

def generate(image, genre, length):
    if image is None:
        return "Please upload an image."

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    files = {
        "image": ("image.png", img_bytes.getvalue(), "image/png")
    }

    data = {
        "genre": genre,
        "length": length
    }

    response = requests.post(
        BACKEND_URL,
        files=files,
        data=data
    )

    return response.json()["story"]
with gr.Blocks(title="Image-to-Story Generator") as demo:
    gr.Markdown("# 📖 Image-to-Story Generator")
    with gr.Row():
        with gr.Column():
            image = gr.Image(
                type="pil",
                label="Upload Image"
            )
            genre = gr.Dropdown(
                [
                    "Adventure",
                    "Fantasy",
                    "Mystery",
                    "Comedy",
                    "Horror",
                    "Science Fiction",
                    "Motivational"
                ],
                value="Adventure",
                label="Story Genre"
            )
            length = gr.Radio(
                [
                    "Short (100 words)",
                    "Medium (200 words)",
                    "Long (400 words)"
                ],
                value="Medium (200 words)",
                label="Story Length"
            )
            button = gr.Button("Generate Story")
        with gr.Column():
            output = gr.Textbox(
                lines=20,
                label="Generated Story"
            )
    button.click(
        generate,
        inputs=[image, genre, length],
        outputs=output
)

demo.launch()