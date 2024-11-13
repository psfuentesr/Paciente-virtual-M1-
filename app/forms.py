from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class CaseForm(FlaskForm):
    name = StringField('Nombre del Paciente', validators=[DataRequired()])
    age = IntegerField('Edad', validators=[DataRequired(), NumberRange(min=18, max=100)])
    gender = SelectField('Género', choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('No Binario', 'No Binario'), ('Prefiero no decirlo', 'Prefiero no decirlo')], validators=[DataRequired()])
    event_location = StringField('Lugar del Evento', validators=[DataRequired()])
    traumatic_event = SelectMultipleField('Tipo de Evento Traumático', choices=[
        ('Incendio', 'Incendio'),
        ('Asalto', 'Asalto'),
        ('Violación', 'Violación'),
        ('Accidente de Tránsito', 'Accidente de Tránsito'),
        ('Terremoto', 'Terremoto'),
        ('Convulsión Social', 'Convulsión Social'),
        ('Terrorismo', 'Terrorismo'),
        ('Otro', 'Otro')
    ], validators=[DataRequired()])
    scenario = SelectMultipleField('Escenario a Resolver', choices=[
        ('Paciente en Shock', 'Paciente en Shock'),
        ('Paciente Agitado', 'Paciente Agitado'),
        ('Paciente No Coopera', 'Paciente No Coopera'),
        ('Paciente Pide Ayuda para Tercero', 'Paciente Pide Ayuda para Tercero'),
        ('Paciente Sin Red de Apoyo', 'Paciente Sin Red de Apoyo'),
        ('Otro', 'Otro')
    ], validators=[DataRequired()])
    openness = IntegerField('Apertura (0-10)', validators=[DataRequired(), NumberRange(min=0, max=10)])
    conscientiousness = IntegerField('Escrupulosidad (0-10)', validators=[DataRequired(), NumberRange(min=0, max=10)])
    extraversion = IntegerField('Extraversión (0-10)', validators=[DataRequired(), NumberRange(min=0, max=10)])
    agreeableness = IntegerField('Amabilidad (0-10)', validators=[DataRequired(), NumberRange(min=0, max=10)])
    neuroticism = IntegerField('Neuroticismo (0-10)', validators=[DataRequired(), NumberRange(min=0, max=10)])
    additional_features = TextAreaField('Características Adicionales')
    improvise = BooleanField('¿Desea que ChatGPT improvise características adicionales?')
    submit = SubmitField('Generar Caso Clínico')