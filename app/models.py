from django.db import models

# Create your models here.

class Profile(models.Model):

	profileId        = models.IntegerField(null=True)
	mobileNo         = models.IntegerField(null=True)
	email            = models.EmailField(max_length=100,null=True)
	password         = models.CharField(max_length=100,null=True)
	isPersonalDetailsVerify = models.BooleanField(default=False)
	isKycVerify = models.BooleanField(default=False)
	eligible = models.BooleanField(default=False)


	def __str__(self):
		return str(self.profileId)

class PersonalDetails(models.Model):

	profile = models.ForeignKey("Profile",on_delete=models.CASCADE)
	fullName  = models.CharField(max_length=100,default="")
	panNumber = models.CharField(max_length=100,unique=True,default="")
	gender    = models.CharField(max_length=100,default="")
	dob       = models.CharField(max_length=100,default="")
	martialStatus = models.CharField(max_length=100,default="")
	employee  = models.CharField(max_length=100,default="")
	noOfDependents = models.IntegerField(default=0)
	education = models.CharField(max_length=100,default="")
	propertyArea = models.CharField(max_length=100,default="")
	income = models.IntegerField(default=0)
	existingEmi = models.IntegerField(default=0)
	address = models.TextField(max_length=200,default="")
	city = models.CharField(max_length=100,default="")
	state = models.CharField(max_length=100,default="")
	pincode = models.IntegerField(default=0)
	aadharFront = models.ImageField(blank=True,upload_to="static/images/")
	aadharBack   = models.ImageField(blank=True,upload_to="static/images/")

	def __str__(self):
		return str(self.profile)


class BankDetails(models.Model):
	profile = models.ForeignKey("Profile",on_delete=models.CASCADE)
	bankName = models.CharField(max_length=100,default="")
	ifscCode = models.CharField(max_length=100,default="")
	accountNo = models.IntegerField(default=0)

	def __str__(self):
		return str(self.profile)




