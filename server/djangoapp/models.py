from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    def __str__(self):
        return "Name: " + self.name + " Description: " + self.description

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dealer_id = models.IntegerField(default=0)
    car_type = models.CharField(max_length=5, choices=[('sedan', 'Sedan'), ('suv', 'SUV'), ('wagon','Wagon')])
    year = models.DateField()
    def __str__(self):
        return "Name: " + self.name + " Dealer: " + str(self.dealer_id) + " Type: " + self.car_type + " Year: " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
