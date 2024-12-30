from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Load data
data_file = 'hackerman.csv'  # Replace with your actual results file
if os.path.exists(data_file):
    data = pd.read_csv(data_file)
else:
    data = pd.DataFrame(columns=["username", "name", "url_main", "http_status"])

@app.route('/')
def home():
    usernames = data['username'].unique()
    return render_template('index.html', usernames=usernames)

@app.route('/results', methods=['POST'])
def results():
    username = request.form.get('username')

    # Filter data for the selected username
    user_data = data[data['username'] == username]

    # Generate a bar plot 
    plot_file = f'static/{username}_plot.png'
    site_counts = user_data['name'].value_counts()
    site_counts.plot(kind='bar', figsize=(10, 6), color='skyblue', title=f'Name Occurrences for {username}')
    plt.xlabel("Sites")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()

    return render_template('results.html', username=username, table=user_data.to_html(classes='table table-striped'), plot_file=plot_file)

if __name__ == '__main__':
    app.run(debug=True)
