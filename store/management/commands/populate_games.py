import os
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from store.models import Game

class Command(BaseCommand):
    help = 'Заполняет базу данных 15 играми с картинками'

    def handle(self, *args, **kwargs):
        if Game.objects.exists():
            self.stdout.write(self.style.WARNING('Игры уже есть в базе. Пропускаем...'))
            return

        games_data = [
            {"title": "Cyberpunk 2077", "price": "1999.00", "desc": "Открытый мир, киберпанк и захватывающий сюжет в Найт-Сити. Играйте за наёмника V и решайте судьбу города.", "img": "https://image.tmdb.org/t/p/w500/2qXJh2yF1t3.jpg"},
            {"title": "The Witcher 3", "price": "1499.00", "desc": "Ролевая игра с открытым миром, ставшая легендой. В роли Геральта из Ривии отправляйтесь на поиски Цири.", "img": "https://image.tmdb.org/t/p/w500/6Tl4r3Z4y8.jpg"},
            {"title": "Elden Ring", "price": "2999.00", "desc": "Эпическое фэнтези от FromSoftware и Джорджа Р. Р. Мартина. Исследуйте Междуземье и бросьте вызов полубогам.", "img": "https://image.tmdb.org/t/p/w500/4j0n1y6u5.jpg"},
            {"title": "Red Dead Redemption 2", "price": "2499.00", "desc": "История Артура Моргана и банды Ван дер Линде на закате эпохи Дикого Запада. Невероятная детализация мира.", "img": "https://image.tmdb.org/t/p/w500/2w1y5r6.jpg"},
            {"title": "God of War", "price": "1799.00", "desc": "Кратос и его сын Атрей отправляются в опасное путешествие по мирам скандинавской мифологии.", "img": "https://image.tmdb.org/t/p/w500/1y3u7t8.jpg"},
            {"title": "Hollow Knight", "price": "499.00", "desc": "Красивый и сложный метроидвания-платформер в подземном королевстве насекомых Халлоунест.", "img": "https://image.tmdb.org/t/p/w500/3y6u8i9.jpg"},
            {"title": "GTA V", "price": "1299.00", "desc": "Три героя, три истории и один огромный город Лос-Сантос. Классика открытого мира.", "img": "https://image.tmdb.org/t/p/w500/5y7u9i0.jpg"},
            {"title": "Dark Souls III", "price": "1599.00", "desc": "Сложная и мрачная Action-RPG. Бросьте вызов проклятым рыцарям и древним богам.", "img": "https://image.tmdb.org/t/p/w500/7u8i0o1.jpg"},
            {"title": "Sekiro: Shadows Die Twice", "price": "1999.00", "desc": "Самурайский экшен с уникальной боевой системой парирования и невероятно красивыми локациями.", "img": "https://image.tmdb.org/t/p/w500/9i0o1p2.jpg"},
            {"title": "Ghost of Tsushima", "price": "2199.00", "desc": "Открытый мир феодальной Японии. Станьте самураем и защитите остров Цусима от монгольского вторжения.", "img": "https://image.tmdb.org/t/p/w500/1o2p3a4.jpg"},
            {"title": "The Last of Us Part II", "price": "1899.00", "desc": "Эмоциональная история выживания в постапокалиптическом мире. Красивый и жестокий экшен.", "img": "https://image.tmdb.org/t/p/w500/3a4s5d6.jpg"},
            {"title": "Spider-Man", "price": "1799.00", "desc": "Станьте Человеком-пауком и защитите Нью-Йорк. Динамичные бои и захватывающие полеты на паутине.", "img": "https://image.tmdb.org/t/p/w500/4s5d6f7.jpg"},
            {"title": "Horizon Zero Dawn", "price": "1699.00", "desc": "Девушка Элой в мире, где правят механические динозавры. Уникальный сеттинг и отличный сюжет.", "img": "https://image.tmdb.org/t/p/w500/5d6f7g8.jpg"},
            {"title": "Resident Evil 2 Remake", "price": "1499.00", "desc": "Легендарный зомби-хоррор на выживание. Воссоздан с нуля на новом движке.", "img": "https://image.tmdb.org/t/p/w500/6f7g8h9.jpg"},
            {"title": "Mass Effect Legendary Edition", "price": "2499.00", "desc": "Космическая опера, в которой вам предстоит спасти галактику. Все три части в одном издании.", "img": "https://image.tmdb.org/t/p/w500/7g8h9j0.jpg"}
        ]

        media_path = os.path.join(settings.BASE_DIR, 'media', 'covers')
        os.makedirs(media_path, exist_ok=True)

        for i, game in enumerate(games_data):
            self.stdout.write(f'Добавление игры: {game["title"]}...')
            new_game = Game(title=game['title'], description=game['desc'], price=game['price'], is_available=True)
            
            # Скачиваем обложку
            try:
                req = urllib.request.Request(game['img'], headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    img_name = f'game_{i}.jpg'
                    new_game.cover.save(img_name, File(response), save=False)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Не удалось скачать картинку для {game["title"]}: {e}'))

            new_game.save()

        self.stdout.write(self.style.SUCCESS('Успешно добавлено 15 игр!'))