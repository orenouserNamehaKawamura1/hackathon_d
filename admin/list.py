from flask import Blueprint, render_template, request, redirect, url_for,session
import db.list_db 

list_bp = Blueprint('list', __name__, url_prefix='',
                      template_folder='templates',
                        static_url_path='/static',
                          static_folder='./static')


@list_bp.route('/<int:page_num>', methods=["GET"])
def ac_list(page_num):
  per_page = 4
  users = db.list_db.ac_lists(page_num,per_page)
  counts = db.list_db.ac_count()
  total_pages = int(counts[0]) // per_page + (int(counts[0]) % per_page > 0)
  page = int(counts[0] / per_page + 1)
  
  return render_template('list/list.html',users=users,counts=counts,page=page,total_pages=total_pages)

@list_bp.route('/confirm/<int:id>/',methods=['GET'])
def confirm(id):
  mail = request.args.get('mail')
  
  return render_template('list/comfirm.html',id=id,mail=mail)
  
  

@list_bp.route('/delete/<int:id>',methods=['POST'])
def delete(id):
  row = db.list_db.ac_delete(id)
  if row == 1:
    return redirect(url_for('list.ac_list',page_num=1))
  else :
    return redirect(url_for('list.ac_list',page_num=1))
  