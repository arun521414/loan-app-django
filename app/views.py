from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.core.exceptions import ObjectDoesNotExist
import json
from app.models import Profile,PersonalDetails,BankDetails
from app.helper import isEmailExist,isMobileExist,generateProfileId,ageCalc,loanAmountCalc,emiCalc
from app.loanPrediction import predict
from random import randint



@csrf_exempt
def login(request):
	if request.method == "POST":

		data = JSONParser().parse(request)

		loginType = data.get("type")
		password  = data.get("password") 

		if(loginType=="email"):

			email = data.get("email")

			try:
				user = Profile.objects.get(email=email,password=password)

				return JsonResponse({
					"status":"success",
					"type"  : "email",
					"msg"   : "login successfully",
					"profileId": user.profileId,
					},safe=False)

			except ObjectDoesNotExist:

				return JsonResponse({
					"status":"error",
					"type" : "email",
					"msg"  : "invalid email and password "
					},safe=False)

		elif(loginType=="mobileNo"):

			mobileNo = data.get("mobileNo")

			try:

				user = Profile.objects.get(mobileNo=mobileNo,password=password)

				return JsonResponse({
					"status":"success",
					"type"  : "mobileNo",
					"msg"   : "login successfully",
					"profileId": user.profileId
					},safe=False)

			except ObjectDoesNotExist:

				return JsonResponse({
					"status":"error",
					"type" : "mobileNo",
					"msg"  : "invalid mobile number and password "
					},safe=False)

	
	return JsonResponse({"status":"false","msg":"bad request"},status=400,safe=False)



@csrf_exempt
def signup(request):

	if request.method == "POST":

		data = JSONParser().parse(request)

		email    = data.get("email")
		mobileNo = data.get("mobileNo")
		password = data.get("password")

		email_exist = isEmailExist(email)
		mobile_exist = isMobileExist(mobileNo)

		if(email_exist):

			return JsonResponse(
				{
				"status":"error",
				"type":"emailError",
				"msg":"Email already exist"
				},safe=False)

		elif(mobile_exist):

			return JsonResponse(
				{
				"status":"error",
				"type":"mobileNoError",
				"msg":"Mobile Number already exist"
				},safe=False)
		else:

			profileId = generateProfileId()

			profile = Profile.objects.create(profileId=profileId,email=email,mobileNo=mobileNo,password=password)

			return JsonResponse(
				{
				"status":"success",
				"type":"signup",
				"msg":"Account created successfully"
				})

	return JsonResponse({"status":"false","msg":"bad request"},status=400,safe=False)


def getProfile(request,profile_id):

	if request.method=="GET":

		try:
			profile = Profile.objects.get(profileId=profile_id)

			return JsonResponse({
				"status"                 : "success",
				"profileId"              : profile.profileId,
				"email"                  : profile.email,
				"mobileNo"               : profile.mobileNo,
				"isPersonalDetailsVerify": profile.isPersonalDetailsVerify,
				"isKycVerify"            : profile.isKycVerify,
				"eligible"               : profile.eligible
				},safe=False)

		except ObjectDoesNotExist:
			return JsonResponse({"status":"error","msg":"not found"},status=404,safe=False)

@csrf_exempt
def registerPersonalDetails(request,profile_id):

	if request.method == "POST":

		data = JSONParser().parse(request)

		fullName       = data.get("fullName")
		panNumber      = data.get("panNumber")
		gender         = data.get("gender")
		dob            = data.get("dob")
		martialStatus  = data.get("martialStatus")
		employee       = data.get("employee")
		noOfDependents = data.get("noOfDependents")
		education      = data.get("education")
		propertyArea   = data.get("propertyArea")
		income         = data.get("income")
		existingEmi    = data.get("existingEmi")
		address        = data.get("address")
		city           = data.get("city")
		state          = data.get("state")
		pincode        = data.get("pincode")

		try:
			profile = Profile.objects.get(profileId=profile_id)
			PersonalDetails(
				profile        = profile,
				fullName       = fullName,
				panNumber      = panNumber,
				gender         = gender,
				dob            = dob,
				martialStatus  = martialStatus,
				employee       = employee,
				noOfDependents = noOfDependents,
				education      = education,
				propertyArea   = propertyArea,
				income         = income,
				existingEmi    = existingEmi,
				address        = address,
				city           = city,
				state          = state,
				pincode        = pincode
				).save()
			
			profile.isPersonalDetailsVerify = True
			profile.save()


			return JsonResponse(
				{
				"status":"success",
				"type":"registerPersonalDetails",
				"msg":"register succesfully"
				},safe=False)
		except:
			return JsonResponse({"status":"error"},safe=False)

@csrf_exempt
def uploadAadhar(request,profile_id):

	if request.method == "POST":

		
		frontImage = request.FILES["frontImage"]
		backImage  = request.FILES["backImage"]

		try:
			profile = Profile.objects.get(profileId=profile_id)
			user    = PersonalDetails.objects.get(profile=profile)
			user.aadharFront= frontImage
			user.aadharBack = backImage
			user.save()
			profile.isKycVerify = True
			profile.save()
			
			return JsonResponse(
				{
				"status":"success",
				"type":"aathar-upload",
				"msg":"upload successfully"
				},safe=False)

		except ObjectDoesNotExist:

			return JsonResponse({"status":"error","type":"aathar-upload","msg":"profile not found"},safe=False)
			

@csrf_exempt
def registerBankDetails(request,profile_id):
	if request.method == "POST":
		data = JSONParser().parse(request)

		bankName = data.get("bankName")
		ifscCode = data.get("ifscCode")
		accountNo = data.get("accountNo")

		try:

			profile = Profile.objects.get(profileId=profile_id)
			BankDetails(profile=profile,bankName=bankName,ifscCode=ifscCode,accountNo=accountNo).save()

			return JsonResponse({"status":"success","type":"bank details","msg":"bank details register succesfully"},safe=False)

		except ObjectDoesNotExist:

			return JsonResponse({
				"status":"error",
				"type":"bank details",
				"msg":"profile not found"
				})
		


def getBankDetails(request,profile_id):

	if request.method == "GET":

		try:
			profile = Profile.objects.get(profileId=profile_id)
			bank = BankDetails.objects.get(profile=profile)
			print(bank)

			return JsonResponse({
				"status" : "success",
				"bankName":bank.bankName,
				"ifscCode":bank.ifscCode,
				"accountNo":bank.accountNo
				},safe=False)

		except ObjectDoesNotExist:
			
			return JsonResponse({
				"status":"error",
				"type":"bankDetails",
				"msg" : "bank details not found"
				},safe=False)


def getLoanDetails(request,profile_id):

	if request.method == "GET":

		try:

			profile = Profile.objects.get(profileId=profile_id)
			personalDetails = PersonalDetails.objects.get(profile=profile)

			#check loan eligibile

			status = predict(

				age = ageCalc(int(personalDetails.dob[6:])),
				gender = personalDetails.gender,
				martialStatus = personalDetails.martialStatus,
				education = personalDetails.education,
				noOfDependents = personalDetails.noOfDependents,
				employee = personalDetails.employee,
				propertyArea = personalDetails.propertyArea,
				income = personalDetails.income,
				existingEmi = personalDetails.existingEmi

				)

			profile.eligible = status
			profile.save()

			

			#calculate loan amount

			if(profile.eligible == True):

				amount = loanAmountCalc(personalDetails.income,personalDetails.existingEmi)
				months = 12
				interestRate = 11
				emi = emiCalc(amount,months,interestRate)
				totalPayable = emi * months
				interestPayable = totalPayable - amount * months  

				return JsonResponse({
					"status":"success",
					"loanAmount":amount * months,
					"tenure":months,
					"interestRate":interestRate,
					"emi":emi,
					"totalPayable":totalPayable,
					"interestPayable":interestPayable,
					"msg":"eligible"
					},safe=False)
			else:
				return JsonResponse({
					"status":"error",
					"type":"loanDetails",
					"msg" : "not eligible"
					},safe=False)

		except ObjectDoesNotExist:
			return JsonResponse({
				"status":"error",
				"msg":"profile not found"
				})
