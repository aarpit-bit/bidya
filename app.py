from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory data structures for events and registrations
events = []
registrations = {}

# Route to show the homepage (list of events)
@app.route('/')
def index():
    return render_template('index.html', events=events)

# Route to create a new event
@app.route('/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        event_name = request.form['name']
        event_date = request.form['date']
        event_description = request.form['description']
        
        # Add the new event to the events list
        events.append({
            'name': event_name,
            'date': event_date,
            'description': event_description
        })
        
        flash('Event created successfully!')
        return redirect(url_for('index'))
    
    return render_template('create_event.html')

# Route to view event details and register for the event
@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = events[event_id]
    
    if request.method == 'POST':
        user_name = request.form['name']
        
        # Add registration to the registrations dictionary
        if event_id not in registrations:
            registrations[event_id] = []
        registrations[event_id].append(user_name)
        
        flash('Registered successfully!')
        return redirect(url_for('event_detail', event_id=event_id))
    
    event_registrations = registrations.get(event_id, [])
    return render_template('event_detail.html', event=event, event_id=event_id, registrations=event_registrations)

# Route to delete an event
@app.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    # Remove the event from the events list
    if 0 <= event_id < len(events):
        del events[event_id]
        
        # Also remove the associated registrations if any
        registrations.pop(event_id, None)
        
        flash('Event deleted successfully!')
    
    return redirect(url_for('index'))

# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5070,debug=True)
