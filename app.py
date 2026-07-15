import os
import io
import requests
import gradio as gr
BACKEND_URL = "https://backend-image-itdr.onrender.com/generate-story"

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

    print(response.status_code)
    print(response.text)

    if response.status_code == 200:
        try:
            return response.json().get("story", response.text)
        except:
            return response.text
    else:
        return f"Backend Error ({response.status_code}):\n{response.text}"


with gr.Blocks(title="Image-to-Story Generator") as demo:
    gr.Markdown("# 📖 Image-to-Story Generator")

    with gr.Row():
        with gr.Column():
            image = gr.Image(type="pil", label="Upload Image")

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
            output = gr.Textbox(lines=20, label="Generated Story")

    button.click(
        fn=generate,
        inputs=[image, genre, length],
        outputs=output
    )

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)
