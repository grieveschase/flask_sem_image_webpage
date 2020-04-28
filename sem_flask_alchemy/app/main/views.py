#set FLASK_APP=flasky.py
#set FLASK_DEBUG=1
##remove all db stuff, clear migrations folder, delete data-dev.sqlite
#flask db init
#flask db migrate
#flask db upgrade
#flask shell
#>Role.insert_roles()
#>User.insert_users()
#>ctrl+z
#flask run --host=172.18.30.60

from flask import render_template, session, redirect, url_for, current_app, request
import datetime
from ..models import User, MeasDisplay_Obs, PatternFOV
from . import main
from .forms import LotSearchForm, DeviceForm
from flask_login import login_user, logout_user, login_required, current_user
from ..decorators import admin_required
import sqlite3
from .semsql import *
import sys
import io
from io import BytesIO
from PIL import Image
from datetime import timedelta



@main.route('/', methods=['GET'])
@login_required
def index():

    if not session['_fresh']:
        logout_user()

    return render_template('index.html')


@main.route('/measdisplay_home/<tool_route>', methods=['GET','POST'])
@login_required
def measdisplay_home(tool_route):
    if not session['_fresh']:
        logout_user()
    form = LotSearchForm()
    if form.validate_on_submit():
        lotlike = "%{}%".format(str(form.lot.data))
        rcplike = "%{}%".format(str(form.recipe.data))
        lots = MeasDisplay_Obs.query.with_entities(MeasDisplay_Obs.lot, MeasDisplay_Obs.slot,MeasDisplay_Obs.recipe, MeasDisplay_Obs.port,MeasDisplay_Obs.measdate).filter(MeasDisplay_Obs.tool.like(tool_route), MeasDisplay_Obs.lot.like(lotlike), MeasDisplay_Obs.recipe.like(rcplike)).order_by(MeasDisplay_Obs.measdate.desc()).distinct().all()
        session['lots_obs'+tool_route] = lots
        return redirect(url_for('.measdisplay_home', tool_route=tool_route))
    return render_template('measdisplay_home.html',
                                form = form,
                                lots = session.get('lots_obs'+tool_route,False),
                                tool_route=tool_route)

@main.route('/measdisplay_view/<t>/<l>/<s>/<r>/<p>/<dd>')
@login_required
def measdisplay_view(t,l,s,r,p,dd):
    if not session['_fresh']:
        logout_user()

    y = datetime.timedelta(seconds=1)
    lot_info = MeasDisplay_Obs.query.filter(MeasDisplay_Obs.tool.like(t), MeasDisplay_Obs.lot.like(l), MeasDisplay_Obs.recipe.like(r),MeasDisplay_Obs.port.like(p),MeasDisplay_Obs.measdate < (datetime.datetime.strptime(dd,"%Y-%m-%d %H:%M:%S") + y), MeasDisplay_Obs.measdate > (datetime.datetime.strptime(dd,"%Y-%m-%d %H:%M:%S") - y)).all()
    info_list = []
    for tic in lot_info:
        save_file_name = "C://Python3//sem_flask_alchemy//app//static//FOV//" +str(tic.lot)+str(tic.recipe)+str(tic.target)+str(tic.fieldx)+str(tic.fieldy)+str(tic.site_order)+str(tic.cycle)+str(datetime.datetime.strftime(tic.date,"%Y_%m_%d_%H_%M_%S")) + ".jpg"
        image = Image.open(io.BytesIO(tic.image))
        image.save(save_file_name)
        image.close()
        img_file_path = "/static/FOV/"+str(tic.lot)+str(tic.recipe)+str(tic.target)+str(tic.fieldx)+str(tic.fieldy)+str(tic.site_order)+str(tic.cycle)+datetime.datetime.strftime(tic.date,"%Y_%m_%d_%H_%M_%S")+ ".jpg"
        temp = [tic.slot,tic.fov,tic.iprobe,tic.lot,tic.recipe,tic.site_type,tic.site_order,tic.fieldx,tic.fieldy,tic.locx,tic.locy,tic.date,tic.port,tic.cycle,tic.target,tic.measdate,img_file_path]
        info_list.append(temp)
    targets = list(set([t[-3] for t in info_list]))
    target_dict = dict((i,[]) for i in targets)
    for i in info_list:
        target_dict[i[-3]].append(i)

    return render_template('measdisplay_view.html',
                            target_dict=target_dict,
                            meas_tool = t,
                            lot = l,
                            slot = s,
                            recipe = r,
                            port = p,
                            date_meas = dd)


@main.route('/patternfov_home/<tool_route>', methods=['GET','POST'])
@login_required
def patternfov_home(tool_route):
    if not session['_fresh']:
        logout_user()
    form = LotSearchForm()
    if form.validate_on_submit():
        lotlike = "%{}%".format(str(form.lot.data))
        rcplike = "%{}%".format(str(form.recipe.data))
        lots = PatternFOV.query.with_entities(PatternFOV.lot, PatternFOV.slot,PatternFOV.recipe, PatternFOV.port,PatternFOV.measdate).filter(PatternFOV.tool.like(tool_route), PatternFOV.lot.like(lotlike), PatternFOV.recipe.like(rcplike)).order_by(PatternFOV.measdate.desc()).distinct().all()
        session['lots_fov'+tool_route] = lots
        return redirect(url_for('.patternfov_home', tool_route=tool_route))
    return render_template('patternfov_home.html',
                                form = form,
                                lots = session.get('lots_fov'+tool_route,False),
                                tool_route=tool_route)


@main.route('/patternfov_view/<t>/<l>/<s>/<r>/<p>/<dd>')
@login_required
def patternfov_view(t,l,s,r,p,dd):
    if not session['_fresh']:
        logout_user()

    y = datetime.timedelta(seconds=1)
    lot_info = PatternFOV.query.filter(PatternFOV.tool.like(t), PatternFOV.lot.like(l), PatternFOV.recipe.like(r),PatternFOV.port.like(p),PatternFOV.measdate < (datetime.datetime.strptime(dd,"%Y-%m-%d %H:%M:%S") + y), PatternFOV.measdate > (datetime.datetime.strptime(dd,"%Y-%m-%d %H:%M:%S") - y)).order_by(PatternFOV.date.asc()).all()
    info_list = []
    for tic in lot_info:
        save_file_name = "C://Python3//sem_flask_alchemy//app//static//FOV//" +str(tic.lot)+str(tic.recipe)+str(tic.target)+str(tic.fieldx)+str(tic.fieldy)+str(tic.site_order)+str(tic.cycle)+str(datetime.datetime.strftime(tic.date,"%Y_%m_%d_%H_%M_%S")) + ".jpg"
        #save_file_name = "//home//ccag//Python_Scripts//sem_flask_alchemy//app//static//FOV//" +str(tic.lot)+str(tic.recipe)+str(tic.target)+str(tic.fieldx)+str(tic.fieldy)+str(tic.site_order)+str(tic.cycle)+str(datetime.datetime.strftime(tic.date,"%Y_%m_%d_%H_%M_%S")) + ".jpg"
        image = Image.open(io.BytesIO(tic.image))
        image.save(save_file_name)
        image.close()
        img_file_path = "/static/FOV/"+str(tic.lot)+str(tic.recipe)+str(tic.target)+str(tic.fieldx)+str(tic.fieldy)+str(tic.site_order)+str(tic.cycle)+datetime.datetime.strftime(tic.date,"%Y_%m_%d_%H_%M_%S")+ ".jpg"
        temp = [tic.slot,tic.fov,tic.iprobe,tic.lot,tic.recipe,tic.site_type,tic.site_order,tic.fieldx,tic.fieldy,tic.locx,tic.locy,tic.date,tic.port,tic.cycle,tic.target,tic.measdate,img_file_path]
        info_list.append(temp)
    targets = list(set([t[-3] for t in info_list]))
    target_dict = dict((i,[]) for i in targets)
    for i in info_list:
        target_dict[i[-3]].append(i)

    return render_template('patternfov_view.html',
                            info_list = info_list,
                            target_dict=target_dict,
                            meas_tool = t,
                            lot = l,
                            slot = s,
                            recipe = r,
                            port = p,
                            date_meas = dd)









#
