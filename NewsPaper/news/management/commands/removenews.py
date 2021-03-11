from django.core.management.base import BaseCommand, CommandError
from ...models import Post, Category, PostCategory


class Command(BaseCommand):
    help = 'Удаляет новости в категории'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если True --
    # то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
    # спрашиваем пользователя действительно ли он хочет удалить все новости
        self.stdout.write(f'Do you really want to delete all posts in {options["category"]}? yes/no')
        answer = input()
        if answer == 'yes':
            try:
                category = Category.objects.get(title=options['category'])
                Post.objects.filter(postcategory__category__title=category.title).delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted all news from category {category.title}'))
                # в случае неправильного подтверждения, говорим что в доступе отказано
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category {category.title}'))
        # в случае неправильного подтверждения, говорим что в доступе отказано
        else:
            self.stdout.write(self.style.ERROR('Access denied'))





