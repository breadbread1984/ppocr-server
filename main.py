#!/usr/bin/python3

from absl import app, flags
import gradio as gr
from uuid import uuid4
from os import listdir
from os.path import join
from ocr import OCR
from minio_client import MinioClient
import configs

FLAGS = flags.FLAGS

def add_options():
  flags.DEFINE_string("host", default = '0.0.0.0', help = 'service host')
  flags.DEFINE_integer("port", default = 8081, help = 'service port')

def create_interface():
  ocr = OCR()
  minio_client = MinioClient(configs)
  def process_ocr(file_input):
    session_id = str(uuid4())
    output_dir = join('/', 'tmp', session_id)
    result = ocr.process(file_input, output_dir)
    minio_client.create_bucket(session_id)
    minio_client.upload(session_id, join(output_dir, 'result.md'))
    for img in listdir(join(output_dir, 'imgs')):
      minio_client.upload(session_id, join(output_dir, 'imgs', f), join('imgs', f))
    return session_id

  with gr.Blocks() as demo:
    with gr.Column():
      file_input = gr.File(label = "file upload", file_types = [".pdf"])
      submit_btn = gr.Button("submit")
      bucket_name = gr.Textbox(label = "bucket name", interactive = False)
    submit_btn.click(process_ocr, inputs = [file_input], outputs = [bucket_name], concurrency_limit = 64)

def main(unused_argv):
  demo = create_interface()
  demo.launch(server_name = FLAGS.host,
              server_port = FLAGS.port,
              shared = True,
              show_error = True,
              max_threads = 64)

if __name__ == "__main__":
  add_options()
  app.run(main)

