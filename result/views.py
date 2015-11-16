from django.http import HttpResponse,Http404
from django.template import Context
from django.template.loader import get_template
from .models import Result
from .models import Student
from .models import Course

def result_list(request):
 
    query = request.GET.get('usn','')
    #query = "13BT6CS001"
    query1 = request.GET.get('num','')
    # try:
        # query=Student.views.values_list(query=usn)
    # except:
        # raise Http404('Requested usn not found.')
    
    e = Student.objects.values_list('usn').filter(usn=query,sem=query1)
    sname = Student.objects.values_list('sname').filter(usn=query,sem=query1)
    dept = Student.objects.values_list('dept').filter(usn=query,sem=query1)
   # cours = Course.objects.values_list('cname').filter(usn=query)
    subname=Course.objects.values_list()
    result = Result.objects.values_list().filter(usn=query)
    total=[]
    grade=[]
    itotal=0
    etotal=0
    ftotal=0
    results=0
    for i in range(0,result.count()):
        grade.append(grades(result[i][3]+result[i][4]))
        total.append(result[i][3]+result[i][4])
        itotal=itotal+result[i][3]
        etotal=etotal+result[i][4]
    ftotal=itotal+etotal
    percentage=ftotal/(result.count())

    if percentage>=90:
        results="OUTSTANDING"
    elif percentage>=70 and percentage<90:
        results="DISTINCTION"
    elif percentage>=60 and percentage<69:
        results="FIRST"
    elif percentage>=50 and percentage<59:
        results="SECOND"
    elif percentage>=40 and percentage<49:
        results="PASS"
    else:
        results="FAIL"
        
        
    zipped = zip(subname,result,total,grade)
    template = get_template('result/result_list.html')
    variables = Context({
        'usn': e[0][0],
        'department': dept[0][0],
        'name': sname[0][0].upper(),
        'res': result,
        'results':results,
        'sname':subname,
        'total':total,
        'grade':grade,
        'itotal':itotal,
        'etotal':etotal,
        'ftotal':ftotal,
        'percentage':percentage,
        'zip':zipped
    })
    output = template.render(variables)
    return HttpResponse(output)

def grades(marks):
    if(marks>=95):
        return "S++"
    elif(marks>=90 and marks<=94):
         return "S+"
    elif(marks>=85 and marks<=89):
         return "S"
    elif(marks>=80 and marks<=84):
         return "A++"
    elif(marks>=75 and marks<=79):
         return "A+"
    elif(marks>=70 and marks<=74):
         return "A"
    elif(marks>=65 and marks<=69):
         return "B+"
    elif(marks>=60 and marks<=64):
         return "B"
    elif(marks>=55 and marks<=59):
         return "C+"
    elif(marks>=50 and marks<=54):
         return "C"
    elif(marks>=45 and marks<=49):
         return "D+"
    elif(marks>=40 and marks<=44):
         return "D"
    elif(marks<40):
         return "F"
        

def result_login(request):
    template = get_template('result/result_login.html')
    output = template.render()
    return HttpResponse(output)