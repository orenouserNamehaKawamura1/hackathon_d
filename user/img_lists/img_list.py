from flask import Blueprint, render_template,request,redirect,url_for,session
import db.list_db

img_list_bp = Blueprint('img', __name__, url_prefix='/img',
                        template_folder='templates',
                        static_url_path='/static',
                        static_folder='./static')


@img_list_bp.route('/<int:page_num>', methods=["GET"])
def list(page_num):
    per_page = 4
    images = db.list_db.img_list(page_num, per_page)
    counts = db.list_db.img_count()
    total_pages = int(counts[0]) // per_page + (int(counts[0]) % per_page > 0)
    page = int(counts[0] / per_page + 1)
    return render_template(
                            'img/list.html',
                            images=images,
                            counts=counts[0],
                            page=page,
                            total_pages=total_pages
                            )

@img_list_bp.route('/datial/',methods=['GET'])
def datail():
    id = request.args.get('id')
    file = request.args.get('filename','')
    return render_template('img/datail.html',filename = file,id=id)

@img_list_bp.route('/confirm/', methods=['GET'])
def confirm():
    id = request.args.get('id')
    file = request.args.get('filename','')
    return render_template('img/comfirm.html', filename = file,id=id)


@img_list_bp.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    row = db.list_db.img_delete(id)
    if row == 1:
        return redirect(url_for('img.list', page_num=1))
    else:
        return redirect(url_for('img.list', page_num=1))