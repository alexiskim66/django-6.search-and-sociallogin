from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.utils import timezone
from .models import Blog
from .forms import BlogForm, PostSearchForm
from django.contrib import messages
from django.db.models import Q
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from django import forms
from django.views.generic import TemplateView

def home(request):
    blogs = Blog.objects.all()
    return render(request, 'home.html', {'blogs':blogs})


def detail(request, id):
    blog = get_object_or_404(Blog, pk=id)
    return render(request, 'detail.html', {'blog':blog})


def delete(request, id):
    delete_blog = Blog.objects.get(id=id)
    delete_blog.delete()
    return redirect('home')


def new(request):
    if request.method == 'POST':
        blog_form = BlogForm(request.POST, request.FILES)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.pub_date = timezone.now()
            blog.save()
            return redirect('home')
    else:
        blog_form = BlogForm()
        return render(request, 'new.html', {'blog_form':blog_form})

def edit(request, id):
    blog = get_object_or_404(Blog, pk=id)
    if request.method == 'GET':
        blog_form = BlogForm(instance=blog)
        return render(request, 'edit.html', {'edit_blog':blog_form})
    else:
        blog_form = BlogForm(request.POST, request.FILES, instance=blog)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.pub_date = timezone.now()
            blog.save()
        return redirect('/wiki/' + str(id))


# class BlogListView(ListView):
#     model = Blog
#     paginate_by = 15
#     template_name = 'wiki/home.html'  #DEFAULT : <app_label>/<model_name>_list.html
#     context_object_name = 'wiki_list'        #DEFAULT : <app_label>_list




#쿼리셋 가져오기
def get_queryset(self):
    searchWord = self.request.GET.get('q', '')
    search_type = self.request.GET.get('type', '')
    blog_list = Blog.objects.order_by('-id') 
        
    if searchWord :
        if len(searchWord) > 1 :
            if search_type == 'all':
                search_blog_list = blog_list.filter(Q (title__icontains=searchWord) | Q (body__icontains=searchWord))
            elif search_type == 'title':
                search_blog_list = blog_list.filter(title__icontains=searchWord)    
            elif search_type == 'content':
                search_blog_list = blog_list.filter(content__icontains=searchWord)    
            elif search_type == 'writer':
                search_blog_list = blog_list.filter(writer__user_id__icontains=searchWord)

                # if not search_blog_list :
                #     messages.error(self.request, '일치하는 검색 결과가 없습니다.')
            return search_blog_list
        else:
            messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
    return blog_list


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tagname'] = self.kwargs['tag']
    return context


class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Blog.objects.filter(Q(title__icontains=searchWord) | Q(writer__icontains=searchWord) | Q(body__icontains=searchWord)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['wiki_list'] = post_list

        return render(self.request, self.template_name, context)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     paginator = context['paginator']
    #     page_numbers_range = 5
    #     max_index = len(paginator.page_range)

    #     page = self.request.GET.get('page')
    #     current_page = int(page) if page else 1

    #     start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    #     end_index = start_index + page_numbers_range
    #     if end_index >= max_index:
    #         end_index = max_index

    #     page_range = paginator.page_range[start_index:end_index]
    #     context['page_range'] = page_range

    #     search_keyword = self.request.GET.get('q', '')
    #     search_type = self.request.GET.get('type', '')
    #     blog_fixed = Blog.objects.filter(top_fixed=True).order_by('-registered_date')

    #     if len(search_keyword) > 1 :
    #         context['q'] = search_keyword
    #     context['type'] = search_type
    #     context['blog_fixed'] = blog_fixed

    #     return context

class HomeView(TemplateView):
        template_name = 'search.html'