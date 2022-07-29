from app.models import Profile
from random import randint
import datetime



def isEmailExist(email):

	profile = Profile.objects.filter(email=email)

	if len(profile) == 0:

		return False
	else:

		return True

def isMobileExist(mobileNo):

	profile = Profile.objects.filter(mobileNo=mobileNo)

	if len(profile) == 0:

		return False
	else:

		return True

def generateProfileId():

	profileId = randint(100000,999999)

	return profileId 

def ageCalc(year):

	age = datetime.datetime.now().year - year

	return int(age)

def loanAmountCalc(income,existingEmi):

	Halfincome = income/2

	loanAmount = Halfincome - existingEmi
	return loanAmount


def emiCalc(principle,months,interestRate):

	p = principle * months
	n = months
	r = interestRate/(12*100)

	emi = p*r*((1+r)**n)/((1+r)**n-1)

	return round(emi)






	

