from django.db import models

# Create your models here.
class update(models.Model):
      status =models.CharField(max_length=100)
      department=models.CharField(max_length=100)
      est_days=models.CharField(max_length=100)
      last_modified=models.DateTimeField(auto_now_add=True,editable=False )
      image_qr=models.ImageField(upload_to='pics')
      User_id=models.ForeignKey('file.Register',on_delete=models.SET_NULL,null=True)
      file_type = models.IntegerField(null=True,default=1)