from flask import Blueprint, render_template, redirect, url_for, current_app, flash
from app.forms import CaseForm
from app.models import Case
from app import db
import openai

bp = Blueprint('main', __name__)

@bp.route('/')
def welcome():
    current_app.logger.info("Accediendo a la página de bienvenida.")
    return render_template('welcome.html')

@bp.route('/create_case', methods=['GET', 'POST'])
def create_case():
    form = CaseForm()
    if form.validate_on_submit():
        current_app.logger.info("Formulario de caso clínico enviado.")
        # Recopilar datos del formulario
        name = form.name.data
        age = form.age.data
        gender = form.gender.data
        event_location = form.event_location.data
        traumatic_event = ', '.join(form.traumatic_event.data)  # Convertir lista a cadena
        scenario = ', '.join(form.scenario.data)  # Convertir lista a cadena
        openness = form.openness.data
        conscientiousness = form.conscientiousness.data
        extraversion = form.extraversion.data
        agreeableness = form.agreeableness.data
        neuroticism = form.neuroticism.data
        additional_features = form.additional_features.data
        improvise = form.improvise.data

        # Crear objeto Case
        case = Case(
            name=name,
            age=age,
            gender=gender,
            event_location=event_location,
            traumatic_event=traumatic_event,
            scenario=scenario,
            openness=openness,
            conscientiousness=conscientiousness,
            extraversion=extraversion,
            agreeableness=agreeableness,
            neuroticism=neuroticism,
            additional_features=additional_features,
            improvise=improvise
        )

        db.session.add(case)
        db.session.commit()
        current_app.logger.info(f"Caso clínico añadido a la base de datos: {case.name}")

        # Llamar a la API de OpenAI para generar la narrativa
        current_app.logger.info(f"Generando narrativa para el caso: {case.name}")
        narrative = generate_narrative(case)

        if narrative.startswith("Error"):
            flash(narrative, 'danger')
            return redirect(url_for('main.create_case'))

        # Guardar la narrativa en la base de datos
        case.narrative = narrative
        db.session.commit()
        current_app.logger.info(f"Narrativa generada y guardada para el caso: {case.name}")

        # Registrar éxito en los logs
        current_app.logger.info(f"Caso clínico generado exitosamente para {case.name}")

        flash('Caso clínico generado exitosamente.', 'success')
        return redirect(url_for('main.case_generated', case_id=case.id))

    current_app.logger.info("Mostrando formulario de creación de caso clínico.")
    return render_template('create_case.html', form=form)

@bp.route('/case_generated/<int:case_id>')
def case_generated(case_id):
    current_app.logger.info(f"Accediendo a la narrativa del caso ID: {case_id}")
    case = Case.query.get_or_404(case_id)
    return render_template('case_generated.html', case=case)

def generate_narrative(case):
    openai.api_key = current_app.config['OPENAI_API_KEY']
    current_app.logger.debug(f"Clave de API de OpenAI configurada: {openai.api_key}")

    # Crear los mensajes para ChatGPT
    messages = [
        {"role": "system", "content": "Eres un asistente que ayuda a generar casos clínicos detallados."},
        {"role": "user", "content": f"""
        Crea un caso clínico detallado basado en las siguientes características:
        Nombre del Paciente: {case.name}
        Edad: {case.age}
        Género: {case.gender}
        Lugar del Evento: {case.event_location}
        Tipo de Evento Traumático: {case.traumatic_event}
        Escenario a Resolver: {case.scenario}
        Rasgos de Personalidad:
          - Apertura: {case.openness}
          - Escrupulosidad: {case.conscientiousness}
          - Extraversión: {case.extraversion}
          - Amabilidad: {case.agreeableness}
          - Neuroticismo: {case.neuroticism}
        Características Adicionales: {case.additional_features}
        """}
    ]

    if case.improvise:
        messages.append({"role": "user", "content": "Además, improvisa características adicionales que puedan enriquecer el caso clínico."})

    try:
        current_app.logger.info("Enviando solicitud a la API de OpenAI.")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        current_app.logger.debug(f"Respuesta de OpenAI: {response}")
        narrative = response.choices[0].message['content'].strip()
        current_app.logger.info("Narrativa generada exitosamente.")
        return narrative

    except openai.error.OpenAIError as e:
        # Registrar el error en los logs
        current_app.logger.error(f"OpenAI API error: {e}")
        return "Error al generar el caso clínico. Por favor, inténtalo de nuevo."
