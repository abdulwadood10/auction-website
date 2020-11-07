from src import app, db, bcrypt
from flask import render_template, url_for, flash, redirect,request
from src.form import RegisterForm, LoginForm, ItemForm,BidForm

from flask_login import logout_user,login_user,current_user,login_required
from src.models import User,Item,Bid,WatchList
import os
import secrets
from PIL import Image



@app.route('/')
@app.route('/home')
def home():
    items = Item.query.all()
    total_bids = []

    for item in items:
        bids = item.bid_price
        for bid in bids:
            total_bids.append(bid.bid_price)

    bids_length = len(total_bids)
    sorted_list = sorted(total_bids)
    if len(sorted_list) == 1:
        closest_bid = sorted_list[0]
    else:
        closest_bid = sorted_list[::-1][1]
    highest_bid = max(total_bids)





    return render_template('home.html', title='Home',  items=items, image_num=1,closest_bid = closest_bid,highest_bid=highest_bid,bids_length=bids_length)



@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,contact=form.contact.data, address=form.address.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)
#
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/createitem',methods=['GET','POST'])
@login_required
def createitem():

    user = User.query.get(int(current_user.id))
    item = ItemForm()
    item.item_category.choices = [('Car','Car'),('Dress','Dress'),('Mobile','Mobile')]
    print('before validation')
    picture_path=''
    if item.validate_on_submit():

        print('on validation')
        item_db = Item(name=item.item_name.data, description=item.item_desc.data,
                       starting_bid=item.item_starting_bid.data, category=item.item_category.data,user_id=current_user.id)


        db.session.add(item_db)
        db.session.commit()
        picture_file = save_picture(item.item_img.data,item_db.id)
        item_db.item_image = picture_file
        picture_path = picture_file

        print('before add')
        db.session.commit()
        bid = Bid(bid_price=item.item_starting_bid.data, item_id=item_db.id,user_name=current_user.username,bid_status=True)
        db.session.add(bid)
        db.session.commit()
        print(bid)
        print(item_db.id)
        print('item added')


        # return redirect(url_for('home'))



    return render_template('createitem.html', title='Create Item',item=item,user=user,item_img=url_for('static',filename ='data/items/'+ picture_path))


def save_picture(item_picture,item_name):
    _,f_ext =os.path.splitext(item_picture.filename)
    picture_fn = str(item_name)+f_ext
    picture_path = os.path.join(app.root_path,'static/data/items',picture_fn)
    print(picture_path)
    output_size= (125,125)
    i =Image.open(item_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route('/categories/<category_name>')
def categories(category_name):
    category = Item.query.filter_by(category=category_name)
    total_bids = []

    for item in category:
        bids = item.bid_price
        for bid in bids:
            total_bids.append(bid.bid_price)
    bids_length = len(total_bids)
    sorted_list = sorted(total_bids)
    if len(sorted_list) == 1:
        closest_bid = sorted_list[0]
    else:
        closest_bid = sorted_list[::-1][1]
    highest_bid = max(total_bids)
    return render_template('categories.html', title=category_name, bids_length=bids_length,category=category, image_num=1,highest_bid = highest_bid,closest_bid=closest_bid)



#
# @app.route('/mybids')
# def mybids():
#     bids = Bid.query.filter_by(username='haris')
#     items =


@app.route('/bid/<int:item_id>',methods=['GET','POST'])
def bid(item_id):
    items = Item.query.filter_by(id=item_id)
    total_bids = []
    user = User.query.get(int(current_user.id))
    for item in items:
        bids = item.bid_price
        for bid in bids:
            total_bids.append(bid.bid_price)

    print(total_bids)
    bids_length = len(total_bids)
    sorted_list = sorted(total_bids)
    if len(sorted_list) == 1:
        closest_bid = sorted_list[0]
    else:
        closest_bid = sorted_list[::-1][1]
    highest_bid = max(total_bids)
    bid_form = BidForm()

    if request.method =='GET':
        print('get method')
        bid_form.userName.data = current_user.username
        bid_form.itemID.data = item_id



    if bid_form.validate_on_submit():
        print('bid form')
        if bid_form.bidPrice.data < highest_bid:
            flash('You are bidding less than the highest bid. Bid greater than highest bid.')
            return redirect(url_for('bid',item_id=item_id))
        else:
            bid = Bid(bid_price=bid_form.bidPrice.data,item_id=item_id,user_name=current_user.username)

            db.session.add(bid)

            db.session.commit()
            return redirect(url_for('bid',item_id=item_id))




    return  render_template('bid.html', title='My bids', items=items,bids_length=bids_length,highest_bid=highest_bid,closest_bid=closest_bid,bid_form=bid_form)




@app.route('/myitems')
@login_required
def myitems():
    items = Item.query.filter_by(user_id=current_user.id)
    return render_template('myitems.html', title='My Items', items=items)

@app.route('/mybids/')
@login_required
def mybids():
    bids = Bid.query.filter_by(user_name=current_user.username)
    itemIds = []
    for bid in bids:
        itemIds.append(bid.item_id)
    items = Item.query.filter(Item.id.in_(itemIds)).all()
    return render_template('myitems.html', title='My Items',items=items)


@app.route('/addwatch/<int:item_id>')
@login_required
def addwatch(item_id):
    watch = WatchList(status=True, user_id=current_user.id, item_id=item_id)
    db.session.add(watch)
    db.session.commit()
    return redirect(url_for('home'))



@app.route('/watchlist')
@login_required
def watchlist():
    watched = WatchList.query.filter_by(user_id=current_user.id)
    itemWatch = []
    for watch in watched:
        itemWatch.append(watch.item_id)
    items = Item.query.filter(Item.id.in_(itemWatch)).all()
    return render_template('watchlist.html', title='My WatchList',items=items)


@app.route('/removeitem/<int:item_id>')
@login_required
def removeitem(item_id):
    item = Item.query.get(item_id)
    bids = Bid.query.filter_by(item_id=item_id)
    for bid in bids:
        db.session.delete(bid)
    db.session.delete(item)
    db.session.commit()

    return redirect(url_for('my_items'))

@app.route('/itemstatus/<int:item_id>')
@login_required
def itemstatus(item_id):
    item = Item.query.get_or_404(item_id)
    if item.status == True:
        item.status = False
    else:
        item.status = True
    db.session.commit()
    return redirect(url_for('myitems'))
