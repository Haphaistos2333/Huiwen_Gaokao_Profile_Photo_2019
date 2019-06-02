import flask
import os
from PIL import Image

basedir = os.path.abspath(os.path.dirname(__file__))
app = flask.Flask(__name__)


@app.route('/up_photo', methods=['post'])
def up_photo():
    img = flask.request.files.get('photo')
    path = basedir+'/hw/'
    file_path = path + img.filename
    img.save(file_path)
    res = make_photo(img.filename)
    return flask.send_from_directory('hw', res, as_attachment=False)


def make_photo(filename):
    base_img = Image.open(basedir+'/hw_base.png')
    target = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    box = (70, 65, 335, 330)
    region = Image.open(basedir+'/hw/'+filename)
    region = region.convert('RGBA')
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    target.paste(region, box)
    target.paste(base_img, (0, 0), base_img)
    target = target.convert('RGB')
    target.save(basedir+'/hw/'+filename+'_out.jpg')
    return filename+'_out.jpg'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
