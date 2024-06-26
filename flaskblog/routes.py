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
from sqlalchemy import text
from datetime import datetime
from collections import defaultdict



@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    # SQL query to fetch private areas ordered by date
    sql_query = text("""
        SELECT t.id, t.title, t.date_posted, t.content, t.user_id, u.image_file, u.username
        FROM topic t
        JOIN "user" u ON t.user_id = u.id
        ORDER BY t.date_posted DESC
    """)

    
    # Execute the SQL query with pagination
    posts = db.session.execute(sql_query, {'per_page': per_page, 'offset': (page-1)*per_page}).fetchall()
    total_posts_count = 0
    total_comments = 0

    topic_post_counts = {}
    topic_comment_counts = {}

    # Loop through topics to count total comments for each post
    for post in posts:
        topic_id = post.id

        # SQL query to count total comments for the topic
        sql_query_comments = text("""
            SELECT COUNT(*) AS num_posts
            FROM topic_posts tp
            WHERE tp.topic_id = :topic_id
        """)

        sql_real_comments = text("""
            SELECT *
            FROM topic_posts tp
            WHERE tp.topic_id = :topic_id """)


        post_posts_result = db.session.execute(sql_query_comments, {'topic_id': topic_id}).fetchone()
        num_posts = post_posts_result.num_posts if post_posts_result else 0
        total_posts_count += num_posts

        topic_post_counts[topic_id] = num_posts

        comments = db.session.execute(sql_real_comments, {'topic_id': topic_id}).fetchall()
        for comment in comments:
            topic_post_id = comment.id

            sql_querya_comments = text("""
            SELECT COUNT(*) AS num_comments
            FROM topic_post_comments tpc
            WHERE tpc.topic_post_id = :topic_post_id
             """)
            
            comment_result = db.session.execute(sql_querya_comments, {'topic_post_id': topic_post_id}).fetchone()
            num_comments = comment_result.num_comments if comment_result else 0
            total_comments += num_comments

            if topic_id in topic_comment_counts:
                topic_comment_counts[topic_id] += num_comments
            else:
                topic_comment_counts[topic_id] = num_comments
            
    
    
  
    return render_template('home.html', posts=posts, total_posts_count=total_posts_count,
                            total_comments=total_comments, topic_post_counts=topic_post_counts, topic_comment_counts=topic_comment_counts)
    
  
    



@app.route("/about")
def about():
    return render_template('about.html', title='About')




@app.route("/topics")
def topics():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    # SQL query to fetch private areas ordered by date
    sql_query = text("""
        SELECT t.id, t.title, t.date_posted, t.content, t.user_id, u.image_file, u.username
        FROM topic t
        JOIN "user" u ON t.user_id = u.id
        ORDER BY t.date_posted DESC
    """)

    # Execute the SQL query with pagination
    posts = db.session.execute(sql_query, {'per_page': per_page, 'offset': (page-1)*per_page}).fetchall()

    total_posts_count = 0
    total_comments = 0

    topic_post_counts = {}
    topic_comment_counts = {}

    # Loop through topics to count total comments for each post
    for post in posts:
        topic_id = post.id

        # SQL query to count total comments for the topic
        sql_query_comments = text("""
            SELECT COUNT(*) AS num_posts
            FROM topic_posts tp
            WHERE tp.topic_id = :topic_id
        """)

        sql_real_comments = text("""
            SELECT *
            FROM topic_posts tp
            WHERE tp.topic_id = :topic_id """)


        post_posts_result = db.session.execute(sql_query_comments, {'topic_id': topic_id}).fetchone()
        num_posts = post_posts_result.num_posts if post_posts_result else 0
        total_posts_count += num_posts

        topic_post_counts[topic_id] = num_posts

        comments = db.session.execute(sql_real_comments, {'topic_id': topic_id}).fetchall()
        for comment in comments:
            topic_post_id = comment.id

            sql_querya_comments = text("""
            SELECT COUNT(*) AS num_comments
            FROM topic_post_comments tpc
            WHERE tpc.topic_post_id = :topic_post_id
             """)
            
            comment_result = db.session.execute(sql_querya_comments, {'topic_post_id': topic_post_id}).fetchone()
            num_comments = comment_result.num_comments if comment_result else 0
            total_comments += num_comments

            if topic_id in topic_comment_counts:
                topic_comment_counts[topic_id] += num_comments
            else:
                topic_comment_counts[topic_id] = num_comments
            
    
    
  
    return render_template('topics.html', posts=posts, total_posts_count=total_posts_count,
                            total_comments=total_comments, topic_post_counts=topic_post_counts, topic_comment_counts=topic_comment_counts)


@app.route("/your_topic/<int:topic_id>")
def your_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    return render_template('area.html', post = topic)


@app.route("/topic_posts")
def topic_posts():
    
    topic_id = int(request.args.get('topic_id'))
   
    

    sql_query = text("""
        SELECT tp.id, tp.title, tp.date_posted, tp.content, tp.user_id, u.username, u.image_file
        FROM topic_posts tp
        JOIN "user" u ON tp.user_id = u.id
        WHERE tp.topic_id = :topic_id
        ORDER BY tp.date_posted DESC
       
    """)

    sql_query_comments = text("""
    SELECT COUNT(*) as num_comments
    FROM topic_post_comments tpc
    WHERE tpc.topic_id = :topic_id AND tpc.topic_post_id = :post_id
    """)

   
    topic = db.session.execute(sql_query, {'topic_id': topic_id}).fetchall()

    total_comments_count = 0


    for post in topic:
        post_id = post.id
        post_comments_result = db.session.execute(sql_query_comments, {'topic_id': topic_id, 'post_id': post_id}).fetchone()
        num_comments = post_comments_result.num_comments if post_comments_result else 0
        total_comments_count += num_comments
        

    
    return render_template('topic_posts.html', topic=topic, total_comments_count=total_comments_count, topic_id=topic_id)


@app.route("/search_topic_posts", methods=["POST"])
@login_required
def search_topic_posts():
    # Extract the search input from the form
    search_input = request.form.get("post_name")

    # Construct the SQL query to search for posts
    sql_query = """
        SELECT id, title, date_posted, content, topic_id, user_id
        FROM topic_posts
        WHERE title ILIKE :search_input
    """


    # Execute the query with the search input
    matching_posts = db.session.execute(text(sql_query), {"search_input": search_input + "%"}).fetchall()

    # Pass the matching posts to the template for rendering
    return render_template("search_topic_results.html", matching_posts=matching_posts)




@app.route('/new_topic', methods=['GET', 'POST'])
def new_topic():
    form = TopicForm()
    if current_user.username != 'admin' and current_user.username != 'admin123':
        return redirect(url_for('home'))
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        date_posted = datetime.utcnow()
        
       
        sql_query = text("""
            INSERT INTO topic (title, content, user_id, date_posted)
            VALUES (:title, :content, :user_id, :date_posted)
        """)
        
       
        db.session.execute(sql_query, {'title': title, 'content': content, 'user_id': user_id, 'date_posted': date_posted})
        db.session.commit()
        
        flash('New topic has been created!', 'success')
        return redirect(url_for('topics'))
    
    return render_template('create_topic.html', title='Create a topic',
                           form=form, legend='New Topic')

    


@app.route("/new_topic_post", methods=['GET', 'POST'])
@login_required
def new_topic_post():
    form = PostForm()
    topic_id = request.args.get('topic_id') 
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        date_posted = datetime.utcnow()  # Get the current datetime
        
        # SQL query to insert a new topic post into the database
        sql_query = text("""
            INSERT INTO topic_posts (title, content, topic_id, user_id, date_posted)
            VALUES (:title, :content, :topic_id, :user_id, :date_posted)
        """)
        
        # Execute the SQL query with the provided data
        db.session.execute(sql_query, {'title': title, 'content': content, 'topic_id': topic_id, 'user_id': user_id, 'date_posted': date_posted})
        db.session.commit()
        
        flash('Your topic-post has been created!', 'success')
        return redirect(url_for('topics'))
    
    return render_template('create_topic_post.html', title='New Topic Post',
                           form=form, legend='New Topic Post', topic_id=topic_id)


@app.route("/topic_post_comments/<int:post_id>")
def topic_post_comments(post_id):
    sql_query = text("""
        SELECT tpc.id, tpc.topic_post_id, tpc.title, tpc.date_posted, tpc.content, tpc.user_id, u.username, u.image_file
        FROM topic_post_comments tpc
        JOIN "user" u ON tpc.user_id = u.id
        WHERE tpc.topic_post_id = :post_id
        ORDER BY tpc.date_posted DESC
    """)

    sql_quera = text("""
        SELECT tp.id, tp.title, tp.date_posted, tp.content, tp.user_id, tp.topic_id, u.username, u.image_file
        FROM topic_posts tp
        JOIN "user" u ON tp.user_id = u.id
        WHERE tp.id = :post_id
        """)
    
    post = db.session.execute(sql_quera, {'post_id': post_id}).fetchone()


    
    comments = db.session.execute(sql_query, {'post_id': post_id}).fetchall()
    
    return render_template('topic_post_comments.html', comments=comments, post_id = post_id, post= post)



@app.route("/topic_post_comment")
def topic_post_comment():

    comment_id = int(request.args.get('comment_id'))

    sql_query = text("""
        SELECT id, title, date_posted, content, user_id, topic_post_id, topic_id
        FROM topic_post_comments
        WHERE id = :comment_id
    """)

    comment_info = db.session.execute(sql_query, {'comment_id': comment_id}).fetchone()

    return render_template('topic_comment.html', comment_info=comment_info)






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
    if current_user.username != 'admin' and current_user.username != 'admin123':
        return redirect(url_for('home'))
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


@app.route("/private_area_posts")
def private_area_posts():
    area_id = int(request.args.get('area_id'))
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    # SQL query to fetch private areas ordered by date
    sql_query = text("""
        SELECT id, title, date_posted, content, user_id, private_area_id
        FROM private_area_posts
        ORDER BY date_posted DESC
        
    """)
    
    # Execute the SQL query with pagination
    areas = db.session.execute(sql_query, {'per_page': per_page, 'offset': (page-1)*per_page}).fetchall()
    print(areas)
    return render_template('private_area_posts.html', areas=areas, area_id=area_id)



@app.route("/search_private_posts", methods=["POST"])
@login_required
def search_private_posts():
    # Extract the search input from the form
    search_input = request.form.get("post_name")

    # Construct the SQL query to search for posts
    sql_query = """
        SELECT id, title, date_posted, content, private_area_id, user_id
        FROM private_area_posts
        WHERE title ILIKE :search_input
    """


    # Execute the query with the search input
    matching_posts = db.session.execute(text(sql_query), {"search_input": search_input + "%"}).fetchall()

    # Pass the matching posts to the template for rendering
    return render_template("search_results.html", matching_posts=matching_posts)





@app.route('/new_private_area_post', methods=['GET', 'POST'])
def new_private_area_post():
    form = TopicForm()
    
    if form.validate_on_submit():
        area_id = request.args.get('area_id')
        sql_query = text("""
            INSERT INTO private_area_posts (title, content, user_id, date_posted, private_area_id ) 
            VALUES (:title, :content, :user_id, :date_posted, :private_area_id)
        """)
        db.session.execute(sql_query, {
            'title': form.title.data,
            'content': form.content.data,
            'user_id': current_user.id,
            'private_area_id': area_id,
            'date_posted': datetime.utcnow()
        })
        db.session.commit()
        flash('New private topic-post has been created!', 'success')
        return redirect(url_for('private_area'))
    return render_template('create_topic.html', title='Create a topic',
                           form=form, legend='New Topic')




@app.route("/post/<int:comment_id>/update_private_post", methods=['GET', 'POST'])
@login_required
def update_private_post(comment_id):
    # Fetch the post from the database
    post_query = text("""
        SELECT id, title, content, private_area_id, user_id
        FROM private_area_posts
        WHERE id = :comment_id
    """)
    comment = db.session.execute(post_query, {'comment_id': comment_id}).fetchone()

    # Check if the post exists and if the current user is the author
    if not comment:
        abort(404)  # Post not found
    if comment.user_id != current_user.id:
        abort(403)  # Forbidden, user is not the author

    form = PostForm()
    if form.validate_on_submit():
        # Update the post with data from the form
        update_query = text("""
            UPDATE private_area_posts
            SET title = :title, content = :content
            WHERE id = :comment_id
        """)
        db.session.execute(update_query, {'title': form.title.data, 'content': form.content.data, 'comment_id': comment_id})
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('private_area'))
    elif request.method == 'GET':
        # Pre-populate the form with post data
        form.title.data = comment.title
        form.content.data = comment.content

    return render_template('new_comment.html', title='Update Comment', form=form, legend='Update Post')




@app.route("/post/<int:post_id>/delete_private_post", methods=['POST'])
@login_required
def delete_private_post(post_id):
    post_query = text("""
        SELECT id, user_id
        FROM private_area_posts
        WHERE id = :post_id
    """)
    post = db.session.execute(post_query, {'post_id': post_id}).fetchone()

    if not post:
        abort(404)  
    if post.user_id != current_user.id:
        abort(403)  

    delete_post_query = text("""
        DELETE FROM private_area_posts
        WHERE id = :post_id
    """)

    db.session.execute(delete_post_query, {'post_id': post_id})

    delete_comments_query = text("""
        DELETE FROM private_area_post_comments
        WHERE private_area_post_id = :post_id
    """)

    db.session.execute(delete_comments_query, {'post_id': post_id})

    db.session.commit()

    flash('Your private post and its comments has been deleted!', 'success')
    return redirect(url_for('private_area'))











@app.route("/private_area_comments")
def private_area_comments():
    area_id = int(request.args.get('area_id'))
    area_post_id = int(request.args.get('area_post_id'))
    page = request.args.get('page', 1, type=int)
    per_page = 5
    

    area_query = text("""
        SELECT id, title, date_posted, content, user_id
        FROM private_area_posts
        WHERE id = :area_post_id
    """)
    area_details = db.session.execute(area_query, {'area_post_id': area_post_id}).fetchone()

    # SQL query to fetch private areas ordered by date
    sql_query = text("""
        SELECT id, title, date_posted, content, user_id, private_area_id, private_area_post_id
        FROM private_area_post_comments
        ORDER BY date_posted DESC
        
    """)
    

  
    # Execute the SQL query with pagination
    areas = db.session.execute(sql_query, {'per_page': per_page, 'offset': (page-1)*per_page}).fetchall()
    print(areas)
    return render_template('private_area_comments.html', areas=areas, area_id=area_id, area_post_id = area_post_id, area_details = area_details)



@app.route('/add_private_comment', methods=['GET', 'POST'])
def add_private_comment():
    form = TopicForm()
    
    if form.validate_on_submit():
        area_id = request.args.get('area_id')
        private_area_post_id = request.args.get('post_id')
        
        sql_query = text("""
            INSERT INTO private_area_post_comments (title, content, user_id, date_posted, private_area_id, private_area_post_id) 
            VALUES (:title, :content, :user_id, :date_posted, :private_area_id, :private_area_post_id)
            
        """)
        db.session.execute(sql_query, {
            'title': form.title.data,
            'content': form.content.data,
            'user_id': current_user.id,
            'private_area_id': area_id,
            'private_area_post_id': private_area_post_id,
            'date_posted': datetime.utcnow()
        })
        db.session.commit()
        flash('New private topic-post has been created!', 'success')
        return redirect(url_for('private_area'))
    return render_template('new_comment.html', title='Create a topic',
                           form=form, legend='New Topic')






@app.route("/private_post_comment")
def private_post_comment():

    area_post_comment_id = int(request.args.get('area_post_comment_id'))
   

    sql_query = text("""
        SELECT id, title, date_posted, content, user_id
        FROM private_area_post_comments
        WHERE id = :area_post_comment_id
    """)

    comment_info = db.session.execute(sql_query, {'area_post_comment_id': area_post_comment_id}).fetchone()
   
    return render_template('private_post_comment.html', comment_info=comment_info)





@app.route("/post/<int:comment_id>/update_private_comment", methods=['GET', 'POST'])
@login_required
def update_private_comment(comment_id):
    # Fetch the post from the database
    post_query = text("""
        SELECT id, title, content, private_area_post_id, user_id
        FROM private_area_post_comments
        WHERE id = :comment_id
    """)
    comment = db.session.execute(post_query, {'comment_id': comment_id}).fetchone()

    # Check if the post exists and if the current user is the author
    if not comment:
        abort(404)  # Post not found
    if comment.user_id != current_user.id:
        abort(403)  # Forbidden, user is not the author

    form = PostForm()
    if form.validate_on_submit():
        # Update the post with data from the form
        update_query = text("""
            UPDATE private_area_post_comments
            SET title = :title, content = :content
            WHERE id = :comment_id
        """)
        db.session.execute(update_query, {'title': form.title.data, 'content': form.content.data, 'comment_id': comment_id})
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('private_area'))
    elif request.method == 'GET':
        # Pre-populate the form with post data
        form.title.data = comment.title
        form.content.data = comment.content

    return render_template('new_comment.html', title='Update Comment', form=form, legend='Update Post')




@app.route("/post/<int:comment_id>/delete_private_comment", methods=['POST'])
@login_required
def delete_private_comment(comment_id):
    comment_query = text("""
        SELECT id, user_id
        FROM private_area_post_comments
        WHERE id = :comment_id
    """)
    comment = db.session.execute(comment_query, {'comment_id': comment_id}).fetchone()

    if not comment:
        abort(404)  # Comment not found
    if comment.user_id != current_user.id:
        abort(403)  

    delete_query = text("""
        DELETE FROM private_area_post_comments
        WHERE id = :comment_id
    """)

    db.session.execute(delete_query, {'comment_id': comment_id})
    db.session.commit()

    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('private_area'))






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
    topic_id = request.args.get('topic_id')
    
    if form.validate_on_submit():
        # SQL query to insert a new comment into the topic_post_comments table
        sql_query = text("""
            INSERT INTO topic_post_comments (title, content, date_posted, topic_post_id, topic_id, user_id)
            VALUES (:title, :content, :date_posted, :topic_post_id, :topic_id, :user_id)
        """)

      
        db.session.execute(sql_query, {
            'title': form.title.data,
            'content': form.content.data,
            'date_posted': datetime.utcnow(),
            'topic_post_id': post_id,
            'topic_id': topic_id,  # Assuming you have a variable named 'post' with the topic ID
            'user_id': current_user.id
        })
        db.session.commit()
        
        flash('Your post has been created!', 'success')
        return redirect(url_for('topics'))
    
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
    sql_query_get_post = text("""
        SELECT id, title, content, user_id, topic_id
        FROM topic_posts
        WHERE id = :post_id
    """)

    post = db.session.execute(sql_query_get_post, {'post_id': post_id}).fetchone()

    if not post:
        abort(404)

    if post.user_id != current_user.id:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        sql_query_update_post = text("""
            UPDATE topic_posts
            SET title = :title, content = :content
            WHERE id = :post_id
        """)

        db.session.execute(sql_query_update_post, {'title': form.title.data, 'content': form.content.data, 'post_id': post_id})
        db.session.commit()

        flash('Your post has been updated!', 'success')
        return redirect(url_for('topic_posts', topic_id=post.topic_id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


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


@app.route("/post/<int:comment_id>/updatecomment", methods=['GET', 'POST'])
@login_required
def update_comment(comment_id):
    sql_query = text("""
        SELECT *
        FROM topic_post_comments
        WHERE id = :comment_id
    """)
    
    comment = db.session.execute(sql_query, {'comment_id': comment_id}).fetchone()

    if comment.user_id != current_user.id:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        update_query = text("""
            UPDATE topic_post_comments
            SET title = :title, content = :content
            WHERE id = :comment_id
        """)
        
        db.session.execute(update_query, {'title': form.title.data, 'content': form.content.data, 'comment_id': comment_id})
        db.session.commit()

        flash('Your comment has been updated!', 'success')
        return redirect(url_for('topics'))
    elif request.method == 'GET':
        form.title.data = comment.title
        form.content.data = comment.content

    return render_template('create_post.html', title='Update Comment', form=form, legend='Update Comment')




@app.route("/post/<int:topic_id>/delete_topic", methods=['POST'])
@login_required
def delete_topic(topic_id):
    # Fetch all posts belonging to the private area
    posts_query = text("""
        SELECT id
        FROM topic_posts
        WHERE topic_id = :topic_id
    """)
    posts = db.session.execute(posts_query, {'topic_id': topic_id}).fetchall()

    # Delete each post and its associated comments
    for post in posts:
        post_id = post.id 
        
        # Delete the post
        delete_post_query = text("""
            DELETE FROM topic_posts
            WHERE id = :post_id
        """)
        db.session.execute(delete_post_query, {'post_id': post_id})

        # Delete associated comments
        delete_comments_query = text("""
            DELETE FROM topic_post_comments
            WHERE topic_post_id = :post_id
        """)
        db.session.execute(delete_comments_query, {'post_id': post_id})

    

    area_query = text("""
            DELETE FROM topic
            WHERE id = :topic_id
        """)
    db.session.execute(area_query, {'topic_id': topic_id})

    db.session.commit()


    flash('Your Topic, its posts, and their comments have been deleted!', 'success')
    return redirect(url_for('topics'))


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_topic_post(post_id):
    # Get the topic post to delete
    sql_query_get_post = text("""
        SELECT id, topic_id, user_id
        FROM topic_posts
        WHERE id = :post_id
    """)
    post = db.session.execute(sql_query_get_post, {'post_id': post_id}).fetchone()

    if not post:
        abort(404)


    # Check if the current user is the author of the post
    
    if post.user_id != current_user.id:
        abort(403)

    # Delete the topic post
    sql_query_delete_post = text("""
        DELETE FROM topic_posts
        WHERE id = :post_id
    """)
    db.session.execute(sql_query_delete_post, {'post_id': post_id})

    # Delete associated comments
    sql_query_delete_comments = text("""
        DELETE FROM topic_post_comments
        WHERE topic_post_id = :post_id
    """)
    db.session.execute(sql_query_delete_comments, {'post_id': post_id})

    db.session.commit()

    flash('Your topic post and its associated comments have been deleted!', 'success')
    return redirect(url_for('topics'))




@app.route("/post/<int:post_id>/delete_post", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    #Comments.query.filter_by(post_id=post_id).delete()
    sql_query = text("DELETE FROM comments WHERE post_id = :post_id")
    db.session.execute(sql_query, {"post_id": post_id})

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/post/<int:comment_id>/delete_comment", methods=['POST'])
@login_required
def delete_comment(comment_id):
    sql_query = text("""
        DELETE FROM topic_post_comments
        WHERE id = :comment_id
        AND user_id = :current_user_id
    """)

    result = db.session.execute(sql_query, {'comment_id': comment_id, 'current_user_id': current_user.id})
    db.session.commit()

    if result.rowcount == 0:
        abort(403)

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
