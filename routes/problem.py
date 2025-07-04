import datetime

from flask import Blueprint,  render_template, request,  redirect, g, abort, url_for
from auth import login_session_required
from models import ProblemManagement, db

problem_bp = Blueprint('problem', __name__)

@problem_bp.route('/', methods=['GET'])
@login_session_required
def problem_list():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    problems  = ProblemManagement.query.all()


    return render_template('problem_list.html', problems=problems)


@problem_bp.route('/create', methods=['GET', 'POST'])
@login_session_required
def create_problem():
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    if request.method == 'POST':
        title = request.form['name']
        description = request.form['description']
        status = request.form['status']
        priority = request.form['priority']
        impact = request.form['impact']
        assignee_id = request.form['assignee_id']
        created_id = request.form['created_id']
        root_cause = request.form['root_cause']
        incident_id = request.form['incident_id']
        resolution = request.form['incident_id']



        # DB transaction
        try:
            with db.session.begin(nested=True):
                problem = ProblemManagement(
                    title = title,
                    description = description,
                    status = status,
                    priority = priority,
                    impact = impact,
                    assignee_id =  assignee_id,
                    created_id = created_id,
                    root_cause =  root_cause,
                    resolution = resolution,
                    incident_id = incident_id,
                    created_at = datetime.datetime.now(datetime.timezone.utc),
                    updated_at =datetime.datetime.now(datetime.timezone.utc),
                )
                db.session.add(problem)

                db.session.commit()
                return redirect(url_for('problem.problem_list'))
        except Exception as e:
            db.session.rollback()
            print(e)






    return render_template('create_problem.html')

@problem_bp.route('/<int:problem_id>/edit', methods=['GET', 'POST'])
@login_session_required
def edit_problem(problem_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)
    problem = ProblemManagement.query.get_or_404(problem_id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status'],
        priority = request.form['priority'],
        impact = request.form['impact'],
        assignee_id = request.form['assignee_id'],
        created_id = request.form['created_id'],
        root_cause = request.form['root_cause'],
        resolution = request.form['resolution'],
        incident_id = request.form['incident_id']

        # DB transaction
        try:
            with db.session.begin(nested=True):# Due to two transactions so need the nested  to allow the second.
                #update problem
                problem.title = title
                problem.description = description
                problem.status = status,
                problem.priority = priority,
                problem.impact = impact,
                problem.assignee_id = assignee_id,
                problem.created_id = created_id,
                problem.root_cause = root_cause,
                problem.resolution = resolution,
                problem.incident_id = incident_id,
                problem.updated_at = datetime.datetime.now(datetime.timezone.utc)

                db.session.commit() # gets user.id

                return redirect(url_for('problem.problem_list'))

        except Exception as e:
            db.session.rollback()
            print('Could not find the problem ' + str(problem_id))
            print(e)
# if  using get it wil drop to this section
    return render_template('create_problem.html',problem=problem)

@problem_bp.route('/<int:problem_id>/delete', methods=['POST'])
@login_session_required
def delete_problem(problem_id):
    if 'VIEW_ADMIN' not in g.permissions:
        return abort(403)

    #Update problem
    ProblemManagement.query.filter_by(id= problem_id).delete()
    db.session.commit()# commit the change


    return redirect(url_for('problem.problem_list'))