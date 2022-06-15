from flask import Blueprint, render_template, request
from ..ctasks import get_unique_id_with_delay

tasks_bp = Blueprint('tasks_bp', __name__, template_folder='../templates/tasks', url_prefix='/tasks')


@tasks_bp.route('/')
def tasks():
    '''display active tasks, option to create new task or enter results page'''    
    # CREATE NEW TASK
    return render_template('tasks.html')


@tasks_bp.route('/results/', methods=['POST'])
def results():
    if request.method == 'POST':
        # get time, pass to task, pass result to results.html
        delay = int(request.form['delay'])
        get_unique_id_with_delay(delay)
        
        # something = celery_in.apply(get_unique_id_with_delay, delay=delay)
        # result = get_unique_id_with_delay(delay=delay)
        something = 'boo'
        return render_template('results.html', result=something)
