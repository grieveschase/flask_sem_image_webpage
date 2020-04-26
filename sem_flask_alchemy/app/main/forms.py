from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import os

class LotSearchForm(FlaskForm):
    lot = StringField('Lot Number')
    recipe = StringField('Recipe')
    submit = SubmitField('Submit')
class DeviceForm(FlaskForm):
    device = StringField('Device', validators=[DataRequired()])
#
# class MasterRecipeDirForm(FlaskForm):
#     choices_single = master_directory_ls()
#     choices_dir_form = [("","")]+[(tic,tic) for tic in choices_single]
#     directory = SelectField("Directory", choices = choices_dir_form)
#     submit = SubmitField('Submit')
#
# class MasterRecipeProductForm(FlaskForm):
#     recipe = SelectField("Recipe")
#     submit = SubmitField('Submit')
#     def __init__(self, master_directory,*args, **kwargs):
#         super(MasterRecipeProductForm, self).__init__(*args, **kwargs)
#         if master_directory:
#             choices_single = FY_ls(master_directory)
#
#             self.recipe.choices = [("","")]+[(tic, tic) for tic in choices_single]
#         else:
#             self.recipe.choices = [('1','1')]
