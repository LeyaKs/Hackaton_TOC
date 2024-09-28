from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Файл не выбран'
        file = request.files['file']
        if file and '.pdf' in file.filename:
            file.save(os.path.join('uploads', file.filename))
            # Обработка файла
            # тык
            # тык
            # тык
            return send_file(os.path.join('uploads', file.filename), as_attachment=True)
        return 'Неверный тип файла'
    return '''
    <!doctype html>
    <title>Загрузка файла</title>
    <h1>Загрузите файл</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Загрузить>
    </form>
    '''

def init_dir(filename):
    if not os.path.exists(filename):
        os.makedirs(filename)

if __name__ == '__main__':
    init_dir('uploads')
    app.run(debug=True)
