from flask import Flask, request, send_file, render_template
import os
import generator, str_find

# HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Файл не выбран'
        file = request.files['file']
        if file and '.pdf' in file.filename:
            input_file_path = os.path.join('uploads', file.filename)
            output_file_path = os.path.join('uploads', 'res.pdf')
            file.save(input_file_path)
            generator.generate(str_find.analyze_font_sizes(input_file_path), input_file_path, output_file_path)
            return send_file(output_file_path, as_attachment=True)
        return 'Неверный тип файла'
    return render_template('index.html')
   
def init_dir(filename):
    if not os.path.exists(filename):
        os.makedirs(filename)

if __name__ == '__main__':
    init_dir('uploads')
    app.run(host='0.0.0.0', debug=True)