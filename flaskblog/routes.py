import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                              PostForm, RequestResetForm, ResetPasswordForm, TopicForm)
from flaskblog.models import User, Post, Topic, TopicPosts, Comments
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message





@app.route("/")
@app.route("/home")
def home():
    page= request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/topics")
def topics():
    page= request.args.get('page', 1, type=int)
    posts = Topic.query.order_by(Topic.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('topics.html', posts=posts)


@app.route("/your_topic/<int:topic_id>")
def your_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    return render_template('area.html', post = topic)


@app.route("/topic_posts")
def topic_posts():
    page= request.args.get('page', 1, type=int)

    topic_id = int(request.args.get('topic_id'))

    posts = TopicPosts.query.order_by(TopicPosts.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('topic_posts.html', posts=posts, topic_id=topic_id)



@app.route('/new_topic', methods=['GET', 'POST'])
def new_topic():
    form = TopicForm()
    if current_user.username != 'admin' and current_user.username != 'admin123':
        return redirect(url_for('home'))
    if form.validate_on_submit():
        topic = Topic(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(topic)
        db.session.commit()
        flash('New topic has been created!', 'success')
        return redirect(url_for('topics'))
    return render_template('create_topic.html', title='Create a topic',
                           form=form, legend='New Topic')
    


@app.route("/topic_post", methods=['GET', 'POST'])
@login_required
def topic_post():
    form = PostForm()
    topic_id = request.args.get('topic_id') 
    if form.validate_on_submit():
        
        post = TopicPosts(title=form.title.data, content=form.content.data, topic_id = topic_id, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('topics'))
    return render_template('create_topic_post.html', title='New Topic Post',
                           form=form, legend='New Topic Post', topic_id=topic_id)


@app.route("/your_topic_post/<int:post_id>")
def your_topic_post(post_id):
    post = TopicPosts.query.get_or_404(post_id)
    return render_template('topic_post.html', title=post.title, post=post)



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)




@app.route("/comments")
def comments():
    page= request.args.get('page', 1, type=int)

    post_id = int(request.args.get('post_id'))

    posts = Comments.query.order_by(Comments.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('comments.html', posts=posts, post_id=post_id)



@app.route("/edit_comment/<int:post_id>")
def edit_comment(post_id):
    post = Comments.query.get_or_404(post_id)
    return render_template('edit_comment.html', title=post.title, post=post)



@app.route("/new_comment", methods=['GET', 'POST'])
@login_required
def new_comment():
    form = PostForm()
    post_id = request.args.get('post_id') 
    if form.validate_on_submit():
        
        post = Comments(title=form.title.data, content=form.content.data, post_id = post_id, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_comment.html', title='New Topic Post',
                           form=form, legend='New Topic Post', post_id=post_id)



@app.route("/post/<int:post_id>/update_topic", methods=['GET', 'POST'])
@login_required
def update_topic(post_id):
    post = Topic.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Topic has been updated!', 'success')
        return redirect(url_for('topics'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')




@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_topic_post(post_id):
    post = TopicPosts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('topic_posts', topic_id=post.topic_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/private_area")
def private_area():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    # SQL query to fetch private areas ordered by date
    sql_query = text("""
        SELECT id, title, date_posted, content, user_id
        FROM private_area
        ORDER BY date_posted DESC
    """)

    access_query = text("""
        SELECT *
        FROM private_area_user
     
    """)
    group_members = db.session.execute(access_query).fetchall()
    # Execute the SQL query with pagination
    areas = db.session.execute(sql_query, {'per_page': per_page, 'offset': (page-1)*per_page}).fetchall()
    
  
    return render_template('private_area.html', areas=areas, group_members= group_members)



@app.route("/add_user_to_private_area", methods=['GET','POST'])
def add_user_to_private_area():
    if request.args.get('area_id') is None:
        return redirect(url_for('private_area'))

    area_id = int(request.args.get('area_id'))

    # Check if the current user is authorized to perform this action
    if current_user.username not in ['admin', 'admin123']:
        flash('You are not authorized to perform this action!', 'danger')
        return redirect(url_for('private_area'))

    # Get the username from the form submission
    username = request.form.get('username')

    # Query the user table to find the corresponding user ID
    user_query = text("""
        SELECT id FROM "user" WHERE username = :username
    """)
    user_result = db.session.execute(user_query, {'username': username}).fetchone()

    if not user_result:
        flash('User not found!', 'danger')
        return redirect(url_for('private_area'))

    user_id = user_result.id

    # Get the private area ID from the form or from the session, depending on how it's implemented
    check_query = text("""
    SELECT id
    FROM private_area_user
    WHERE private_area_id = :private_area_id AND user_id = :user_id
    """)
    result = db.session.execute(check_query, {'private_area_id': area_id, 'user_id': user_id}).fetchone()

    if result is not None:
        flash('User is already in the area!', 'error')
        return redirect(url_for('private_area'))

    # Insert the new record into the private_area_user table
    insert_query = text("""
        INSERT INTO private_area_user (private_area_id, user_id)
        VALUES (:private_area_id, :user_id)
    """)
    db.session.execute(insert_query, {'private_area_id': area_id, 'user_id': user_id})
    db.session.commit()

    flash('User added to private area successfully!', 'success')
    return redirect(url_for('private_area'))





@app.route('/new_private_area', methods=['GET', 'POST'])
def new_private_area():
    form = TopicForm()
    if current_user.username != 'admin' and current_user.username != 'admin123':
        return redirect(url_for('home'))
    if form.validate_on_submit():
        sql_query = text("""
            INSERT INTO private_area (title, content, user_id, date_posted) 
            VALUES (:title, :content, :user_id, :date_posted)
        """)
        db.session.execute(sql_query, {
            'title': form.title.data,
            'content': form.content.data,
            'user_id': current_user.id,
            'date_posted': datetime.utcnow()
        })
        db.session.commit()
        flash('New private topic has been created!', 'success')
        return redirect(url_for('private_area'))
    return render_template('create_topic.html', title='Create a topic',
                           form=form, legend='New Topic')





@app.route("/post/<int:area_id>/delete_private_area", methods=['POST'])
@login_required
def delete_private_area(area_id):
    # Fetch all posts belonging to the private area
    posts_query = text("""
        SELECT id
        FROM private_area_posts
        WHERE private_area_id = :area_id
    """)
    posts = db.session.execute(posts_query, {'area_id': area_id}).fetchall()

    # Delete each post and its associated comments
    for post in posts:
        post_id = post.id 
        
        # Delete the post
        delete_post_query = text("""
            DELETE FROM private_area_posts
            WHERE id = :post_id
        """)
        db.session.execute(delete_post_query, {'post_id': post_id})

        # Delete associated comments
        delete_comments_query = text("""
            DELETE FROM private_area_post_comments
            WHERE private_area_post_id = :post_id
        """)
        db.session.execute(delete_comments_query, {'post_id': post_id})

    delete_user_area_query = text("""
        DELETE FROM private_area_user
        WHERE private_area_id = :area_id
    """)
    db.session.execute(delete_user_area_query, {'area_id': area_id})

    area_query = text("""
            DELETE FROM private_area
            WHERE id = :area_id
        """)
    db.session.execute(area_query, {'area_id': area_id})

    

    db.session.commit()


    flash('Your private area, its posts, and their comments have been deleted!', 'success')
    return redirect(url_for('private_area'))



@app.route("/post/<int:post_id>/update_post", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/updatecomment", methods=['GET', 'POST'])
@login_required
def update_comment(post_id):
    post = Comments.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('topics'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete_area", methods=['POST'])
@login_required
def delete_area(post_id):
    topic = Topic.query.get_or_404(post_id)
    
    if topic.author != current_user:
        abort(403)


    TopicPosts.query.filter_by(topic_id=topic.id).delete()
    db.session.delete(topic)
    db.session.commit()
    flash('Your topic has been deleted!', 'success')
    return redirect(url_for('topics'))


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_topic_post(post_id):
    post = TopicPosts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your topic post has been deleted!', 'success')
    return redirect(url_for('topics'))



@app.route("/post/<int:post_id>/delete_post", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    Comments.query.filter_by(post_id=post_id).delete()
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/post/<int:post_id>/delete_comment", methods=['POST'])
@login_required
def delete_comment(post_id):
    post = Comments.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('home'))



@app.route("/user/<string:username>")
def user_posts(username):
    page= request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
     if current_user.is_authenticated:
        return redirect(url_for('home'))
     user =  User.verify_reset_token(token)
     if user is None:
         flash('That is an invalid or expired token', 'warning')
         return redirect(url_for('reset_request'))
     form = ResetPasswordForm()
     if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login')) 
     return render_template('reset_token.html', title='Reset Password', form=form)
