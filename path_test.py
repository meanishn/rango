
import calendar
c = calendar.monthcalendar(2014, 10)
#work list for anish where 1 represents 'has work' and 0 'no work'
#each element is considered as [M,T,W,T,F,S,S]
work_list_anish=[1,1,0,1,0,1]

#capture first week
first_week=c[0]
#show whether anish has work or not 
if (len(work_list_anish)== 7):
    for i in range(len(work_list_anish)):
        if work_list_anish[i]==1:
            print(first_week[i],"\n has work")
        else:
            print(first_week[i],"\n NO WORK")

else:
    print("Schedule can be made only on weekly basis")




#print (calendar.TextCalendar(calendar.MONDAY).formatyear(2014,5,5,5,1))
    
            
            
            
            
            
        
        

    

    

    
