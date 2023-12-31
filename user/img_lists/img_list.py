from flask import Blueprint, render_template, request, redirect, url_for,session
import db.list_db 

img_list_bp = Blueprint('img', __name__, url_prefix='/img',
                      template_folder='templates',
                        static_url_path='/static',
                          static_folder='./static')


@img_list_bp.route('/<int:page_num>', methods=["GET"])
def list(page_num):
    per_page = 4
    images = db.list_db.img_list(page_num,per_page)
    counts = db.list_db.img_count()
    total_pages = int(counts[0]) // per_page + (int(counts[0]) % per_page > 0)
    page = int(counts[0] / per_page + 1)
  
    return render_template('list.html',images=images,counts=counts,page=page,total_pages=total_pages)


