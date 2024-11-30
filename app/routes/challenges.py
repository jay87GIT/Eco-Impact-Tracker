from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Challenge, User, Activity
from datetime import datetime, timedelta

bp = Blueprint('challenges', __name__)

@bp.route('/challenges')
@login_required
def challenges():
    # Get active challenges
    active_challenges = Challenge.query.filter(
        Challenge.end_date >= datetime.utcnow()
    ).order_by(Challenge.start_date.asc()).all()
    
    # Calculate statistics for each challenge
    for challenge in active_challenges:
        challenge.participant_count = len(challenge.participants)
        challenge.completion_rate = challenge.get_completion_rate()
    
    return render_template('challenges/list.html', challenges=active_challenges)

@bp.route('/challenges/join/<int:challenge_id>')
@login_required
def join_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    
    if challenge not in current_user.challenges:
        current_user.challenges.append(challenge)
        db.session.commit()
        flash(f'You have joined the {challenge.title} challenge!', 'success')
    
    return redirect(url_for('challenges.challenges'))

@bp.route('/challenges/complete/<int:challenge_id>')
@login_required
def complete_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    
    if challenge in current_user.challenges and not challenge.is_completed_by(current_user):
        # Add challenge to user's completed challenges
        current_user.completed_challenges.append(challenge)
        
        # Add points to user
        current_user.add_points(challenge.points)
        
        # Log the activity
        activity = Activity(
            user_id=current_user.id,
            category='Challenge',
            description=f'Completed challenge: {challenge.title}',
            impact=challenge.points / 10  # Convert points to CO2 impact
        )
        db.session.add(activity)
        db.session.commit()
        
        flash(f'Congratulations! You completed the {challenge.title} challenge and earned {challenge.points} points!', 'success')
    
    return redirect(url_for('challenges.challenges'))

@bp.route('/challenges/leaderboard')
def leaderboard():
    # Get top 100 users by points
    top_users = User.query.order_by(User.points.desc()).limit(100).all()
    
    return render_template('challenges/leaderboard.html', users=top_users)

@bp.route('/api/challenges/stats')
@login_required
def challenge_stats():
    # Get user's challenge statistics
    completed_challenges = current_user.completed_challenges.all()
    total_completed = len(completed_challenges)
    total_joined = len(current_user.challenges)
    
    # Calculate completion rate
    completion_rate = (total_completed / total_joined * 100) if total_joined > 0 else 0
    
    # Get category distribution
    category_stats = {}
    for challenge in completed_challenges:
        category_stats[challenge.category] = category_stats.get(challenge.category, 0) + 1
    
    return jsonify({
        'total_joined': total_joined,
        'total_completed': total_completed,
        'total_points': current_user.points,
        'current_level': current_user.level,
        'next_level_points': (current_user.level * 1000) - current_user.points,
        'completion_rate': round(completion_rate, 2),
        'category_distribution': category_stats
    })

@bp.route('/challenges/create', methods=['GET', 'POST'])
@login_required
def create_challenge():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        points = int(request.form.get('points'))
        category = request.form.get('category')
        difficulty = request.form.get('difficulty')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        
        if end_date <= start_date:
            flash('End date must be after start date!', 'error')
            return redirect(url_for('challenges.create_challenge'))
        
        challenge = Challenge(
            title=title,
            description=description,
            points=points,
            category=category,
            difficulty=difficulty,
            start_date=start_date,
            end_date=end_date
        )
        
        db.session.add(challenge)
        db.session.commit()
        
        flash('Challenge created successfully!', 'success')
        return redirect(url_for('challenges.challenges'))
    
    return render_template('challenges/create.html')

@bp.route('/challenges/my')
@login_required
def my_challenges():
    # Get user's active challenges
    active_challenges = [c for c in current_user.challenges if current_user not in c.completed_by]
    
    # Get user's completed challenges
    completed_challenges = [c for c in current_user.challenges if current_user in c.completed_by]
    
    return render_template('challenges/my_challenges.html',
                         active_challenges=active_challenges,
                         completed_challenges=completed_challenges)
