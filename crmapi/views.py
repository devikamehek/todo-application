from django.shortcuts import render
from crm.models import Employee

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework import permissions,authentication
# Create your views here.

class EmployeeSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Employee
        fields="__all__"
        # exclude=("id",)






class EmployeesView(ViewSet):
    # localhost:8000/api/employees/
    # method-GET
    def list(self,request,*args,**kwargs):
        qs=Employee.objects.all()
        # qs-->py native -- deserialization
        # varname=SerializerName(qs)
        # localhost:8000/api/employees/?department=hr (passing querry params url in list employees to list those with same dept)
        if "department" in request.query_params:
            dept=request.query_params.get("department")
            qs=qs.filter(department=dept)

        # localhost:8000/api/employees/?department=hr&salary=45000(it can be used in list employees api)
        if "salary" in request.query_params:
            sal=request.query_params.get("salary")
            qs=qs.filter(salary=sal)

        # # localhost:8000/api/employees/?salary_gt=35000
        # if "salary_gt" in request.query_params:
        #     sal=request.query_params.get("salary_gt")
        #     qs=qs.filter(salary_gt=sal)

        serializer=EmployeeSerializer(qs,many=True)
        return Response(data=serializer.data)
      




    # localhost:8000/api/employees/
    # method-POST
    def create(self,request,*args,**kwargs):
        # serialization
        serializer=EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        



    
    # localhost:8000/api/employees/2/
    # method-GET
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(qs)
        return Response(data=serializer.data)
    





    # localhost:8000/api/employees/1/
    # method-PUT
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp_obj=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(instance=emp_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    




    # localhost:8000/api/employees/
    # method-DELETE
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            Employee.objects.get(id=id).delete()
            return Response(data="deleted")
        except Exception:
            return Response(data="no matching record found")
    

    # custom methods
    # method:GET
    # custom method cheythal maatrame optional query_params cheyyan patulu
    @action(methods=["get"],detail=False)
    def departments(self,request,*args,**kwargs):
        qs=Employee.objects.all().values_list("department",flat=True).distinct()
        return Response(data=qs)

# list,create,retrive,update,delete
    # get-list,retrive
    # post-create
    # put-update
    # delete-delete

    # json format



  
# depts=Employee.objects.all().values_list('department',flat=True).distinct()



class EmployeeViewSetView(ModelViewSet):
    serializer_class=EmployeeSerializer
    model=Employee
    queryset=Employee.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAdminUser]



# python manage.py createsuperuser
# usernam:admin
# password:admin

