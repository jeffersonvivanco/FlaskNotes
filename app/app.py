from flask import Flask, render_template, redirect, request, url_for
import os
import boto3


bucket_name = 'mypicturesbucket2020'

# Let's use Amazon S3 (store to store images)
s3_client = boto3.client('s3')

# app instance, flask uses __name__ to determine the root path of the app
app = Flask(__name__, static_folder='static', static_url_path='')


@app.route('/')
def hello_world():
    images = s3_client.list_objects_v2(Bucket=bucket_name)
    return render_template('index.html', name='Jeff', images=images['Contents'])


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return redirect('/')
    username = request.form['username']
    return redirect(url_for('home', username=username))


# note: dynamic components can also be defined with a type. For example /user/<int:id>, flask supports int, float & path
@app.route('/home/<username>')
def home(username):
    return render_template('home.html', username=username)


@app.route('/upload-image', methods=['POST'])
def upload_image():
    f = request.files['image-file']
    s3_client.put_object(Body=f, Bucket=bucket_name, ContentType=f.content_type, Key=f.filename)
    return 'done!'


@app.route('/upload-image/<username>', methods=['POST'])
def upload_image_to_username(username):
    f = request.files['image-file']
    s3_client.put_object(Body=f, Bucket=bucket_name, ContentType=f.content_type, Key=username + '/' + f.filename)
    return 'done!'


@app.route('/get-images')
def get_images():
    images = s3_client.list_objects_v2(Bucket=bucket_name)
    return images


@app.route('/get-images/<username>')
def get_images_for_username(username):
    images = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter=username)
    return images


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # server startup, stop app by hitting CTRL - C
    # During development it is convenient to enable debug mode, which activates the debugger and the reloader
    app.run(host='0.0.0.0', port=port, debug=True)
