import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np

# import data set
url = "https://drive.google.com/file/d/1YA11pBzuFi2UCDrXafAr_Tq9qot-GB92/view?usp=sharing"
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]

data = pd.read_csv(url)

data["Gender"] = data["Gender"].replace(["Male","Female"],[1,0])
data["MartialStatus"] = data["MartialStatus"].replace(["Married","UnMarried"],[1,0])
data["Education"] = data["Education"].replace(["Graduate","UnderGraduate"],[1,0])
data["Employee"] = data["Employee"].replace(["Yes","No"],[1,0])
data["PropertyArea"] = data["PropertyArea"].replace(["Rural","Urban","Semi-Urban"],[0,1,2])
del data["LoanId"]

feature_cols = ["Age","Gender","MartialStatus","Education","NoOfDependents","Employee","PropertyArea","Income","ExistingEmi"]
x = data[feature_cols]
y = data.Status

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=1)

# clf = DecisionTreeClassifier(max_depth=5)

# clf = clf.fit(x_train,y_train)
# y_pred = clf.predict(x_test)



def predict(age,gender,martialStatus,education,noOfDependents,employee,propertyArea,income,existingEmi):
	Age = age
	Gender = 1 if (gender=="Male") else 0
	MartialStatus = 1 if (martialStatus=="Married") else 0
	Education = 1 if (education == "Graduate") else 0
	NoOfDependents = noOfDependents
	Employee = 1 if (employee=="Yes") else 0
	PropertyArea = 0 if (propertyArea=="Rural") else 1 if(propertyArea=="Urban") else 2 if(propertyArea=="Semi-Urban") else ""
	Income = income
	ExistingEmi = existingEmi

	clf = DecisionTreeClassifier(max_depth=5)
	clf = clf.fit(x_train,y_train)
	status = clf.predict([[Age,Gender,MartialStatus,Education,NoOfDependents,Employee,PropertyArea,Income,ExistingEmi]])
	
	if status == 1:
		return True
	else:
		return False









