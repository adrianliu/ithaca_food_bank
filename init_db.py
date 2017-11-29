from foodbank import db, Category, FoodItem

# recreate all of the db tables
db.drop_all()
db.create_all()

#insert 2 categories
category_one = Category(name='Fruit',description='This is Fruit')
category_two = Category(name='Meat',description='This is Meat')
db.session.add(category_one)
db.session.add(category_two)
db.session.commit()

#insert 3 items in category_one, 3 items in category_two
fooditem1 = FoodItem(category=category_one, name='Watermelon', description='This is Watermelon')
fooditem2 = FoodItem(category=category_one, name='Apple', description='This is Apple')
fooditem3 = FoodItem(category=category_one, name='PineApple', description='This is PineApple')

fooditem4 = FoodItem(category=category_two, name='Beef', description='This is Beef')
fooditem5 = FoodItem(category=category_two, name='Lamb', description='This is Lamb')
fooditem6 = FoodItem(category=category_two, name='Pork', description='This is Pork')

db.session.add(fooditem1)
db.session.add(fooditem2)
db.session.add(fooditem3)
db.session.add(fooditem4)
db.session.add(fooditem5)
db.session.add(fooditem6)
db.session.commit()