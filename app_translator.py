import random
import gradio as gr
from transformers import pipeline

pipe = pipeline("translation", "t5-base")

def translate(text):
    return pipe(text)[0]['translation_text']

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            english = gr.Textbox(label="English Text")
            translate_btn = gr.Button(value="Translate")
        with gr.Column():
            german = gr.Textbox(label='German Translation')
    
    translate_btn.click(translate, inputs=english, outputs=german)
    examples = gr.Examples(examples=["I went to market", "Helen is a good swimmer"],
                           inputs=english)

demo.launch(share=True)
