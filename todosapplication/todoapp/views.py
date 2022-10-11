from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView
from todoapp import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from todoapp.models import Todos
from django.contrib import messages



class SignUpView(CreateView):
    model = Todos
    form_class = forms.RegistrationForm
    template_name = "registeration.html"
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"your account has been created")
        return super().form_valid(form)


    # def get(self,request,*args,**kwargs):
    #     form=forms.RegistrationForm()
    #     return render(request,"registeration.html",{"form":form})
    #
    # def post(self,request,*args,**kwargs):
    #     form=forms.RegistrationForm(request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         msg = "your account has been created"
    #         messages.success(request, msg)
    #         return redirect("signin")
    #     else:
    #         msg="registration failed"
    #         messages.error(request,msg)
    #         return render(request,"registeration.html",{"form":form})

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=forms.LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                msg="logged in successfully"
                messages.success(request,msg)
                return redirect("index")
            else:
                msg="invalid username or password"
                messages.error(request,msg)
                return render(request,"login.html",{"form":form})
        return render(request,"login.html")

class IndexView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["todos"]=Todos.objects.filter(user=self.request.user,status=False)
        return context
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        msg="logged out successfully"
        messages.success(request,msg)
        return redirect("signin")

class TodoAddView(CreateView):
    model=Todos
    template_name = "add-todo.html"
    form_class = forms.TodoForm
    success_url = reverse_lazy("todos-list")
    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request, "todo has been added")
        return super().form_valid(form)


    # def get(self,request,*args,**kwargs):
    #     form=forms.TodoForm()
    #     return render(request,"add-todo.html",{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=forms.TodoForm(request.POST)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
    #         msg = "todo added successfully"
    #         messages.success(request, msg)
    #         return redirect("index")
    #     else:
    #         msg="something went wrong"
    #         messages.error(request,msg)
    #         return render(request,"add-todo.html",{"form":form})

class TodoListView(ListView):
    model=Todos
    context_object_name = "todos"
    template_name = "todolist.html"

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    # def get(self,request,*args,**kwargs):
    #     all_todos=Todos.objects.filter(user=request.user)
    #     return render(request,"todolist.html",{"todos":all_todos})

# url : localhost:8000/todos/remove/<int:id>
def delete_todo(request,*args,**kwargs):
    id=kwargs.get("id")
    Todos.objects.get(id=id).delete()
    msg="todo deleted"
    messages.success(request,msg)
    return redirect("todos-list")

class TodoDetailView(DetailView):
    model = Todos
    context_object_name = "todo"
    template_name = "todo-detail.html"
    pk_url_kwarg = "id"


    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo=Todos.objects.get(id=id)
    #     return render(request,"todo-detail.html",{"todo":todo})
class TodoEditView(UpdateView):
    model = Todos
    form_class = forms.TodoChangeForm
    template_name = "edit.html"
    success_url = reverse_lazy("todos-list")
    pk_url_kwarg = "id"

    def form_valid(self, form):
        messages.success(self.request, "todo has been updated")
        return super().form_valid(form)

    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo=Todos.objects.get(id=id)
    #     form=forms.TodoChangeForm(instance=todo)
    #     return render(request,"edit.html",{"form":form})
    # def post(self,request,*args,**kwargs):
    #     id = kwargs.get("id")
    #     todo = Todos.objects.get(id=id)
    #     form=forms.TodoChangeForm(request.POST,instance=todo)
    #     if form.is_valid():
    #         form.save()
    #         msg="todo has been updated"
    #         messages.success(request,msg)
    #         return redirect("todos-list")
    #     else:
    #         msg="todo update failed"
    #         messages.error(request,msg)
    #         return render(request,"edit.html",{"form":form})
