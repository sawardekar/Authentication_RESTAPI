# Django Custom Authorization
	Django Authorization base on django groups applied to API controller.
Below step for installations and configurations:
	1>First download authorizeapi package in git repository.
		Install package on the terminal using command:
		pip install django-authorizeapi-1.0.tar.gz [downloaded path]
	2>In your own project setting py in that 
		INSTALLED_APPS = [
		‘authorizeapi’
		]
		MIDDLEWARE = [
		   # 'django.middleware.csrf.CsrfViewMiddleware',    Comment this package
		]
	3>Run command 
		python manage.py makemigrations authorizeapi
	4>Create group and assign to users and also assign super group.
	5>Now applied on any api controller method for example:
		from authorizeapi.permission import Authorize
		@api_view(['GET'])
		@Authorize(['Admin'])   Admin as Group Name,You assign multiple group name
		def read(request):
			.....
			return HttpResponse()

	
