from django.db import models

# Create your models here.

class Person(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    user_Id = models.CharField(max_length=20, verbose_name='_id')
    user_name = models.CharField(max_length=20, verbose_name='_name')
    user_email = models.CharField(max_length=20, verbose_name='_email')

    # Metadata
    class Meta: 
        ordering = ["-user_Id"]

    # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.field_name