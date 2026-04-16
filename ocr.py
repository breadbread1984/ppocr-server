#!/usr/bin/python3

import subprocess

class OCR(object):
  def __init__(self,):
    pass
  def process(self, pdf_path, output_dir):
    proc = subprocess.Popen(
      [
        "python3.12",
        "-m"
        "uv",
        "run",
        "paddleocr",
        "pp_structurev3",
        "-i",
        pdf_path,
        "--save_path",
        output_dir,
      ],
      env = env,
      cwd = "/app",
      stdout = subprocess.PIPE,
      stderr = subprocess.STDOUT,
      text = True,
      bufsize = 1,
      universal_newlines = True
    )
    try:
      while True:
        output = proc.stdout.readline()
        if output == '' and proc.poll() is not None:
          break
        if output:
          print(output.strip())
    except:
      proc.kill()
    if not exists(output_dir):
      return False
    markdowns = dict()
    pattern = r'_(\d+)\.md$'
    img_dir = None
    files_to_delete = list()
    for f in listdir(output_dir):
      if isdir(join(output_dir, f)):
        img_dir = join(output_dir, f)
        continue
      files_to_delete.append(join(output_dir, f))
      stem, ext = splitext(f)
      if ext != '.md': continue
      matches = re.search(pattern, f)
      page_num = int(matches.group(1))
      markdowns[page_num] = join(output_dir, f)
    markdowns = dict(sorted(markdowns.items(), key = lambda x: int(x[0])))
    markdown_contents = list()
    for idx, md_path in markdowns.items():
      with open(md_path, 'r') as f:
        markdown_contents.append(f.read())
    markdown = '\n\n'.join(markdown_contents)
    for f in files_to_delete:
      remove(f)
    with open(join(output_dir, 'result.md'), 'w') as f:
      f.write(markdown)
    return True
