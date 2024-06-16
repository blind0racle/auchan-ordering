from flask import Flask, request, render_template

app = Flask(__name__)

# Dummy data for worker authentication
workers = [{'email': 'worker1@example.com', 'password': 'password1', 'id': '1'},
           {'email': 'worker2@example.com', 'password': 'password2', 'id': '2'}]


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        worker_id = request.form.get('worker_id')

        if email and password:
            worker = next((worker for worker in workers if worker['email'] == email and worker['password'] == password),
                          None)
            if worker:
                return f'Logged in as {email} (Worker ID: {worker["id"]})'
            return 'Invalid email or password'

        if worker_id:
            worker = next((worker for worker in workers if worker['id'] == worker_id), None)
            if worker:
                return f'Logged in as Worker ID: {worker_id} (Email: {worker["email"]})'
            return 'Invalid worker ID'

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
