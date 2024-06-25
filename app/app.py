# app.py

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Counter for task IDs
task_id_counter = 1

# List to store tasks
tasks = []

# Function to generate a new task ID
def generate_task_id():
    global task_id_counter
    task_id = task_id_counter
    task_id_counter += 1
    return task_id

# Route to render index.html with tasks data
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

# Route to render add_task.html for adding new task
@app.route('/task/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        global task_id_counter
        task_id = generate_task_id()
        new_task = {
            'id': task_id,
            'title': request.form['title'],
            'description': request.form['description'],
            'due_date': request.form['due_date']
        }
        tasks.append(new_task)
        flash('Task added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_task.html')

# Route to render task_detail.html for displaying a single task
@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return render_template('task_detail.html', task=task)
    else:
        flash('Task not found!', 'error')
        return redirect(url_for('index'))

# Route to render edit_task.html for editing an existing task
@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        flash('Task not found!', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        task['title'] = request.form['title']
        task['description'] = request.form['description']
        task['due_date'] = request.form['due_date']
        flash('Task updated successfully!', 'success')
        return redirect(url_for('task_detail', task_id=task['id']))
    
    return render_template('edit_task.html', task=task)

# Route to delete a task
@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
