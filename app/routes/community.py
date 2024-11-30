from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import ForumPost, Comment, User, Event, Product, ProductReview
from datetime import datetime

bp = Blueprint('community', __name__)

# Forum routes
@bp.route('/forum')
def forum():
    # Get all forum posts with author info and comment count
    posts = db.session.query(
        ForumPost,
        User.username,
        db.func.count(Comment.id).label('comment_count')
    ).join(User, ForumPost.user_id == User.id)\
     .outerjoin(Comment, ForumPost.id == Comment.post_id)\
     .group_by(ForumPost.id, User.username)\
     .order_by(ForumPost.created_at.desc())\
     .all()
    
    return render_template('community/forum.html', posts=posts)

@bp.route('/forum/post/<int:post_id>')
def view_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id)\
        .order_by(Comment.created_at.asc()).all()
    
    return render_template('community/post.html', post=post, comments=comments)

@bp.route('/forum/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        
        if not title or not content or not category:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('community.create_post'))
        
        post = ForumPost(
            user_id=current_user.id,
            title=title,
            content=content,
            category=category
        )
        
        db.session.add(post)
        db.session.commit()
        
        # Award points for creating a post
        current_user.add_points(50)
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('community.forum'))
    
    return render_template('community/create_post.html')

@bp.route('/forum/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = ForumPost.query.get_or_404(post_id)
    content = request.form.get('content')
    
    if not content:
        flash('Comment cannot be empty', 'error')
        return redirect(url_for('community.view_post', post_id=post_id))
    
    comment = Comment(
        user_id=current_user.id,
        post_id=post_id,
        content=content
    )
    
    db.session.add(comment)
    db.session.commit()
    
    # Award points for commenting
    current_user.add_points(10)
    
    flash('Comment added successfully!', 'success')
    return redirect(url_for('community.view_post', post_id=post_id))

@bp.route('/forum/categories')
def categories():
    # Get posts grouped by category with counts
    categories = db.session.query(
        ForumPost.category,
        db.func.count(ForumPost.id).label('post_count')
    ).group_by(ForumPost.category).all()
    
    return render_template('community/categories.html', categories=categories)

@bp.route('/forum/category/<category>')
def view_category(category):
    posts = ForumPost.query.filter_by(category=category)\
        .order_by(ForumPost.created_at.desc()).all()
    
    return render_template('community/category.html',
                         category=category,
                         posts=posts)

# Event routes
@bp.route('/events')
def events():
    upcoming_events = Event.query.filter(
        Event.date > datetime.utcnow()
    ).order_by(Event.date).all()
    
    past_events = Event.query.filter(
        Event.date <= datetime.utcnow()
    ).order_by(Event.date.desc()).all()
    
    return render_template('community/events.html',
                         upcoming_events=upcoming_events,
                         past_events=past_events)

@bp.route('/events/<int:event_id>')
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('community/event.html', event=event)

@bp.route('/events/<int:event_id>/join', methods=['POST'])
@login_required
def join_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if event not in current_user.events:
        current_user.events.append(event)
        db.session.commit()
        flash('Successfully joined the event!', 'success')
    else:
        flash('You are already registered for this event.', 'info')
    
    return redirect(url_for('community.view_event', event_id=event_id))

# Product routes
@bp.route('/products')
def products():
    products = Product.query.order_by(Product.eco_score.desc()).all()
    return render_template('community/products.html', products=products)

@bp.route('/products/<int:product_id>')
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = ProductReview.query.filter_by(product_id=product_id)\
        .order_by(ProductReview.created_at.desc()).all()
    
    return render_template('community/product.html',
                         product=product,
                         reviews=reviews)

@bp.route('/products/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    content = request.form.get('content')
    rating = int(request.form.get('rating'))
    
    if not content or not rating:
        flash('Please provide both a review and rating', 'error')
        return redirect(url_for('community.view_product', product_id=product_id))
    
    review = ProductReview(
        user_id=current_user.id,
        product_id=product_id,
        content=content,
        rating=rating
    )
    
    db.session.add(review)
    db.session.commit()
    
    flash('Review added successfully!', 'success')
    return redirect(url_for('community.view_product', product_id=product_id))
