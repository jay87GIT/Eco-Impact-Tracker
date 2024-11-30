from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Activity, Challenge, ForumPost, Event, User
from datetime import datetime, timedelta
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Get user's recent activities
    recent_activities = Activity.query.filter_by(user_id=current_user.id)\
        .order_by(Activity.created_at.desc()).limit(5).all()
    
    # Get upcoming events
    upcoming_events = Event.query.filter(
        Event.date >= datetime.utcnow()
    ).order_by(Event.date.asc()).limit(3).all()
    
    # Get recent forum discussions
    recent_discussions = ForumPost.query.order_by(
        ForumPost.created_at.desc()
    ).limit(5).all()
    
    # Get active challenges
    active_challenges = Challenge.query.filter(
        Challenge.end_date >= datetime.utcnow()
    ).order_by(Challenge.start_date.asc()).limit(3).all()
    
    # Calculate total impact
    total_impact = db.session.query(db.func.sum(Activity.impact))\
        .filter_by(user_id=current_user.id).scalar() or 0
    
    # Get leaderboard
    leaderboard = User.query.order_by(User.points.desc()).limit(5).all()
    
    return render_template('main/dashboard.html',
                         recent_activities=recent_activities,
                         upcoming_events=upcoming_events,
                         recent_discussions=recent_discussions,
                         active_challenges=active_challenges,
                         total_impact=total_impact,
                         leaderboard=leaderboard)

@main.route('/log-activity', methods=['GET', 'POST'])
@login_required
def log_activity():
    if request.method == 'POST':
        category = request.form.get('category')
        description = request.form.get('description')
        impact = float(request.form.get('impact'))
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        
        activity = Activity(
            user_id=current_user.id,
            category=category,
            description=description,
            impact=impact,
            date=date
        )
        
        # Add points based on impact (negative impact is good, so multiply by -10)
        points = int(impact * -10)  # 10 points per kg of CO2 saved
        current_user.add_points(points)
        
        db.session.add(activity)
        db.session.commit()
        
        flash(f'Activity logged successfully! You earned {points} points!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('main/log_activity.html')

@main.route('/activity-stats')
@login_required
def activity_stats():
    # Get all user activities
    activities = Activity.query.filter_by(user_id=current_user.id).all()
    
    # Convert to pandas DataFrame for analysis
    df = pd.DataFrame([{
        'date': a.date,
        'impact': a.impact,
        'category': a.category
    } for a in activities])
    
    if not df.empty:
        # Calculate statistics
        total_impact = df['impact'].sum()
        impact_by_category = df.groupby('category')['impact'].sum().to_dict()
        daily_average = df.groupby(df['date'].dt.date)['impact'].mean().mean()
        
        # Calculate trend
        df['date'] = pd.to_datetime(df['date'])
        weekly_trend = df.resample('W', on='date')['impact'].sum().tolist()[-4:]  # Last 4 weeks
    else:
        total_impact = 0
        impact_by_category = {}
        daily_average = 0
        weekly_trend = []
    
    return jsonify({
        'total_impact': float(total_impact),
        'impact_by_category': impact_by_category,
        'daily_average': float(daily_average),
        'weekly_trend': [float(x) for x in weekly_trend]
    })

@main.route('/daily-tips')
@login_required
def daily_tips():
    tips = [
        {
            'title': 'Use Reusable Bags',
            'description': 'Switch to reusable shopping bags instead of plastic bags. This can save up to 307 plastic bags per person annually.',
            'impact': 4.1,  # kg CO2 saved per year
            'difficulty': 'Easy',
            'points': 50
        },
        {
            'title': 'LED Light Bulbs',
            'description': 'Replace traditional bulbs with LED lights. They use 75% less energy and last 25 times longer.',
            'impact': 226.8,  # kg CO2 saved per year
            'difficulty': 'Easy',
            'points': 100
        },
        {
            'title': 'Public Transportation',
            'description': 'Use public transportation instead of driving. This can reduce your carbon footprint by up to 2.6 tons annually.',
            'impact': 2600,  # kg CO2 saved per year
            'difficulty': 'Medium',
            'points': 200
        },
        {
            'title': 'Reduce Meat Consumption',
            'description': 'Try having one meatless day per week. This can save up to 331 kg of CO2 annually.',
            'impact': 331,  # kg CO2 saved per year
            'difficulty': 'Medium',
            'points': 150
        },
        {
            'title': 'Start Composting',
            'description': 'Begin composting your food waste. This can reduce methane emissions and create nutrient-rich soil.',
            'impact': 113.4,  # kg CO2 saved per year
            'difficulty': 'Medium',
            'points': 150
        }
    ]
    
    # Get user's completed tips
    completed_tips = Activity.query.filter_by(
        user_id=current_user.id,
        category='Daily Tip'
    ).with_entities(Activity.description).all()
    completed_tips = [tip.description for tip in completed_tips]
    
    return render_template('main/daily_tips.html',
                         tips=tips,
                         completed_tips=completed_tips)

@main.route('/complete-tip', methods=['POST'])
@login_required
def complete_tip():
    tip_title = request.form.get('tip_title')
    impact = float(request.form.get('impact'))
    points = int(request.form.get('points'))
    
    # Log the activity
    activity = Activity(
        user_id=current_user.id,
        category='Daily Tip',
        description=tip_title,
        impact=impact,
        date=datetime.utcnow()
    )
    
    db.session.add(activity)
    
    # Add points
    current_user.add_points(points)
    
    db.session.commit()
    
    flash(f'Congratulations! You completed the tip "{tip_title}" and earned {points} points!', 'success')
    return redirect(url_for('main.daily_tips'))

@main.route('/privacy')
def privacy_policy():
    return render_template('main/privacy.html')

@main.route('/terms')
def terms():
    return render_template('main/terms.html')
