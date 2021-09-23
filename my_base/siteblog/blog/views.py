from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import (TemplateView,ListView,
                                    DetailView,CreateView,
                                    UpdateView,DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm,CommentForm,UserForm
from django.utils import timezone
from .models import Post,Comment,User
from django.urls import reverse_lazy
# Create your views here.



class RegisterView(CreateView):
    model = User
    form = UserForm
    template_name='registration.html'
    success_url = reverse_lazy('post_list')
    success_messege = 'You are now registered!<3'
    fields=('username','password','email','first_name','last_name')



class AboutView(TemplateView):
     template_name = 'about.html'

#####################################POSTS###############################################
class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(publication_date__lte= timezone.now()).order_by('-publication_date') #'publication_date__lte' means filter by less then or equal to. the '-' in 'order_by('-published_date ')' is telling it to order the in newest post first


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model =Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model =Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url= '/login/'
    redirect_field_name='blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(publication_date__isnull=True).order_by('create_date') #Show unpublished posts only!

@staff_member_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)




#####################################COMMENTS###############################################





def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form= CommentForm(request.POST)
        if form.is_valid():
            comment =form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form}) 

@staff_member_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)


@staff_member_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk

    comment.delete()
    return redirect('post_detail',pk=post_pk)

