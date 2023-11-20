from django.db import models

# Create your models here.

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=32, verbose_name='Username', db_index=True)
    email = models.EmailField(max_length=32, verbose_name='Email')
    mobile_phone = models.CharField(max_length=32, verbose_name='Phone')
    password = models.CharField(verbose_name='Password',max_length=64)


class PricePolicy(models.Model):
    category_choices = (
        (1, 'Free'),
        (2, 'VIP'),
        (3, 'SVIP'),
    )
    category = models.SmallIntegerField(verbose_name='Price Policy', choices=category_choices, default=2)
    title = models.CharField(verbose_name='Title', max_length=32)
    price = models.PositiveIntegerField(verbose_name='Price')

    project_num = models.PositiveIntegerField(verbose_name='Project Number')
    project_member = models.PositiveIntegerField(verbose_name='Project Member')
    project_space = models.PositiveIntegerField(verbose_name='Single Project Size')
    per_file_size = models.PositiveIntegerField(verbose_name='Single File Size')

    create_datetime = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)

class Transaction(models.Model):
    status_choices = (
        (1, 'Not Paid'),
        (2, 'Paid'),
    )
    status = models.SmallIntegerField(verbose_name='Status', choices=status_choices)
    order = models.CharField(verbose_name='Order', max_length=64, unique=True)

    user = models.ForeignKey(verbose_name='User', to='UserInfo', on_delete=models.CASCADE)
    price_policy = models.ForeignKey(verbose_name='Price Policy', to='PricePolicy', on_delete=models.CASCADE)

    count = models.IntegerField(verbose_name='Count (Year)', help_text='0 for unlimited time')
    price = models.IntegerField(verbose_name='Price')

    start_datetime = models.DateTimeField(verbose_name='Start Time', null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name='End Time', null=True, blank=True)
    create_datetime = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)


class Project(models.Model):
    COLOR_CHOICES = (
        (1, '#56b8eb'),
        (2, '#f28033'),
        (3, '#ebc656'),
        (4, '#a2d148'),
        (5, '#20bfa4'),
        (6, '#7461c2'),
        (7, '#20bfa3'),
    )
    name = models.CharField(verbose_name='Project Name', max_length=32)
    color = models.SmallIntegerField(verbose_name='Color', choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name='Description', max_length=128, null=True, blank=True)
    use_space = models.IntegerField(verbose_name='Used size', default=0)
    star = models.BooleanField(verbose_name='Star', default=False)

    join_count = models.SmallIntegerField(verbose_name='Join Count', default=1)
    creator = models.ForeignKey(verbose_name='Creator', to='UserInfo', on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)

class ProjectUser(models.Model):
    user = models.ForeignKey(verbose_name='User', to='UserInfo', on_delete=models.CASCADE)
    project = models.ForeignKey(verbose_name='Project', to='Project', on_delete=models.CASCADE)
    star = models.BooleanField(verbose_name='Star', default=False)

    create_datetime = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)


class Wiki(models.Model):
    project = models.ForeignKey(verbose_name='Project', to='Project', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title', max_length=32)
    content = models.TextField(verbose_name='Content')
    depth = models.IntegerField(verbose_name='Depth', default=1)

    parent = models.ForeignKey(verbose_name='Parent', to='self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.title
    


class FileRepository(models.Model):
    project = models.ForeignKey(verbose_name='Project', to='Project', on_delete=models.CASCADE)
    file_type_choices = (
        (1, 'Folder'),
        (2, 'File'),
    )
    file_type = models.SmallIntegerField(verbose_name='Upload Type', choices=file_type_choices)
    name = models.CharField(verbose_name='Folder Name', max_length=128, help_text='Directory Name')
    key = models.CharField(verbose_name='s3 stored key', max_length=128, null=True, blank=True)
    file_size = models.IntegerField(verbose_name='File Size', null=True, blank=True)
    file_path = models.CharField(verbose_name='File Path', max_length=255, null=True, blank=True)

    parent = models.ForeignKey(verbose_name='Parent', to='self', null=True, blank=True, on_delete=models.CASCADE, related_name='child')

    update_user = models.ForeignKey(verbose_name='Last Update User', to='UserInfo', on_delete=models.CASCADE)
    update_datetime = models.DateTimeField(verbose_name='Last Update Time', auto_now=True)

