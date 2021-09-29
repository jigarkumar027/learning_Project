from django.urls import path,include
from . import views
urlpatterns = [
   path('',views.index,name='index'),
   path('rpage/',views.registerpage,name='registerpage'),
   path('login/',views.loginstudent,name='loginpage'),
   path('tlogin/',views.Tutorlogin,name='loginTutor'),
   path('rtutor/',views.TutorRegister,name='registerTutor'),
   path('resisters/',views.registerstudent,name='registerstudent'),
   path('otpstudent/',views.otpstudent,name='otpstudent'),
   path('loginvarifyS/',views.loginvarifyS,name='loginvarifyS'),
   path('indexTutor/',views.indexTutor,name='indexTutor'),
   path('sprofile/',views.student_profile,name='student_profile'),
   path('sdata/<int:pk>',views.student_data,name='student_data'),
   path('logouts/',views.studentlogout,name='studentlogout'),
   path('logintutordata/',views.loginTutor_data,name='loginTutor_data'),
   path('registerT/',views.registerT,name='registerT'),
   path('OtpvarifyTotor/',views.OtpvarifyTotor,name='OtpvarifyTotor'),


   #########################  --  tutor  -- ###############################
   path('addcourse/',views.addcourse,name='addcourse'),
   path('coursedata/',views.coursedata,name='coursedata'),
   path('tutorlogout/',views.tutorlogout,name='tutorlogout'),
   

   ######################### -- course  -- ##################################
   path('shopgrid/',views.shopgrid,name='shopgrid'),
   path('class_grid/',views.class_grid,name='class_grid'),
   path('course_detail/<int:pk>',views.course_detail,name='course_detail'),

   ########################### -- cart -- ##################################
   path('cart/<int:pk>',views.cart,name='cart'),
   path('cremove/<int:pk>',views.cremove,name='cremove'),
   path('checkout/',views.checkout,name='checkout'),
   path('cart_gen/',views.cart_gen,name='cart_gen'),

   ##########################  -- admin -- ################################
   path('adminpage/',views.admin,name='admin'),

   # paytm
   path('pay/',views.initiate_payment, name='pay'),
   path('callback/', views.callback, name='callback'),
   path('welcomeback/',views.welcome,name='welcome')
   
]
