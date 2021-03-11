from django.contrib.auth.models import User
from news.models import Author, Post, Comment, Category, PostCategory

user = User.objects.create_user(username='David')
user = User.objects.create_user(username='Roman')

author = User.objects.get(username='Roman')
Author.objects.create(author=author)

author = User.objects.get(username='David')
Author.objects.create(author=author)

Category.objects.create(title='IT')
Category.objects.create(title='Спорт')
Category.objects.create(title='Бизнес')
Category.objects.create(title='Наука')

Post.objects.create(post_author = Author.objects.get(author = User.objects.get(username = 'David')), post_theme = Post.news, post_title = 'Новости хоккея', post_text = 'Word Championship 2020')
Post.objects.create(post_author = Author.objects.get(author = User.objects.get(username = 'Roman')), post_theme = Post.article, post_title = 'Знаете ли вы?', post_text = 'Нет не знаем...')
Post.objects.create(post_author = Author.objects.get(author = User.objects.get(username = 'Roman')), post_theme = Post.article, post_title = 'Всё про IT', post_text = 'Жил был программист.')

post_1 = Post.objects.get(post_title='Новости хоккея')
post_2 = Post.objects.get(post_title = 'Знаете ли вы?')
post_3 = Post.objects.get(post_title = 'Всё про IT')

post_1.post_category.add(Category.objects.get(title = 'Спорт'))
post_2.post_category.add(Category.objects.get(title = 'Бизнес'), Category.objects.get(title = 'Наука'))
post_1.post_category.add(Category.objects.get(title = 'IT'))

Comment.objects.create(comment_user = User.objects.get(username= 'Roman'), comment_post = Post.objects.get(post_title = 'Новости хоккея'), comment_text = 'Отлично!')
Comment.objects.create(comment_user = User.objects.get(username= 'Roman'), comment_post = Post.objects.get(post_title = 'Всё про IT'), comment_text = 'Молодец!')
Comment.objects.create(comment_user = User.objects.get(username= 'David'), comment_post = Post.objects.get(post_title = 'Всё про IT'), comment_text = ')))')
Comment.objects.create(comment_user = User.objects.get(username= 'David'), comment_post = Post.objects.get(post_title = 'Знаете ли вы?'), comment_text = 'Ну конечно же!')

Post.objects.get(post_title='Новости хоккея').like()
Post.objects.get(post_title='Новости хоккея').like()
Post.objects.get(post_title='Новости хоккея').like()
Post.objects.get(post_title='Новости хоккея').like()
Post.objects.get(post_title='Новости хоккея').like()
Post.objects.get(post_title='Новости хоккея').dislike()

Post.objects.get(post_title='Знаете ли вы?').like()
Post.objects.get(post_title='Знаете ли вы?').like()
Post.objects.get(post_title='Знаете ли вы?').like()
Post.objects.get(post_title='Знаете ли вы?').like()
Post.objects.get(post_title='Знаете ли вы?').dislike()
Post.objects.get(post_title='Знаете ли вы?').dislike()

Post.objects.get(post_title='Всё про IT').like()
Post.objects.get(post_title='Всё про IT').like()
Post.objects.get(post_title='Всё про IT').like()
Post.objects.get(post_title='Всё про IT').dislike()
Post.objects.get(post_title='Всё про IT').dislike()
Post.objects.get(post_title='Всё про IT').dislike()

Comment.objects.get(comment_text = 'Отлично!').like()
Comment.objects.get(comment_text = 'Молодец!').like()
Comment.objects.get(comment_text = ')))').like()
Comment.objects.get(comment_text = 'Ну конечно же!').dislike()

rating = Author.objects.get(author= User.objects.get(username ='David')).rating
Author.objects.get(author= User.objects.get(username ='David')).update_rating(rating)
rating = Author.objects.get(author= User.objects.get(username ='Roman')).rating
Author.objects.get(author= User.objects.get(username ='Roman')).update_rating(rating)

top = Author.objects.all().order_by('-rating').values('author', 'rating')[0]
top['author'] = Author.objects.all().order_by('-rating')[0].author.username
print(top)

top_post = Post.objects.all().order_by('-rating_of_post').values('created', 'post_author', 'post_rating', 'post_title')[0]
top_post['created'] = top_post['created'].strftime("%A, %d. %B %Y %I:%M%p")
top_post['author'] = Post.objects.all().order_by('-rating_of_post')[0].author.author.username
top_post['preview'] = Post.objects.all().order_by('-post_rating')[0].preview()
print(top_post)

comments = Comment.objects.filter(comments_post =Post.objects.get(post_title='Новости хоккея')).values('comment_created', 'comment_user', 'comment_rating', 'comment_text')
for comment in comments:
    comment['comment_created'] = comment['comment_created'].strftime("%A, %d. %B %Y %I:%M%p")
    comment['comment_user'] = Author.objects.get(author = comment['comment_user']).author.username
print(comment)

