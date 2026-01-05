from django.db import models

# 商品モデル
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=[
            ('tunnel', 'トンネル'),
            ('hospital', '廃病院'),
            ('mountain', '山奥'),
            ('school', '廃校'),
        ],
        default='tunnel'
    )

    def __str__(self):
        return self.name


# レビューモデル
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} のレビュー"


# 記事モデル（ブログなど）
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

image = models.ImageField(upload_to='products/', blank=True, null=True)