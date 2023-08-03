from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from EmployeeAPP.models import Departments,Employees 
from EmployeeAPP.serializers import DepartmentSerializer, EmployeeSerializer

# Create your views here.
@csrf_exempt
def departmentApi(request , id=0):
    if request.method == 'GET':
        # methode 1
        #ids=[]
        #AllDdepartments = Departments.objects.all()
        #for department in AllDdepartments:
        #    ids.append(department.DepartmentId)
        # methode 2
        ids = Departments.objects.values_list('DepartmentId', flat=True)

        if id != 0:
            if int(id) in ids:
            #if ids.count(int(id)) >0:
                department = Departments.objects.get(DepartmentId=id)
                department_serializer = DepartmentSerializer(department)
                return JsonResponse(department_serializer.data, safe=False)
            else:                
                return JsonResponse(" department inexiste",safe=False)
        
        departments = Departments.objects.all()
        departments_serializer = DepartmentSerializer(departments, many=True)
        return JsonResponse(departments_serializer.data, safe=False) 
    
    elif request.method == 'POST':
        
        department_data=JSONParser().parse(request)
        departmentNameToIN= department_data["DepartmentName"]
        departmentNames = Departments.objects.values_list('DepartmentName', flat=True)
        if departmentNameToIN in departmentNames :
            return JsonResponse("Failed to add department because this Name is already exist ", safe=False)
        else :
            #print("department_data est : ",department_data)
            department_serializer = DepartmentSerializer(data = department_data)
            #print("department_serializer est : ",department_serializer)
            if department_serializer.is_valid():
                department_serializer.save()
                return JsonResponse("Added successfully ", safe=False)
            return JsonResponse("Failed to add ", safe=False)
    
    elif request.method == 'PUT':
        department_data=JSONParser().parse(request)
        department=Departments.objects.get(DepartmentId=department_data['DepartmentId'])
        department_serializer = DepartmentSerializer(department , data = department_data)
        if department_serializer.is_valid():
            department_serializer.save()
            return JsonResponse("Updated successfully ", safe=False)
        return JsonResponse("Failed to Update ", safe=False)
    
    elif request.method =='DELETE':
        department=Departments.objects.get(DepartmentId=id)
        department.delete()
        return JsonResponse("Deleted sucessfully ", safe=False)
    
    
@csrf_exempt 
def employeeApi(request , id=0):
    if request.method == 'GET':
        employees = Employees.objects.all()
        employees_serializer = EmployeeSerializer(employees, many=True) 
        return JsonResponse(employees_serializer.data, safe=False) 
    
    elif request.method == 'POST':
        employee_data=JSONParser().parse(request)
        employee_serializer = EmployeeSerializer(data = employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return JsonResponse("Added successfully ", safe=False)
        return JsonResponse("Failed to add ", safe=False)
    
    elif request.method == 'PUT':
        employee_data=JSONParser().parse(request)
        employee=Employees.objects.get(EmployeeId=employee_data['EmployeeId']) 
        employee_serializer = EmployeeSerializer(employee , data = employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return JsonResponse("Updated successfully ", safe=False)
        return JsonResponse("Failed to Update ", safe=False)
    
    elif request.method =='DELETE':
        employee=Employees.objects.get(EmployeeId=id)
        employee.delete()
        return JsonResponse("Deleted sucessfully ", safe=False)
    

    
